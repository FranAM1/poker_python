from game.card import Card
from game.deck import Deck

# build the deck
cards = []
for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
    for rank in ['1','2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']:
        cards.append(Card(suit, rank))

deck = Deck(cards)
print(deck)