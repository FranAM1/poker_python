SUITS = {
    'hearts': '♥',
    'diamonds': '♦',
    'clubs': '♣',
    'spades': '♠'
}

RANKS = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    '10': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

def print_cards_in_rows(cards):
    cards_lines = [card.lines() for card in cards]
    
    for i in range(0, len(cards_lines), 5):
        for lines in zip(*cards_lines[i:i+5]):
            print(' '.join(lines))
        print()