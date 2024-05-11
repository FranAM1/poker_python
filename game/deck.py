import random
from game.card import Card
from game import SUITS, RANKS

class Deck:
    cards: list
    board: list
    MAX_CARDS = 52
    MAX_BOARD = 5

    def __init__(self):
        self.cards = []
        self.board = []
    
    def __str__(self) -> str:
        return f"Deck with {self.get_deck_count()} cards"

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
    
    def draw_board(self) -> Card|None:
        if len(self.board) >= self.MAX_BOARD:
            print("La mesa ya tiene 5 cartas.")
            return None
        
        self.board.append(self.draw())
        return self.board[-1]

    def get_deck_count(self):
        return len(self.cards)
    
    def build_new_deck(self):
        self.cards = []
        self.board = []
        for suit in SUITS.keys():
            for rank in RANKS.keys():
                self.add_card(Card(suit, rank))
        self.shuffle()