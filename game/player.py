from game.card import Card
from . import print_cards_in_rows

class Player:
    __hand: list[Card]
    __voted_to_start: bool

    def __init__(self, name):
        self.__name = name
        self.__chips = 500
        self.__hand = []
        self.__voted_to_start = False

    def voted_to_start(self):
        self.__voted_to_start = True

    def add_chips(self, chips: int):
        self.__chips += chips

    def remove_chips(self, chips: int):
        self.__chips -= chips

    def reset_hand(self):
        self.__hand = []

    def __str__(self):
        return f"{self.get_name} tiene {self.get_chips} puntos."
    
    def add_card(self, card):
        self.__hand.append(card)

    def clear_hand(self):
        self.__hand = []
    
    def print_hand(self):
        print_cards_in_rows(self.__hand)


    
    # MARK: - Getters and Setters
    def get_hand(self):
        return self.__hand
    
    def set_hand(self, hand):
        self.__hand = hand

    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

    def get_chips(self):
        return self.__chips
    
    def set_chips(self, chips):
        return self.__chips
    
    def get_voted_to_start(self):
        return self.__voted_to_start
    
    def set_voted_to_start(self, voted_to_start):
        self.__voted_to_start = voted_to_start