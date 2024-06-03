import unittest
from game.card import Card
from utils.poker_logic import (
    compare_hands,
    is_royal_flush,
    is_straight_flush,
    is_four_of_a_kind,
    is_full_house,
    is_flush,
    is_straight,
    is_three_of_a_kind,
    is_two_pair,
    is_one_pair,
    value_of_hand,
    get_hand_ranking_from_value,
)


class TestHand(unittest.TestCase):
    def test_royal_flush(self):
        hand = [
            Card("diamonds", "2"),
            Card("spades", "A"),
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("hearts", "A"),
        ]
        self.assertTrue(is_royal_flush(hand))

    def test_straight_flush(self):
        hand = [
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("hearts", "9"),
            Card("hearts", "8"),
            Card("hearts", "7"),
        ]
        self.assertTrue(is_straight_flush(hand))

    def test_four_of_a_kind(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "10"),
            Card("spades", "10"),
            Card("hearts", "9"),
            Card("hearts", "8"),
            Card("hearts", "7"),
        ]
        self.assertTrue(is_four_of_a_kind(hand))

    def test_full_house(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "10"),
            Card("spades", "9"),
            Card("hearts", "9"),
            Card("hearts", "8"),
            Card("hearts", "7"),
        ]
        self.assertTrue(is_full_house(hand))

    def test_flush(self):
        hand = [
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("hearts", "2"),
            Card("hearts", "8"),
            Card("hearts", "7"),
        ]
        self.assertTrue(is_flush(hand))

    def test_straight(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "J"),
            Card("clubs", "Q"),
            Card("spades", "K"),
            Card("hearts", "A"),
            Card("hearts", "8"),
            Card("hearts", "7"),
        ]
        self.assertTrue(is_straight(hand))

    def test_three_of_a_kind(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "10"),
            Card("spades", "K"),
            Card("hearts", "A"),
        ]
        self.assertTrue(is_three_of_a_kind(hand))

    def test_two_pair(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "10"),
            Card("spades", "K"),
            Card("hearts", "A"),
            Card("hearts", "8"),
            Card("hearts", "7"),
        ]
        self.assertTrue(is_two_pair(hand))

    def test_one_pair(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "K"),
            Card("spades", "Q"),
            Card("hearts", "A"),
            Card("hearts", "8"),
            Card("hearts", "7"),
        ]
        self.assertTrue(is_one_pair(hand))

    def test_high_card(self):
        VALUE_HIGH_CARD = 1
        hand = [
            Card("hearts", "7"),
            Card("clubs", "5"),
            Card("hearts", "10"),
            Card("diamonds", "2"),
            Card("clubs", "Q"),
            Card("spades", "3"),
            Card("hearts", "A"),
        ]
        self.assertEqual(VALUE_HIGH_CARD, value_of_hand(hand, []))

    def test_compare_best_hand(self):
        # generate 4 randoms hands and a board
        hand1 = [Card("spades", "Q"), Card("hearts", "A")]

        hand2 = [Card("hearts", "10"), Card("diamonds", "10")]

        hand3 = [Card("clubs", "K"), Card("spades", "K")]

        hand4 = [Card("hearts", "2"), Card("diamonds", "2")]

        board = [
            Card("spades", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("spades", "2"),
            Card("hearts", "2"),
        ]

        # compare the hands
        list_hands = [hand1, hand2, hand3, hand4]
        best_hand = hand4

        best_hands = compare_hands(list_hands, board)

        self.assertEqual(best_hand, best_hands[0])

    def test_compare_hands_with_tie(self):
        hand1 = [Card("clubs", "A"), Card("spades", "A")]

        hand2 = [Card("hearts", "K"), Card("diamonds", "K")]

        hand3 = [Card("clubs", "K"), Card("spades", "K")]

        hand4 = [Card("hearts", "3"), Card("diamonds", "4")]

        board = [
            Card("spades", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("spades", "2"),
            Card("hearts", "2"),
        ]

        list_hands = [hand1, hand2, hand3, hand4]
        best_hands = [hand2, hand3]

        result_hands = compare_hands(list_hands, board)

        self.assertEqual(best_hands, result_hands)

    def test_compare_hands_with_tie_in_board(self):
        hand1 = [Card("clubs", "8"), Card("spades", "7")]

        hand2 = [Card("hearts", "K"), Card("diamonds", "A")]

        hand3 = [Card("clubs", "5"), Card("spades", "A")]

        hand4 = [Card("hearts", "3"), Card("diamonds", "4")]

        board = [
            Card("spades", "10"),
            Card("diamonds", "J"),
            Card("hearts", "Q"),
            Card("spades", "2"),
            Card("hearts", "10"),
        ]

        list_hands = [hand1, hand2, hand3, hand4]
        best_hands = [hand2]

        print(get_hand_ranking_from_value(value_of_hand(hand2, board)))

        result_hands = compare_hands(list_hands, board)

        self.assertEqual(best_hands, result_hands)
