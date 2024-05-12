from game.player import Player
from game.card import Card

class Game():
    __players: list[Player]
    __board: list[Card]
    __pot: int

    def __init__(self):
        self.__players = []
        self.__board = []
        self.__pot = 0

    def add_player(self, player):
        self.players.append(player)

    def start(self):
        for player in self.players:
            player.play()

    
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