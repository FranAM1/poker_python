from . import SUITS, RANKS
class Card:
    __suit: str
    __rank: str

    def __init__(self, suit: str, rank: str):
        self.set_suit(suit)
        self.set_rank(rank)

    def __str__(self) -> str:
        card = (
        '┌─────────┐\n'
        '│ {}      │\n'
        '│         │\n'
        '│    {}   │\n'
        '│         │\n'
        '│      {} │\n'
        '└─────────┘\n'
        ).format(
            format(self.__rank, ' <2'),
            format(self.__suit, ' <2'),
            format(self.__rank, ' >2')
        )
        return card
    
    def lines(self):
        return str(self).split('\n')  
    
    def get_suit(self) -> str:
        return self.__suit
    
    def get_rank(self) -> str:
        return self.__rank
    
    def set_suit(self, suit: str):
        if suit not in SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        self.__suit = SUITS[suit]

    def set_rank(self, rank: str):
        if rank not in RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        self.__rank = RANKS[rank]