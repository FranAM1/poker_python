import socket
import threading
import json
from game.player import Player
from game.card import Card
from game.game import Game 

class PokerServer:
    def __init__(self, host='localhost', port=12345, max_players=4):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(max_players)
        self.clients = {}
        self.max_players = max_players
        self.game = Game()
        print(f'Servidor iniciado en {host}:{port}')

    def broadcast(self, message, sender_socket=None):
        if sender_socket:
            try:
                sender_socket.sendall(message)
            except:
                print('Error enviando mensaje al cliente.')
                sender_socket.close()
                del self.clients[sender_socket]
        else:
            for client in self.clients:
                try:
                    client.sendall(message)
                except:
                    print('Error enviando mensaje al cliente.')
                    client.close()
                    del self.clients[client]

    def handle_client(self, client_socket):
        try:
            # Receive player name
            player_name = client_socket.recv(1024).decode()
            player = Player(player_name)
            self.game.add_player(player)
            self.clients[client_socket] = player
            print(f'El jugador {player_name} se ha unido.')
            self.broadcast(json.dumps(
                {"success": 'Te has unido al juego. Espera a que comience el juego.'}
            ).encode())

            while True:
                message = client_socket.recv(1024)
                if message:
                    decoded_message = message.decode()
                    data = json.loads(decoded_message)
                    action = data['action']
                    player: Player = self.clients[client_socket]
                    print(f'Recibido de {player.get_name()}: {action}')

                    if action == "votar":
                        if player.get_voted_to_start():
                            response = json.dumps(
                                {"voted": "Ya has votado para comenzar el juego."}
                            )
                            self.broadcast(
                                response.encode(),
                                client_socket
                            )
                        else:
                            self.game.add_vote_to_start()
                            player.voted_to_start()
                            print(f'Voto recibido de {player.get_name()}.  Votos totales: {self.game.get_votes_to_start()}')
                            if (self.game.get_votes_to_start == 
                                len(self.game.get_players())
                            ):
                                self.game.start()
                                self.broadcast(json.dumps(
                                    {"game_started": "El juego ha comenzado!"}
                                ).encode())
                    
                    elif not self.game.has_started():
                        message = json.dumps(
                            {"game_not_started": "El juego no ha comenzado. No se permiten acciones hasta que comience el juego."}
                        )
                        self.broadcast(
                            message.encode(),
                            client_socket
                        )    

                    elif action == "apuesta":
                        amount = data["amount"]
                        player.remove_chips(amount)
                        self.game.add_to_pot(amount)

                    
                else:
                    break
        except Exception as e:
            print(f'Error handling client: {e}')
        finally:
            del self.clients[client_socket]
            self.game.get_players().remove(player)
            client_socket.close()
            print(f'El jugador {player.get_name()} ha salido.')

    def start(self):
        while True:
            if len(self.clients) < self.max_players and not self.game.has_started():
                client_socket, client_address = self.server_socket.accept()
                print(f'Nueva conexion de {client_address}')
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            elif self.game.has_started():
                print("El juego ha comenzado. No se permiten nuevas conexiones.")
            else:
                print("Maximo de jugadores alcanzado. No se permiten nuevas conexiones.")

def run_server():
    server = PokerServer()
    server.start()