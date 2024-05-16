from game.card import Card
from . import print_cards_in_rows

class Player:
    __hand: list[Card]

    def __init__(self, name):
        self.__name = name
        self.__chips = 0
        self.__hand = []

    def add_chips(self, chips: int):
        self.__chips += chips

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