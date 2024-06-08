import socket
import threading
import json
from game.player import Player
from game.game import Game
from . import actions, validate_users_turn


class PokerServer:
    def __init__(self, host="192.168.0.10", port=12345, max_players=4):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(max_players)
        self.clients = {}
        self.max_players = max_players
        self.game = Game()
        print(f"Servidor iniciado en {host}:{port}")

    def broadcast(self, message, sender_socket=None):
        if sender_socket:
            self.send_message_to_client(sender_socket, message)
        else:
            for client in self.clients:
                self.send_message_to_client(client, message)

    def send_message_to_client(self, client_socket, message):
        try:
            client_socket.sendall(message)
        except:
            print("Error enviando mensaje al cliente.")
            client_socket.close()
            if client_socket in self.clients:
                del self.clients[client_socket]

    def handle_client(self, client_socket):
        try:
            player_name = client_socket.recv(1024).decode()
            player = Player(player_name)
            self.game.add_player(player)
            self.clients[client_socket] = player
            print(f"El jugador {player_name} se ha unido.")
            self.broadcast(
                json.dumps(
                    {
                        "player_joined": f"{player_name} se ha unido al juego. Jugadores actuales: {len(self.clients)}/{self.max_players}"
                    }
                ).encode()
            )

            while True:
                message = client_socket.recv(1024)
                if not message:
                    break

                decoded_message = message.decode()
                data = json.loads(decoded_message)
                action = data.get("action")
                player = self.clients[client_socket]
                print(f"Recibido de {player.get_name()}: {action}")

                self.process_action(action, data, player, client_socket)

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error en los datos recibidos: {e}")
        except Exception as e:
            print(f"Error manejando el cliente: {e}")
        finally:
            self.cleanup_client(client_socket, player)

    def process_action(self, action, data, player, client_socket):
        if action == "votar":
            self.handle_vote_action(player, client_socket)
        elif action == "acciones":
            self.send_message_to_client(
                client_socket, json.dumps({"actions": actions}).encode()
            )
        elif action == "salir":
            self.game.remove_player(player)
            self.cleanup_client(client_socket, player)
        elif not self.game.has_started():
            self.send_message_to_client(
                client_socket,
                json.dumps(
                    {
                        "game_not_started": "El juego no ha comenzado. No se permiten acciones hasta que comience el juego."
                    }
                ).encode(),
            )
        elif player.has_lost():
            self.send_message_to_client(
                client_socket,
                json.dumps(
                    {"has_lost": "Has perdido no puedes seguir jugando."}
                ).encode(),
            )
        else:
            self.process_game_action(action, data, player, client_socket)

    def handle_vote_action(self, player, client_socket):
        if player.get_voted_to_start():
            self.send_message_to_client(
                client_socket,
                json.dumps({"voted": "Ya has votado para comenzar el juego."}).encode(),
            )
        else:
            self.game.add_vote_to_start()
            player.voted_to_start()
            print(
                f"Voto recibido de {player.get_name()}. Votos totales: {self.game.get_votes_to_start()}"
            )
            if self.game.has_started():
                self.broadcast(
                    json.dumps(
                        {
                            "game_started": "El juego ha comenzado!",
                            "current_turn": self.game.get_current_player().get_name(),
                        }
                    ).encode()
                )
            else:
                self.broadcast(
                    json.dumps(
                        {
                            "game_not_started": f"Voto recibido de {player.get_name()}. Esperando votos de otros jugadores."
                        }
                    ).encode()
                )

    def process_game_action(self, action, data, player, client_socket):
        if action in ["mano", "bote", "mesa", "fichas"]:
            self.handle_information_request(action, player, client_socket)
        elif not validate_users_turn(self.game, player):
            self.send_message_to_client(
                client_socket,
                json.dumps({"not_your_turn": "No es tu turno de jugar."}).encode(),
            )
        elif action in ["raise", "check", "call", "fold", "all-in"]:
            self.handle_player_turn(action, data, player, client_socket)

    def handle_player_turn(self, action, data, player, client_socket):
        if action == "raise":
            amount = int(data["amount"])
            self.handle_raise_action(amount, player, client_socket)
        elif action == "check":
            self.handle_check_action(player, client_socket)
        elif action == "call":
            self.handle_call_action(player, client_socket)
        elif action == "fold":
            self.handle_fold_action(player)
        elif action == "all-in":
            self.handle_all_in_action(player, client_socket)
        else:
            self.send_message_to_client(
                client_socket,
                json.dumps({"error": "Accion no tratada"}).encode(),
            )

    def handle_raise_action(self, amount, player, client_socket):
        if amount > player.get_chips():
            self.send_message_to_client(
                client_socket, json.dumps({"error": "Fichas insuficientes"}).encode()
            )
        else:
            if self.game.place_bet(player, amount):
                self.advance_game(player)
            else:
                self.send_message_to_client(
                    client_socket,
                    json.dumps({"error": "Fichas insuficientes"}).encode(),
                )

    def handle_check_action(self, player, client_socket):
        if player.get_current_bet() < self.game.get_current_bet():
            self.send_message_to_client(
                client_socket,
                json.dumps(
                    {
                        "error": "No puedes hacer check porque hay una apuesta superior a la tuya"
                    }
                ).encode(),
            )
        else:
            self.advance_game(player)

    def handle_call_action(self, player, client_socket):
        amount = min(self.game.get_current_bet(), player.get_chips())
        if self.game.place_bet(player, amount):
            self.advance_game(player)
        else:
            self.send_message_to_client(
                client_socket, json.dumps({"error": "Fichas insuficientes"}).encode()
            )

    def handle_fold_action(self, player):
        player.fold()
        self.broadcast(json.dumps({"folded": player.get_name()}).encode())
        self.advance_game(player)

    def handle_all_in_action(self, player, client_socket):
        amount = player.get_chips()
        if self.game.place_bet(player, amount):
            self.advance_game(player)
        else:
            self.send_message_to_client(
                client_socket, json.dumps({"error": "Fichas insuficientes"}).encode()
            )

    def handle_information_request(self, action, player, client_socket):
        if action == "mano":
            hand = [card.to_dict() for card in player.get_hand()]
            self.send_message_to_client(
                client_socket, json.dumps({"hand": hand}).encode()
            )
        elif action == "bote":
            self.send_message_to_client(
                client_socket, json.dumps({"pot": self.game.get_pot()}).encode()
            )
        elif action == "mesa":
            board = [card.to_dict() for card in self.game.get_board()]
            self.send_message_to_client(
                client_socket, json.dumps({"board": board}).encode()
            )
        elif action == "fichas":
            self.send_message_to_client(
                client_socket, json.dumps({"chips": player.get_chips()}).encode()
            )
        else:
            self.send_message_to_client(
                client_socket, json.dumps({"error": "Accion no tratada"}).encode()
            )

    def advance_game(self, player):
        player.set_has_played(True)
        self.game.next_turn()
        self.check_winner()
        if self.game.has_started():
            self.broadcast_game_state()

    def cleanup_client(self, client_socket, player):
        if client_socket in self.clients:
            del self.clients[client_socket]
        if player in self.game.get_players():
            self.game.get_players().remove(player)
        client_socket.close()
        
        if self.game.has_started() and len(self.clients) < 2:
            print("Fin del juego.")
            self.game.set_started(False)
            self.game.reset_player_votes()
            self.game.reset_players_new_game()
            self.broadcast(
                json.dumps(
                    {
                        "game_over": "Fin del juego. No hay suficientes jugadores para continuar."
                    }
                ).encode()
            )


    def check_winner(self):
        winners = self.game.get_winners()
        if winners:
            self.broadcast_winner(winners)
            self.game.reset_round()
            self.handle_end_of_round()

    def broadcast_winner(self, winners):
        if winners:
            winner_names = [winner.get_name().strip('"') for winner in winners]
            response = json.dumps(
                {
                    "winners": {
                        "players": winner_names,
                        "pot": self.game.get_pot(),
                        "hand": winners[0].get_hand_ranking(self.game.get_board()),
                    }
                }
            )
            self.broadcast(response.encode())

    def broadcast_game_state(self):
        state = {
            "pot": self.game.get_pot(),
            "board": [card.to_dict() for card in self.game.get_board()],
            "current_turn": self.game.get_current_player().get_name(),
        }
        self.broadcast(json.dumps(state).encode())

    def handle_end_of_round(self):
        self.check_for_losers()

        active_players = [
            player for player in self.clients.values() if not player.has_lost()
        ]
        print(f"Jugadores activos: {[player.get_name() for player in active_players]}")

        if len(active_players) == 1:
            player_name = active_players[0].get_name()
            print(f"El jugador {player_name} es el ganador.")
            message = json.dumps(
                {
                    "game_over": "Fin del juego. Ganador: " + player_name,
                }
            ).encode()
            self.broadcast(message)
            print("Fin del juego.")
            self.game.set_started(False)
            self.game.reset_player_votes()
            self.game.reset_players_new_game()

    def check_for_losers(self):
        for client_socket in list(self.clients.keys()):
            client_player = self.clients[client_socket]
            if client_player.has_lost():
                self.send_message_to_client(
                    client_socket,
                    json.dumps({"loser": client_player.get_name()}).encode(),
                )
                print(f"El jugador {client_player.get_name()} ha perdido.")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            if len(self.clients) >= self.max_players:
                print(
                    f"Conexión rechazada de {client_address}. Máximo de jugadores alcanzado."
                )
                self.send_message_to_client(
                    client_socket,
                    json.dumps({"error": "Máximo de jugadores alcanzado."}).encode(),
                )
                client_socket.close()
                continue

            if self.game.has_started():
                print(
                    f"Conexión rechazada de {client_address}. El juego ya ha comenzado."
                )
                self.send_message_to_client(
                    client_socket,
                    json.dumps({"error": "El juego ya ha comenzado."}).encode(),
                )
                client_socket.close()
                continue

            print(f"Nueva conexion de {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()


def run_server():
    server = PokerServer()
    server.start()
