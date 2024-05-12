from game.card import Card
from . import print_cards_in_rows

class Player:
    __hand: list[Card]

    def __init__(self, name):
        self.__name = name
        self.__score = 0

    def add_score(self, score: int):
        self.__score += score

    def __str__(self):
        return f"{self.get_name} has {self.get_score} points."
    
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

    def get_score(self):
        return self.__score
    
    def set_score(self, score):
        return self.__score