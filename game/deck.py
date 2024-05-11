import random
from game.card import Card

class Deck:
    cards: list

    def __init__(self, cards=[]):
        self.cards = cards
    
    def __str__(self) -> str:
        return '\n'.join([str(card) for card in self.cards])

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def shuffle(self):
        random.shuffle(self.cards)
        pass

    def draw(self) -> Card|None:
        deck_count = self.get_deck_count()
        if deck_count == 0:
            return None
        
        random_index = random.randint(0, deck_count - 1)
        card = self.cards[random_index]
        self.cards.pop(random_index)
        return card

    def get_deck_count(self):
        return len(self.cards)