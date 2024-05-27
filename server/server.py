import socket
import threading
import json
from game.player import Player
from game.game import Game
from . import actions, validate_users_turn


class PokerServer:
    def __init__(self, host="localhost", port=12345, max_players=4):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(max_players)
        self.clients = {}
        self.max_players = max_players
        self.game = Game()
        print(f"Servidor iniciado en {host}:{port}")

    def broadcast(self, message, sender_socket=None):
        if sender_socket:
            try:
                sender_socket.sendall(message)
            except:
                print("Error enviando mensaje al cliente.")
                sender_socket.close()
                del self.clients[sender_socket]
        else:
            for client in self.clients:
                try:
                    client.sendall(message)
                except:
                    print("Error enviando mensaje al cliente.")
                    client.close()
                    del self.clients[client]

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
                        "success": "Te has unido al juego. Espera a que comience el juego."
                    }
                ).encode()
            )

            while True:
                message = client_socket.recv(1024)
                if message:
                    decoded_message = message.decode()
                    data = json.loads(decoded_message)
                    action = data["action"]
                    player: Player = self.clients[client_socket]
                    print(f"Recibido de {player.get_name()}: {action}")

                    if action == "votar":
                        if player.get_voted_to_start():
                            response = json.dumps(
                                {"voted": "Ya has votado para comenzar el juego."}
                            )
                            self.broadcast(response.encode(), client_socket)
                        else:
                            self.game.add_vote_to_start()
                            player.voted_to_start()
                            print(
                                f"Voto recibido de {player.get_name()}.  Votos totales: {self.game.get_votes_to_start()}"
                            )
                            self.game.start()

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

                    elif action == "acciones":
                        response = json.dumps({"actions": actions})
                        self.broadcast(response.encode(), client_socket)

                    elif action == "salir":
                        break

                    elif not self.game.has_started():
                        message = json.dumps(
                            {
                                "game_not_started": "El juego no ha comenzado. No se permiten acciones hasta que comience el juego."
                            }
                        )
                        self.broadcast(message.encode(), client_socket)

                    # MARK: All turns
                    elif action == "mano":
                        player_hand = player.get_hand()
                        hand = [card.to_dict() for card in player_hand]
                        response = json.dumps({"hand": hand})
                        self.broadcast(response.encode(), client_socket)

                    elif action == "bote":
                        response = json.dumps({"pot": self.game.get_pot()})
                        self.broadcast(response.encode(), client_socket)

                    elif action == "mesa":
                        response = json.dumps(
                            {
                                "board": [
                                    card.to_dict() for card in self.game.get_board()
                                ]
                            }
                        )
                        self.broadcast(response.encode(), client_socket)

                    elif action == "fichas":
                        response = json.dumps(
                            {
                                "chips": player.get_chips(),
                            }
                        )
                        self.broadcast(response.encode(), client_socket)

                    # MARK: Validate player's turn
                    elif not validate_users_turn(self.game, player):
                        message = json.dumps(
                            {"not_your_turn": "No es tu turno de jugar."}
                        )
                        self.broadcast(message.encode(), client_socket)

                    # MARK: Player's turn
                    elif action == "raise":
                        amount = data["amount"]
                        if self.game.place_bet(player, amount):
                            self.game.next_turn()
                            player.set_has_played(True)
                            self.check_winner()
                            self.broadcast_game_state()
                        else:
                            self.broadcast(
                                {
                                    "error": "Apuesta muy baja o no tienes suficientes fichas"
                                }.encode(),
                                client_socket,
                            )

                    elif action == "check":
                        player.set_has_played(True)
                        self.game.next_turn()
                        player.set_has_played(True)
                        self.check_winner()
                        self.broadcast_game_state()

                    elif action == "call":
                        amount = self.game.get_current_bet()
                        if self.game.place_bet(player, amount):
                            self.game.next_turn()
                            player.set_has_played(True)
                            self.check_winner()
                            self.broadcast_game_state()
                        else:
                            self.broadcast(
                                {"error": "Fichas insuficientes"}.encode(),
                                client_socket,
                            )

                    elif action == "fold":
                        player.fold()
                        player.set_has_played(True)
                        self.game.next_turn()
                        self.check_winner()
                        self.broadcast_game_state()

                    elif action == "all_in":
                        amount = player.get_chips()
                        if self.game.place_bet(player, amount):
                            player.set_has_played(True)
                            self.game.next_turn()
                            self.check_winner()
                            self.broadcast_game_state()
                        else:
                            self.broadcast(
                                {"error": "Fichas insuficientes"}.encode(),
                                client_socket,
                            )

                    else:
                        response = json.dumps({"no_action": "Accion no tratada"})
                        self.broadcast(response.encode(), client_socket)

                else:
                    break
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            if client_socket in self.clients:
                del self.clients[client_socket]
            if player in self.game.get_players():
                self.game.get_players().remove(player)
            client_socket.close()

    def check_winner(self):
        if self.game.get_winners():
            self.broadcast_winner(self.game.get_winners())
            self.game.reset_round()

    def broadcast_winner(self, winners):
        if winners:
            winner_names = [winner.get_name() for winner in winners]
            response = json.dumps(
                {
                    "winners": {
                        "players": winner_names,
                        "pot": self.game.get_pot(),
                        "hand": winners[0].get_hand_ranking(self.game.get_board()),
                    }
                }
            )
            print(f"El bote de {self.game.get_pot()} fichas se ha repartido.")
            print(response)
            self.broadcast(response.encode())

    def broadcast_game_state(self):
        state = {
            "pot": self.game.get_pot(),
            "board": [card.to_dict() for card in self.game.get_board()],
            "current_turn": self.game.get_current_player().get_name(),
        }
        self.broadcast(json.dumps(state).encode())

    def check_and_advance_round(self):
        if all(player.get_has_played() for player in self.game.get_players()):
            self.game.next_round()
            self.broadcast_game_state()

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            if len(self.clients) >= self.max_players:
                print(
                    f"Conexión rechazada de {client_address}. Máximo de jugadores alcanzado."
                )
                client_socket.sendall(
                    json.dumps({"error": "Máximo de jugadores alcanzado."}).encode()
                )
                client_socket.close()
                continue

            if self.game.has_started():
                print(
                    f"Conexión rechazada de {client_address}. El juego ya ha comenzado."
                )
                client_socket.sendall(
                    json.dumps({"error": "El juego ya ha comenzado."}).encode()
                )
                client_socket.close()
                continue

            print(f"Nueva conexion de {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()


def run_server():
    server = PokerServer()
    server.start()
