from game.card import Card
from . import print_cards_in_rows
from utils.poker_logic import get_hand_ranking_from_value, value_of_hand


class Player:
    __hand: list[Card]
    __voted_to_start: bool
    __folded: bool
    __current_bet: int
    __has_played: bool
    __has_lost: bool

    def __init__(self, name):
        self.__name = name
        self.__chips = 100
        self.__hand = []
        self.__voted_to_start = False
        self.__folded = False
        self.__current_bet = 0
        self.__has_played = False
        self.__has_lost = False

    def to_dict(self):
        return {
            "name": self.__name,
            "chips": self.__chips,
            "hand": [card.to_dict() for card in self.__hand],
            "voted_to_start": self.__voted_to_start,
            "folded": self.__folded,
            "current_bet": self.__current_bet,
        }

    def __str__(self):
        return f"{self.get_name} tiene {self.get_chips} puntos."

    def voted_to_start(self):
        self.__voted_to_start = True

    def add_chips(self, chips: int):
        self.__chips += chips

    def remove_chips(self, chips: int):
        self.__chips -= chips

    def reset_hand(self):
        self.__hand = []

    def fold(self):
        self.__folded = True

    def add_card(self, card):
        self.__hand.append(card)

    def clear_hand(self):
        self.__hand = []

    def print_hand(self):
        print_cards_in_rows(self.__hand)

    def get_hand_ranking(self, board):
        value = value_of_hand(self.__hand, board)
        return get_hand_ranking_from_value(value)

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

    def get_folded(self):
        return self.__folded

    def set_folded(self, folded):
        self.__folded = folded

    def get_current_bet(self):
        return self.__current_bet

    def set_current_bet(self, current_bet):
        self.__current_bet = current_bet

    def get_has_played(self):
        return self.__has_played

    def set_has_played(self, has_played):
        self.__has_played = has_played

    def has_lost(self):
        return self.__has_lost

    def set_lost(self, has_lost):
        self.__has_lost = has_lost

    def has_voted(self):
        return self.__voted_to_start

    def set_voted(self, voted):
        self.__voted_to_start = voted
