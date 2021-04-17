# We need 6 bits to fit a big enough value for each ranked hand's state
STATE_BITWIDTH = 6
HAND_MASK = int('111111', 2)

# Bitmasks for determining the state of a hand from its hash
# with bitwise "AND".
SFLUSH_MASK = HAND_MASK << (STATE_BITWIDTH*8)
FOURKIND_MASK = HAND_MASK << (STATE_BITWIDTH*7)
FHOUSE_MASK = HAND_MASK << (STATE_BITWIDTH*6)
FLUSH_MASK = HAND_MASK << (STATE_BITWIDTH*5)
STRAIGHT_MASK = HAND_MASK << (STATE_BITWIDTH*4)
THREEKIND_MASK = HAND_MASK << (STATE_BITWIDTH*3)
TWOPAIR_MASK = HAND_MASK << (STATE_BITWIDTH*2)
ONEPAIR_MASK = HAND_MASK << STATE_BITWIDTH
HIGHCARD_MASK = HAND_MASK


def _resolve_sflush(card_hash):
    if (card_hash & STRAIGHT_MASK > 0) and (card_hash & FLUSH_MASK > 0):
        return card_hash & HIGHCARD_MASK


def _resolve_fhouse(card_hash):
    pair_adj, three_adj = 0, 0
    if (card_hash & THREEKIND_MASK > 0) and (card_hash & TWOPAIR_MASK > 0):
        pair_adj = (card_hash & TWOPAIR_MASK) >> (STATE_BITWIDTH*2)
        three_adj = (card_hash & THREEKIND_MASK) >> (STATE_BITWIDTH*3)
    elif (card_hash & THREEKIND_MASK > 0) and (card_hash & ONEPAIR_MASK > 0):
        pair_adj = (card_hash & ONEPAIR_MASK) >> STATE_BITWIDTH
        three_adj = (card_hash & THREEKIND_MASK) >> (STATE_BITWIDTH*3)

    return pair_adj + three_adj


def _resolve_flush(sorted_cards):
    ''' returns the value of the highest card in the flush
        (if there is a flush) '''
    rval = 0
    for i in range(0, len(sorted_cards)-4):
        if sorted_cards[i].suite == sorted_cards[i+4].suite:
            rval = sorted(sorted_cards[i:i+5],
                          key=(lambda card: card.value))[-1]

    return rval


def _resolve_4kind(sorted_cards):
    ''' returns the value of the card there are 4 of in the hand
        (if there are 4 of any card), plus the remaining cards
        after stripping the ones there are 4 of a kind of '''
    for i in range(0, len(sorted_cards)-3):
        if sorted_cards[i].value == sorted_cards[i+3].value:
            remaining_cards = sorted_cards[:i] + sorted_cards[i+4:]
            return (sorted_cards[i].value, remaining_cards)

    return (0, sorted_cards)


def _resolve_3kind(sorted_cards):
    ''' returns the value of the card there are 3 of in the hand
        (if there are 3 of any card) '''
    for i in range(0, len(sorted_cards)-2):
        if sorted_cards[i].value == sorted_cards[i+2].value:
            remaining_cards = sorted_cards[:i] + sorted_cards[i+3:]
            return (sorted_cards[i].value, remaining_cards)

    return (0, sorted_cards)


def _resolve_pair(sorted_cards):
    ''' returns the value of the lowest (or only) pair remaining
        in the set of cards '''
    for card, i in enumerate(sorted_cards[:-1]):
        if card.value == sorted_cards[i+1].value:
            remaining_cards = sorted_cards[:i] + sorted_cards[i+2:]
            return (card.value, remaining_cards)
    return (0, sorted_cards)


def _resolve_highcard(sorted_cards):
    ''' returns the highest single card value '''
    return sorted_cards[-1]


def _resolve_straight(sorted_cards):
    if sorted_cards[-1] == 14:
        # we have an ace, which can act as 1 or 14
        fake_card = type('', (), {'value': 1})()
        straight_cards = [fake_card] + sorted_cards

    i = 0
    len_seq = 1
    while i < len(straight_cards)-1:
        while straight_cards[i].value+1 == straight_cards[i+1].value:
            len_seq += 1
            i += 1
            if len_seq == 5:
                # return highest value in straight
                return straight_cards[i+1].value
        len_seq = 1
        i += 1
    return 0


def resolve_hand(cards):
    ''' hash the hand into a 64-bit value which can be numerically
        compared against other hands to see which one wins '''
    value_ordered_cards = sorted(cards, key=(lambda card: card.value))
    suite_ordered_cards = sorted(cards, key=(lambda card: card.suite))

    # First, check if there are any flushes in the deck before we remove cards
    # from either collection
    card_hash = _resolve_flush(suite_ordered_cards) << (STATE_BITWIDTH*5)

    # Add the value of the high card into its 6-bit wide "slot"
    card_hash += _resolve_highcard(value_ordered_cards)

    # Add the value of the highest card in the straight into its "slot"
    card_hash += _resolve_straight(value_ordered_cards) << (STATE_BITWIDTH*4)

    # Add the value of the card there is 4 of a kind of, and return
    # the collection of cards with those cards removed
    resolution = _resolve_4kind(value_ordered_cards)
    card_hash += resolution[0] << (STATE_BITWIDTH*7)
    value_ordered_cards = resolution[1]

    # Add the value of the card there is 3 of a kind of, and return
    # the collection of cards with those cards removed
    resolution = _resolve_3kind(value_ordered_cards)
    card_hash += resolution[0] << (STATE_BITWIDTH*3)
    value_ordered_cards = resolution[1]

    # Add the value of the lowest pair we can find remaining into the
    # "1 pair" slot, and return the collection of remaining cards
    resolution = _resolve_pair(value_ordered_cards)
    card_hash += resolution[0] << STATE_BITWIDTH
    value_ordered_cards = resolution[1]

    # Add the value of the lowest pair we can find remaining into the
    # "2 pair" slot, and return the collection of remaining cards
    resolution = _resolve_pair(value_ordered_cards)
    card_hash += resolution[0] << (STATE_BITWIDTH*2)
    value_ordered_cards = resolution[1]

    # Check the card's hash for a full house
    card_hash += _resolve_fhouse(card_hash) << (STATE_BITWIDTH*6)

    # Check the card's hash for a straight flush
    card_hash += _resolve_sflush(card_hash) << (STATE_BITWIDTH*8)

    # The hash now contains everything you need to know about what hands
    # the set of cards has
    return card_hash
