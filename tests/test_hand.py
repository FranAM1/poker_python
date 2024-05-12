import unittest
from game.card import Card
from utils.poker_logic import compare_hands, is_royal_flush, is_straight_flush, is_four_of_a_kind, is_full_house, is_flush, is_straight, is_three_of_a_kind, is_two_pair, is_one_pair, value_of_hand

class TestHand(unittest.TestCase):
    def test_royal_flush(self):
        hand = [
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("hearts", "A")
        ]
        self.assertTrue(is_royal_flush(hand))

    def test_not_royal_flush(self):
        hand = [
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("hearts", "2")
        ]
        self.assertFalse(is_royal_flush(hand))

    def test_straight_flush(self):
        hand = [
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("hearts", "9")
        ]
        self.assertTrue(is_straight_flush(hand))

    def test_not_straight_flush(self):
        hand = [
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("hearts", "2")
        ]
        self.assertFalse(is_straight_flush(hand))

    def test_four_of_a_kind(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "10"),
            Card("spades", "10"),
            Card("hearts", "9")
        ]
        self.assertTrue(is_four_of_a_kind(hand))

    def test_not_four_of_a_kind(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "10"),
            Card("spades", "9"),
            Card("hearts", "9")
        ]
        self.assertFalse(is_four_of_a_kind(hand))

    def test_full_house(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "10"),
            Card("spades", "9"),
            Card("hearts", "9")
        ]
        self.assertTrue(is_full_house(hand))

    def test_not_full_house(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "10"),
            Card("spades", "9"),
            Card("hearts", "8")
        ]
        self.assertFalse(is_full_house(hand))

    def test_flush(self):
        hand = [
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("hearts", "2")
        ]
        self.assertTrue(is_flush(hand))

    def test_not_flush(self):
        hand = [
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("spades", "2")
        ]
        self.assertFalse(is_flush(hand))

    def test_straight(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "J"),
            Card("clubs", "Q"),
            Card("spades", "K"),
            Card("hearts", "A")
        ]
        self.assertTrue(is_straight(hand))

    def test_not_straight(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "J"),
            Card("clubs", "Q"),
            Card("spades", "K"),
            Card("hearts", "2")
        ]
        self.assertFalse(is_straight(hand))

    def test_three_of_a_kind(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "10"),
            Card("spades", "K"),
            Card("hearts", "A")
        ]
        self.assertTrue(is_three_of_a_kind(hand))

    def test_not_three_of_a_kind(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "4"),
            Card("clubs", "10"),
            Card("spades", "K"),
            Card("hearts", "9")
        ]
        self.assertFalse(is_three_of_a_kind(hand))

    def test_two_pair(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "K"),
            Card("spades", "K"),
            Card("hearts", "A")
        ]
        self.assertTrue(is_two_pair(hand))

    def test_not_two_pair(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "K"),
            Card("spades", "Q"),
            Card("hearts", "A")
        ]
        self.assertFalse(is_two_pair(hand))

    def test_one_pair(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "10"),
            Card("clubs", "K"),
            Card("spades", "Q"),
            Card("hearts", "A")
        ]
        self.assertTrue(is_one_pair(hand))

    def test_not_one_pair(self):
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "3"),
            Card("clubs", "K"),
            Card("spades", "Q"),
            Card("hearts", "9")
        ]
        self.assertFalse(is_one_pair(hand))

    def test_high_card(self):
        VALUE_HIGH_CARD= 1
        hand = [
            Card("hearts", "10"),
            Card("diamonds", "2"),
            Card("clubs", "Q"),
            Card("spades", "3"),
            Card("hearts", "A")
        ]
        self.assertEqual(VALUE_HIGH_CARD, value_of_hand(hand, []))
        
    def test_compare_best_hand(self):
        #generate 4 randoms hands and a board
        hand1 = [
            Card("spades", "Q"),
            Card("hearts", "A")
        ]

        hand2 = [
            Card("hearts", "10"),
            Card("diamonds", "10")
        ]

        hand3 = [
            Card("clubs", "K"),
            Card("spades", "K")
        ]

        hand4 = [
            Card("hearts", "2"),
            Card("diamonds", "2")
        ]

        board = [
            Card("spades", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("spades", "2"),
            Card("hearts", "2")
        ]

        #compare the hands
        list_hands = [hand1, hand2, hand3, hand4]
        best_hand = hand4
        

        self.assertEqual(best_hand, compare_hands(list_hands, board))