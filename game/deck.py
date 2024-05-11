

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
        pass

    def draw(self):
        pass

    def draw_hand(self):
        pass