from game.card import Card
from game.deck import Deck
from game import print_cards_in_rows
from utils.poker_logic import value_of_hand
import threading
import subprocess

def start_server():
    print("Iniciando el servidor...")
    subprocess.run(["python", "server/server.py"])

def start_client():
    print("Iniciando el cliente...")
    subprocess.run(["python", "client/client.py"])

if __name__ == "__main__":
    # Ejecutar el servidor y el cliente en subprocesos separados
    server_thread = threading.Thread(target=start_server)
    client_thread = threading.Thread(target=start_client)

    server_thread.start()
    client_thread.start()

    # Esperar a que ambos subprocesos terminen
    server_thread.join()
    client_thread.join()
    
