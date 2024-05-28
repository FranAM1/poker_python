import socket
import threading
import json
from game.card import Card
from game.__init__ import print_cards_in_rows


class PokerClient:
    def __init__(self, host="localhost", port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print(f"Conectado al servidor{host}:{port}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024)
                if message:
                    data = json.loads(message.decode())
                    if "pot" in data:
                        print(f'Bote actual: {data["pot"]}')
                    if "player_chips" in data:
                        player_chips = data["player_chips"]
                        print(
                            f'El jugador {player_chips["name"]} ha apostado {player_chips["bet"]} fichas. Fichas restantes: {player_chips["chips"]}'
                        )
                    if "voted" in data:
                        print(data["voted"])
                    if "game_started" in data:
                        print(data["game_started"])
                    if "game_not_started" in data:
                        print(data["game_not_started"])
                    if "not_your_turn" in data:
                        print(data["not_your_turn"])
                    if "no_action" in data:
                        print(data["no_action"])
                    if "actions" in data:
                        print("Acciones disponibles:")
                        for action in data["actions"]:
                            print(action)
                    if "hand" in data:
                        hand_data = data["hand"]
                        hand = [Card(card["suit"], card["rank"]) for card in hand_data]
                        print("Tu mano:")
                        print_cards_in_rows(hand)
                    if "chips" in data:
                        print(f'Fichas restantes: {data["chips"]}')
                    if "board" in data:
                        board_data = data["board"]
                        board = [
                            Card(card["suit"], card["rank"]) for card in board_data
                        ]
                        print("Cartas de la mesa: ")
                        print_cards_in_rows(board)
                    if "folded" in data:
                        print(f'El jugador {data["folded"]} ha pasado.')
                    if "current_turn" in data:
                        print(f'Es el turno de {data["current_turn"]}')
                    if "winners" in data:
                        print("Ganadores:")
                        print(data["winners"]["players"])
                        print(
                            f'{data["winners"]["players"]} con {data["winners"]["hand"]}'
                        )
                        print(
                            f'El bote de {data["winners"]["pot"]} fichas se ha repartido.'
                        )
                    if "error" in data:
                        print(data["error"])
                else:
                    break
            except:
                break
        self.client_socket.close()

    def send_message(self, message):
        self.client_socket.sendall(json.dumps(message).encode())

    def start(self):
        threading.Thread(target=self.receive_messages).start()


def run_client():
    client = PokerClient()
    client.start()

    player_name = input("Escribe tu nombre: ")
    client.send_message(player_name)

    while True:
        action = input('Escribe una accion (ver todas con "acciones"): \n')

        if action == "salir":
            client.send_message({"action": action})
            print("Desconectándose del servidor...")
            break
        elif action == "raise":
            amount = int(input("Escribe la cantidad que quieres apostar: "))
            client.send_message({"action": action, "amount": amount})
        elif action in [
            "votar",
            "acciones",
            "call",
            "fold",
            "mano",
            "bote",
            "fichas",
            "mesa",
            "check",
            "all-in",
        ]:
            client.send_message({"action": action})
        else:
            client.send_message({"action": action})
