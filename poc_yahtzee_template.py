"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    if len(hand) == 0:
        return 0

    scores = {}
    for die in hand:
        if scores.has_key(die):
            scores[die] += die
        else:
            scores[die] = die
     
    return max(scores.values())


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    outcomes = [(die + 1) for die in range(num_die_sides)]
    sequences = gen_all_sequences(outcomes, num_free_dice)
    sum_scores = sum([score(held_dice + hand) for hand in sequences])
    return (1.0 * sum_scores / len(sequences))


def all_subsets_recur(left, current_subset, accumulator):
    """
    Recursive helper for all_subsets
    builds binary recurse tree where leaves are subsets we're interested in
    """
    if len(left) == 0:
        # at a leaf, where subsets we're interest reside
        accumulator.append(current_subset)
    else:
        # recursively build all subsets that have 1st element of left in them
        all_subsets_recur(left[1:], [left[0]] + current_subset, accumulator)
        # recursively build all subsets that do NOT have 1st element of left in them
        all_subsets_recur(left[1:], current_subset, accumulator)

def all_subsets(items):
    """
    returns all subsets of items
    if items is not a set, the result will not be either
    """
    accumulator = []
    all_subsets_recur(items, [], accumulator)
    return accumulator


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    subsets = all_subsets(hand)
    tuple_subsets = [tuple(sorted(subset)) for subset in subsets]
    return set(tuple_subsets)


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    best_hold = (0.0, ())
    holds = gen_all_holds(hand)
    for hold in holds:
        e_val = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if e_val > best_hold[0]:
            best_hold = (e_val, hold)

    return best_hold


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 6, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
