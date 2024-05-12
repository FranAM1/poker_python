from game import SUITS, RANKS
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
            format(self.get_rank(), ' <2'),
            format(self.get_suit_value(), ' <2'),
            format(self.get_rank(), ' >2')
        )
        return card
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.__suit == other.__suit and self.__rank == other.__rank
        return False
    
    def lines(self):
        return str(self).split('\n') 
    

    # MARK: - Getters and Setters
    
    def get_suit(self) -> str:
        return self.__suit
    
    def get_suit_value(self) -> int:
        return SUITS[self.__suit]
    
    def get_rank(self) -> str:
        return self.__rank
    
    def get_rank_value(self) -> int:
        return RANKS[self.__rank]
    
    def set_suit(self, suit: str):
        if suit not in SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        self.__suit = suit

    def set_rank(self, rank: str):
        if rank not in RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        self.__rank = rank