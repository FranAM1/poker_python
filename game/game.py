from game.player import Player
from game.card import Card
from game.deck import Deck

class Game():
    __players: list[Player]
    __board: list[Card]
    __pot: int
    __started: bool
    __votes_to_start: int
    __deck: Deck

    def __init__(self):
        self.__players = []
        self.__board = [Card]
        self.__pot = 0
        self.__started = False
        self.__votes_to_start = 0
        self.__deck = Deck()

    def start(self):
        if (len(self.__players) > 1 and 
            self.__votes_to_start >= len(self.__players)
        ):
            self.__started = True
            print("Juego iniciado!")
            self.__deck.build_new_deck()
        else:
            print("No se puede iniciar la partida. Faltan jugadores o votos.")

    def add_vote_to_start(self):
        self.__votes_to_start += 1

    def add_player(self, player):
        self.__players.append(player)

    def add_to_pot(self, amount):
        self.__pot += amount

    def reset_pot(self):
        """Reset the pot to zero."""
        self.__pot = 0

    def distribute_pot(self, winners):
        """Distribute the pot to the winner(s)."""
        if winners:
            winnings = self.__pot // len(winners)
            for winner in winners:
                winner.add_chips(winnings)
            
            self.reset_pot()

    
    # MARK: - Getters and Setters
    def get_players(self):
        return self.__players
    
    def set_players(self, players):
        self.__players = players

    def get_board(self):
        return self.__board
    
    def set_board(self, board):
        self.__board = board

    def get_pot(self):
        return self.__pot
    
    def set_pot(self, pot):
        self.__pot = pot

    def has_started(self):
        return self.__started
    
    def has_started(self):
        return self.__started
    
    def get_votes_to_start(self):
        return self.__votes_to_start
    
    def set_votes_to_start(self, votes_to_start):
        self.__votes_to_start = votes_to_start

    def get_deck(self):
        return self.__deck
    
    def set_deck(self, deck):
        self.__deck = deck
    
    