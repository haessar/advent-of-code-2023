"""
--- Day 7: Camel Cards ---

Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

    32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
    KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
"""
from collections import Counter, defaultdict

with open('input/day_7.txt', 'r') as f:
    data = f.read().splitlines()

cards_by_type = defaultdict(list)
bids = {}

sort_order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


def assign_cards_by_type(cards, cards_by_type, dummy_cards=None):
    if not dummy_cards:
        dummy_cards = cards
    uniq = len(set(dummy_cards))
    if uniq == 5:
        cards_by_type['high_card'].append(cards)
    elif uniq == 4:
        cards_by_type['one_pair'].append(cards)
    elif uniq == 3:
        if max(Counter(dummy_cards).values()) == 2:
            cards_by_type['two_pair'].append(cards)
        else:
            cards_by_type['three_of_a_kind'].append(cards)
    elif uniq == 2:
        if max(Counter(dummy_cards).values()) == 3:
            cards_by_type['full_house'].append(cards)
        else:
            cards_by_type['four_of_a_kind'].append(cards)
    elif uniq == 1:
        cards_by_type['five_of_a_kind'].append(cards)


def calc_total_winnings(bids, cards_by_type, sort_order):
    rank = 1
    total_winnings = 0
    for type in ['high_card', 'one_pair', 'two_pair', 'three_of_a_kind', 'full_house', 'four_of_a_kind', 'five_of_a_kind']:
        for hand in sorted(cards_by_type[type], key=lambda cards: [sort_order.index(c) for c in cards], reverse=True):
            total_winnings += bids[hand] * rank
            rank += 1
    return total_winnings


for hand in data:
    cards, bid = hand.split()
    bids[cards] = int(bid)
    assign_cards_by_type(cards, cards_by_type)

print(calc_total_winnings(bids, cards_by_type, sort_order))


"""
--- Part Two ---

To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
    KK677 is now the only two pair, making it the second-weakest hand.
    T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.

With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""

cards_by_type = defaultdict(list)

sort_order = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

for hand in data:
    cards, _ = hand.split()
    if set(cards) != {"J"}:
        dummy_cards = cards.replace("J", Counter(cards.replace("J", "")).most_common(1)[0][0])
    else:
        dummy_cards = cards.replace("J", "A")
    assign_cards_by_type(cards, cards_by_type, dummy_cards)

print(calc_total_winnings(bids, cards_by_type, sort_order))
