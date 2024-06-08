from game import SUITS, RANKS


# Escalera real de color
def is_royal_flush(hand: list) -> bool:
    if is_straight_flush(hand):
        ranks = [card.get_rank() for card in hand]
        royal_ranks = ["10", "J", "Q", "K", "A"]
        return all(rank in ranks for rank in royal_ranks)
    return False


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
    return any(suits.count(suit) >= 5 for suit in set(suits))


# Escalera
def is_straight(hand: list) -> bool:
    ranks = [card.get_rank() for card in hand]
    ranks_values = [RANKS[rank] for rank in ranks]
    ranks_values.sort()

    for i in range(len(ranks_values) - 4):
        if all(
            ranks_values[i + j] == ranks_values[i] + j for j in range(1, 5)
        ):
            return True
    return False
    


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
    for rank in set(ranks):
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
    "one_pair": is_one_pair,
}

HANDS_RANKING = {
    "royal_flush": 10,
    "straight_flush": 9,
    "four_of_a_kind": 8,
    "full_house": 7,
    "flush": 6,
    "straight": 5,
    "three_of_a_kind": 4,
    "two_pair": 3,
    "one_pair": 2,
    "high_card": 1,
}

HANDS_TRANSLATION = {
    "royal_flush": "Escalera real de color",
    "straight_flush": "Escalera de color",
    "four_of_a_kind": "Poker",
    "full_house": "Full",
    "flush": "Color",
    "straight": "Escalera",
    "three_of_a_kind": "Trio",
    "two_pair": "Doble pareja",
    "one_pair": "Pareja",
    "high_card": "Carta alta",
}


def value_of_hand(hand: list, board: list):

    full_hand = hand + board
    value = "high_card"

    # Logica para ordenar las claves de HAND_VALUES de mayor a menor para evitar
    # que una escalera de color se detecte como una escalera o que un full se detecte como un trio
    for hand_value in sorted(HAND_VALUES, key=lambda x: HANDS_RANKING[x], reverse=True):
        print(hand_value)
        if HAND_VALUES[hand_value](full_hand):
            value = hand_value
            break

    return HANDS_RANKING[value]


def get_hand_ranking_from_value(value: int):
    for hand, ranking in HANDS_RANKING.items():
        if ranking == value:
            return HANDS_TRANSLATION[hand]

    return None


def compare_hands(list_hands: list, board: list):
    best_hand = list_hands[0]
    best_value = value_of_hand(best_hand, board)

    tied_hands = [best_hand]

    for hand in list_hands[1:]:
        value = value_of_hand(hand, board)
        if value > best_value:
            best_hand = hand
            best_value = value
            tied_hands = [hand]
        elif value == best_value:
            tied_hands.append(hand)

    if len(tied_hands) > 1:
        return

    return tied_hands