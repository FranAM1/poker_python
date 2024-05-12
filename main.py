from game.deck import Deck
from game.player import Player
from game import print_cards_in_rows
from utils.poker_logic import value_of_hand
import threading
import subprocess

while True:
    deck = Deck()
    deck.build_new_deck()

    player1 = Player("Jugador 1")
    player2 = Player("Jugador 2")

    player1.add_card(deck.draw())
    player1.add_card(deck.draw())
    player2.add_card(deck.draw())
    player2.add_card(deck.draw())

    print("Mano del jugador 1:")
    player1.print_hand()

    print("Mano del jugador 2:")
    player2.print_hand()
    
    break
