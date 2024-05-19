import socket
import threading
import json
from . import actions
class PokerClient:
    def __init__(self, host='localhost', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print(f'Conectado al servidor{host}:{port}')

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024)
                if message:
                    data = json.loads(message.decode())

                    if "pot" in data:
                        print(f'Bote actualizado: {data["pot"]}')
                    if "player_chips" in data:
                        print(f'Tus fichas: {data["player_chips"]}')
                    if "voted" in data:
                        print(data["voted"])
                    if "game_started" in data:
                        print(data["game_started"])
                    
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

    player_name = input('Escribe tu nombre: ')
    client.send_message(player_name)

    while True:
            action = input('Escribe una accion (ver todas con "acciones"): ')
            
            if action == "acciones":
                print('Acciones disponibles:')
                for action in actions:
                    print(action)
            elif action == "votar":
                client.send_message({"action": action})
            elif action == "apuesta":
                amount = int(input('Escribe la cantidad que quieres apostar: '))
                client.send_message({"action": action, "amount": amount})
            elif action == "salir":
                client.send_message({"action": action})
                break
            else:
                print('Accion no tratada. Escribe "acciones" para ver las acciones disponibles.')