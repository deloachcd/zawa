from enum import Enum


# String literal template constants for rendering the cards,
# they accept string.format() calls directly
HEARTS = r'''
.-----------.
|{2} {0}        {3}|
|{2}   _   _   {3}|
|{2}  / \_/ \  {3}|
|{2}  \     /  {3}|
|{2}   \   /   {3}|
|{2}    \ /    {3}|
|{2}     V     {3}|
|{2}        {1} {3}|
'-----------'
'''
DIAMONDS = r'''
.-----------.
|{2} {0}        {3}|
|{2}     .     {3}|
|{2}    / \    {3}|
|{2}   /   \   {3}|
|{2}   \   /   {3}|
|{2}    \ /    {3}|
|{2}     V     {3}|
|{2}        {1} {3}|
'-----------'
'''
CLUBS = r'''
.-----------.
| {0}{2}  _     {3}|
|{2}    / \    {3}|
|{2}  _ \_/ _  {3}|
|{2} / \_|_/ \ {3}|
|{2} \_/ | \_/ {3}|
|{2}     |     {3}|
|{2}    /_\    {3}|
|        {0} |
'-----------'
'''
SPADES = r'''
.-----------.
| {0}{2}  _     {3}|
|{2}    / \    {3}|
|{2}   /   \   {3}|
|{2}  /     \  {3}|
|{2} /  _ _  \ {3}|
|{2} \_/ | \_/ {3}|
|{2}    /_\    {3}|
|        {0} |
'-----------'
'''


class TermColors:
    NORMAL = '\033[m'
    RED = '\033[31m'


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
        suite_color = (TermColors.RED if self.suite < 2
                       else TermColors.NORMAL)
        return self.RENDER_SUITES[self.suite].format(
            value.ljust(2), value.rjust(2), suite_color,
            TermColors.NORMAL
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
