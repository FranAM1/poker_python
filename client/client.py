import socket
import threading
import json
from . import actions
import queue
class PokerClient:
    def __init__(self, host='localhost', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.output_queue = queue.Queue()
        print(f'Conectado al servidor{host}:{port}')

    def print_message(self, message):
        self.output_queue.put(message)

    def handle_output(self):
        while True:
            message = self.output_queue.get()
            if message is None:
                break
            print(message)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024)
                if message:
                    data = json.loads(message.decode())

                    if "pot" in data:
                        self.print_message(f'Bote actualizado: {data["pot"]}')
                    if "player_chips" in data:
                        player_chips = data["player_chips"]
                        self.print_message(f'El jugador {player_chips["name"]} ha apostado {player_chips["bet"]} fichas. Fichas restantes: {player_chips["chips"]}')
                    if "voted" in data:
                        self.print_message(data["voted"])
                    if "game_started" in data:
                        self.print_message(data["game_started"])
                    if "game_not_started" in data:
                        self.print_message(data["game_not_started"])
                    
                else:
                    break
            except:
                break
        self.client_socket.close()

    def send_message(self, message):
        self.client_socket.sendall(json.dumps(message).encode())

    def start(self):
        threading.Thread(target=self.receive_messages).start()
        threading.Thread(target=self.handle_output).start()

def run_client():
    client = PokerClient()
    client.start()

    player_name = input('Escribe tu nombre: ')
    client.send_message(player_name)

    while True:
            action = input('Escribe una accion (ver todas con "acciones"): ')
            
            if action == "acciones":
                client.print_message('Acciones disponibles:')
                for action in actions:
                    client.print_message(action)
            elif action == "votar":
                client.send_message({"action": action})
            elif action == "apuesta":
                amount = int(input('Escribe la cantidad que quieres apostar: '))
                client.send_message({"action": action, "amount": amount})
            elif action == "salir":
                client.send_message({"action": action})
                client.print_message("Desconectándose del servidor...")
                break
            else:
                client.print_message('Accion no tratada. Escribe "acciones" para ver las acciones disponibles.')