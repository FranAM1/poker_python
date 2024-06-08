from game.player import Player
from game.card import Card
from game import ROUND_STATE
from game.deck import Deck
from utils.poker_logic import compare_hands


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
    __winners: list[Player]

    def __init__(self):
        self.__players = []
        self.__board = []
        self.__winners = []
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

    def place_bet(self, player: Player, amount):
        """
        Place a bet for the current player.

        :param player: The player placing the bet.
        :param amount: The amount to bet.

        :return: False if the amount is less than the current bet or the player
        doesn't have enough chips to keep playing, True otherwise.
        """
        if amount >= self.__current_bet:
            player.remove_chips(amount)
            self.__pot += amount
            player.set_has_played(True)
            player.set_current_bet(amount)
            self.__current_bet = amount
            return True
        return False

    def next_round(self):
        if self.__round_stage == ROUND_STATE["Pre-flop"]:
            if self.all_players_all_in():
                self.deal_flop()
                self.deal_turn()
                self.deal_river()
                return self.determine_winner()
            self.__round_stage += 1
            self.deal_flop()
            self.reset_turn()
        elif self.__round_stage == ROUND_STATE["Flop"]:
            if self.all_players_all_in():
                self.__round_stage = ROUND_STATE["Pre-flop"]
                self.deal_turn()
                self.deal_river()
                return self.determine_winner()
            self.__round_stage += 1
            self.deal_turn()
            self.reset_turn()
        elif self.__round_stage == ROUND_STATE["Turn"]:
            if self.all_players_all_in():
                self.__round_stage = ROUND_STATE["Pre-flop"]
                self.deal_river()
                return self.determine_winner()
            self.__round_stage += 1
            self.deal_river()
            self.reset_turn()
        elif self.__round_stage == ROUND_STATE["River"]:
            self.__round_stage = ROUND_STATE["Pre-flop"]
            self.determine_winner()

    def all_players_all_in(self):
        active_players = [
            player for player in self.__players if not player.get_folded()
        ]
        return all(player.get_chips() == 0 for player in active_players)

    def determine_winner(self):
        active_players = [
            player for player in self.__players if not player.get_folded()
        ]

        hands = [player.get_hand() for player in active_players]

        best_hands = compare_hands(hands, self.__board)
        for player in active_players:
            if player.get_hand() in best_hands:
                self.__winners.append(player)

        self.distribute_pot(self.__winners)

    def deal_flop(self):
        self.__deck.deal_flop(self.__board)

    def deal_turn(self):
        self.__deck.deal_turn(self.__board)

    def deal_river(self):
        self.__deck.deal_river(self.__board)

    def remove_player(self, player):
        self.__players.remove(player)

    def reset_players_new_game(self):
        for player in self.__players:
            player.set_chips(100)
            player.set_lost(False)

    def add_vote_to_start(self):
        self.__votes_to_start += 1
        if self.__votes_to_start >= len(self.__players):
            self.start()

    def add_player(self, player):
        self.__players.append(player)

    def add_to_pot(self, amount):
        self.__pot += amount

    def reset_pot(self):
        """Reset the pot to zero."""
        self.__pot = 0

    def next_turn(self):
        active_players = [
            player for player in self.__players if not player.get_folded()
        ]
        if len(active_players) == 1:
            self.__winners.append(active_players[0])
            self.distribute_pot(self.__winners)
        else:
            self.__players_turn = (self.__players_turn + 1) % len(self.__players)
            while self.__players[self.__players_turn].get_folded():
                self.__players_turn = (self.__players_turn + 1) % len(self.__players)
            if self.__players_turn == 0:
                if self.all_active_players_have_bet():
                    self.next_round()

    def all_active_players_have_bet(self):
        return all(
            player.get_has_played() and player.get_current_bet() >= self.__current_bet
            for player in self.__players
            if not player.get_folded()
        )

    def get_current_player(self):
        return self.__players[self.__players_turn]

    def reset_turn(self):
        self.__players_turn = 0
        self.__current_bet = 0
        for player in self.__players:
            player.set_has_played(False)
            player.set_current_bet(0)
            player.set_folded(False)

    def reset_players_action(self):
        for player in self.__players:
            player.set_has_played(False)
            player.set_folded(False)
            player.reset_hand()
            player.set_current_bet(0)

    def reset_round(self):
        self.__players_turn = 0
        self.__current_bet = 0
        self.__winners = []
        self.__board = []
        self.reset_players_action()
        self.reset_pot()
        self.__deck.build_new_deck()
        self.__deck.shuffle()
        self.__deck.deal(self.__players)
        self.initial_bet()

    def initial_bet(self):
        """Make the initial bet."""
        initial_bet = 50

        for player in self.__players:
            if player.get_chips() >= initial_bet:
                player.remove_chips(initial_bet)
                self.add_to_pot(initial_bet)
            elif player.get_chips() > 0:
                self.add_to_pot(player.get_chips())
                player.set_chips(0)
            else:
                player.set_lost(True)

    def distribute_pot(self, winners):
        """Distribute the pot to the winner(s)."""
        if winners:
            winnings = self.__pot // len(winners)
            for winner in winners:
                winner.add_chips(winnings)

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

    def set_started(self, started):
        self.__started = started

    def reset_player_votes(self):
        self.__votes_to_start = 0

        for player in self.__players:
            player.set_voted(False)

    def get_votes_to_start(self):
        return self.__votes_to_start

    def set_votes_to_start(self, votes_to_start):
        self.__votes_to_start = votes_to_start

    def get_deck(self):
        return self.__deck

    def set_deck(self, deck):
        self.__deck = deck

    def get_players_turn(self):
        return self.__players_turn

    def set_players_turn(self, players_turn):
        self.__players_turn = players_turn

    def get_round_stage(self):
        return self.__round_stage

    def set_round_stage(self, round_stage):
        self.__round_stage = round_stage

    def get_current_bet(self):
        return self.__current_bet

    def set_current_bet(self, current_bet):
        self.__current_bet = current_bet

    def get_winners(self):
        return self.__winners

    def set_winners(self, winners):
        self.__winners = winners
