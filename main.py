from game.deck import Deck
from game.player import Player
from game import print_cards_in_rows
from utils.poker_logic import value_of_hand
import sys
from client.client import run_client
from server.server import run_server

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <server|client>")
        sys.exit(1)

    role = sys.argv[1]
    
    if role == 'server':
        run_server()
    elif role == 'client':
        run_client()
    else:
        print("Rol invalido. Uso: python main.py <server|client>")
        sys.exit(1)

if __name__ == "__main__":
    main()