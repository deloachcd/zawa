from enum import Enum

# String literal template constants for rendering the cards,
# they accept string.format() calls directly
HEARTS = r'''
.-----------.
| {}        |
|   _   _   |
|  / \_/ \  |
|  \     /  |
|   \   /   |
|    \ /    |
|     V     |
|        {} |
'-----------'
'''
DIAMONDS = r'''
.-----------.
| {}        |
|     .     |
|    / \    |
|   /   \   |
|   \   /   |
|    \ /    |
|     V     |
|        {} |
'-----------'
'''
CLUBS = r'''
.-----------.
| {}  _     |
|    / \    |
|  _ \_/ _  |
| / \_|_/ \ |
| \_/ | \_/ |
|     |     |
|    /_\    |
|        {} |
'-----------'
'''
SPADES = r'''
.-----------.
| {}  _     |
|    / \    |
|   /   \   |
|  /     \  |
| /  _ _  \ |
| \_/ | \_/ |
|    /_\    |
|        {} |
'-----------'
'''


class Suite(Enum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3


class Card:
    RENDER_SUITES = [HEARTS, DIAMONDS, CLUBS, SPADES]
    RENDER_VALUES = {
        11: "J",
        12: "Q",
        13: "K",
        14: "A"
    }

    def __init__(self, suite, value):
        if type(suite) is Suite:
            self.suite = suite.value
        else:
            self.suite = suite

        if value >= 2 and value <= 14:
            self.value = value

    def render(self):
        value = (str(self.value) if self.value >= 2 and self.value <= 10
                 else self.RENDER_VALUES[self.value])
        return self.RENDER_SUITES[self.suite].format(
            value.ljust(2), value.rjust(2)
        )

    def __str__(self):
        return f"Card(suite={self.suite} value={self.value})"

    def __repr__(self):
        return f"Card(suite={self.suite} value={self.value})"


def render_multiple_cards(cards, sep=' '):
    linesets = [
        card.render().split('\n') for card in cards
    ]
    return '\n'.join([
        sep.join([cardstr[line_index] for cardstr in linesets])
        for line_index in range(len(linesets[0]))
    ])


if __name__ == "__main__":
    import random

    DECK = [
        Card(suite, value) for value in range(2, 15)
        for suite in range(0, 4)
    ]
    random.shuffle(DECK)
    print(render_multiple_cards(list(DECK)[0:5]))
