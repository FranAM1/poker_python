SUITS = {
    'hearts': '♥',
    'diamonds': '♦',
    'clubs': '♣',
    'spades': '♠'
}

RANKS = {
    '1': 'A',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': '10',
    '11': 'J',
    '12': 'Q',
    '13': 'K'
}

def print_cards_in_rows(cards):
    cards_lines = [card.lines() for card in cards]
    
    for i in range(0, len(cards_lines), 5):
        for lines in zip(*cards_lines[i:i+5]):
            print(' '.join(lines))
        print()