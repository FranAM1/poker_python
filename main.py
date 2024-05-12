from game.card import Card
from game.deck import Deck
from game import print_cards_in_rows
from utils.poker_logic import value_of_hand

# build the deckç

while True:
    test = input("Pedir mano? (s/n): ")

    if test == "s":
        deck = Deck()
        deck.build_new_deck()
        hand = [deck.draw() for _ in range(2)]
        print_cards_in_rows(hand)

        while True:
            board = input("Pedir mesa? (s/n): ")
            if board == "s":
                deck.draw_board()
                print_cards_in_rows(deck.board)
            elif board == "n":
                break

            if len(deck.board) == 5:
                print("Mano: ")
                print_cards_in_rows(hand)
                print("Mesa: ")
                print_cards_in_rows(deck.board)
                print(value_of_hand(hand, deck.board))
        
    elif test == "n":
        break
