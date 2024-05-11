from game.card import Card
from game.deck import Deck
from game import print_cards_in_rows

# build the deck


deck = Deck()
deck.build_deck()
print_cards_in_rows(deck.cards)
