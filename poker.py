from deck import *

# Helper for tests: string to card integer
rank_map = {r: i for i, r in enumerate([str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A'])}
suit_map = {'♣': 0, '♦': 1, '♥': 2, '♠': 3}

def str_to_card(s):
    """Convert strings like 'AS', '10♣' to integer 0-51."""
    suit_char = s[-1]
    rank_str = s[:-1]
    return suit_map[suit_char] * 13 + rank_map[rank_str]

def main():
    test_cards = [str_to_card(c) for c in ['A♠','2♠','3♠','4♠','5♠','K♦','K♣']]
    print("Category:", evalBoard(test_cards, [])[0], "Expected Category: 8")

if __name__ == "__main__":
    main()