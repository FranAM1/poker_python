from game.player import Player
from game.card import Card
from game import ROUND_STATE
from game.deck import Deck


class Game:
    __players: list[Player]
    __board: list[Card]
    __pot: int
    __started: bool
    __votes_to_start: int
    __deck: Deck
    __players_turn: int
    __round_stage: int
    __current_bet: int

    def __init__(self):
        self.__players = []
        self.__board = [Card]
        self.__pot = 0
        self.__started = False
        self.__votes_to_start = 0
        self.__deck = Deck()
        self.__players_turn = 0
        self.__round_stage = 0
        self.__current_bet = 0

    def start(self):
        if len(self.__players) > 1 and self.__votes_to_start >= len(self.__players):
            self.__started = True
            print("Juego iniciado!")
            self.reset_round()
        else:
            print("No se puede iniciar la partida. Faltan jugadores o votos.")

    def place_bet(self, player, amount):
        """
        Place a bet for the current player.

        :param player: The player placing the bet.
        :param amount: The amount to bet.

        :return: False if the amount is less than the current bet or the player
        doesn't have enough chips, True otherwise.
        """
        player_chips = player.get_chips()
        if amount < self.__current_bet:
            return False
        else:
            self.add_to_pot(amount)
            player.remove_chips(amount)
            self.__current_bet = amount
            return True

    def next_round(self):
        if self.__round_stage == ROUND_STATE["Pre-flop"]:
            self.__round_stage += 1
            self.deal_flop()
        elif self.__round_stage == ROUND_STATE["Flop"]:
            self.__round_stage += 1
            self.deal_turn()
        elif self.__round_stage == ROUND_STATE["Turn"]:
            self.__round_stage += 1
            self.deal_river()
        elif self.__round_stage == ROUND_STATE["River"]:
            self.__round_stage = ROUND_STATE["Pre-flop"]
            self.determine_winner()
            self.reset_round()

    def check_next_round(self):
        if all(
            player.get_current_bet() == self.__current_bet for player in self.__players
        ):
            self.next_round()

    def add_vote_to_start(self):
        self.__votes_to_start += 1

    def add_player(self, player):
        self.__players.append(player)

    def add_to_pot(self, amount):
        self.__pot += amount

    def reset_pot(self):
        """Reset the pot to zero."""
        self.__pot = 0

    def next_turn(self):
        self.__players_turn = (self.__players_turn + 1) % len(self.__players)

    def get_current_player(self):
        return self.__players[self.__players_turn]

    def reset_round(self):
        """Reset the board and the players' hands."""
        self.__board = []
        for player in self.__players:
            player.reset_hand()
        self.__deck.build_new_deck()
        self.__deck.shuffle()
        self.__deck.deal(self.__players)
        self.initial_bet()

    def initial_bet(self):
        """Make the initial bet."""
        initial_bet = 50

        for player in self.__players:
            player.remove_chips(initial_bet)
            self.add_to_pot(initial_bet)

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

    def get_votes_to_start(self):
        return self.__votes_to_start

    def set_votes_to_start(self, votes_to_start):
        self.__votes_to_start = votes_to_start

    def get_deck(self):
        return self.__deck

    def set_deck(self, deck):
        self.__deck = deck
