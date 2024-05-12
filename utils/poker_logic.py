from game import SUITS, RANKS, HANDS_RANKING

# Escalera real de color
def is_royal_flush(hand: list) -> bool:
    return is_straight_flush(hand) and hand[0].get_rank() == "10"

# Escalera de color
def is_straight_flush(hand: list) -> bool:
    return is_straight(hand) and is_flush(hand)

# Poker
def is_four_of_a_kind(hand: list) -> bool:
    ranks = [card.get_rank() for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 4:
            return True
    return False

# Full
def is_full_house(hand: list) -> bool:
    return is_three_of_a_kind(hand) and is_one_pair(hand)

# Color
def is_flush(hand: list) -> bool:
    suits = [card.get_suit() for card in hand]
    return len(set(suits)) == 1

# Escalera
def is_straight(hand: list) -> bool:
    ranks = [card.get_rank() for card in hand]
    ranks_values = [RANKS[rank] for rank in ranks]
    ranks_values.sort()
    return ranks_values == list(range(ranks_values[0], ranks_values[0] + 5))

# Trio
def is_three_of_a_kind(hand: list) -> bool:
    ranks = [card.get_rank() for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 3:
            return True
    return False

# Doble pareja
def is_two_pair(hand: list) -> bool:
    ranks = [card.get_rank() for card in hand]
    pairs = 0
    for rank in ranks:
        if ranks.count(rank) == 2:
            pairs += 1
    return pairs == 2

# Pareja
def is_one_pair(hand: list) -> bool:
    ranks = [card.get_rank() for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 2:
            return True
    return False

HAND_VALUES = {
    "royal_flush": is_royal_flush,
    "straight_flush": is_straight_flush,
    "four_of_a_kind": is_four_of_a_kind,
    "full_house": is_full_house,
    "flush": is_flush,
    "straight": is_straight,
    "three_of_a_kind": is_three_of_a_kind,
    "two_pair": is_two_pair,
    "one_pair": is_one_pair
}

def value_of_hand(hand:dict, board:dict):
    
    full_hand = hand + board
    value = "high_card"

    for hand_value, function in HAND_VALUES.items():
        if function(full_hand):
            value = hand_value
            break

    print(value)

    return HANDS_RANKING[value]


    