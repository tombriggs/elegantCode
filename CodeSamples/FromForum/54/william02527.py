def same_suit(hand): # or flush
    return (len(set(hand[1::2])) == 1)

def royal_flush(hand):
    return (sorted(hand[::2]) == ['A', 'J', 'K', 'Q', 'T'] and same_suit(hand))

def straight(hand): # to check for straight flush, use same_suit(hand) together
    return ("".join(sorted(hand[::2])) in "123456789AJKQT")

def values_count(hand):
    values = sorted(hand[::2])
    values_set = list(set(values))
    counts = []
    for value in values_set:
        counts = counts + ["".join([str(values.count(value)), ' of ', value, ';'])]
    return ("".join(counts))

def high_card(counts1, counts2): # check if player2/counts2 is higher
    for d, r in zip(['T', 'J', 'Q', 'K', 'A'], ['V', 'W', 'X', 'Y', 'Z']): # enable comparison and sorting with string
        counts1 = counts1.replace(d, r)
        counts2 = counts2.replace(d, r)
    counts1 = counts1.split(";")
    counts2 = counts2.split(";")
    a = sorted([x for x in counts1 if x not in counts2])
    b = sorted([x for x in counts2 if x not in counts1])
    return int(a[-1] < b[-1])


with open("0054_poker.txt") as f:
    hands = [x.split(' ') for x in f.read().splitlines()]

def test_hands(hands): # must test hand as joined string
    wins = np.zeros(1000)
    
    for i in range(len(hands)):
        p1 = "".join(hands[i][:5])
        p2 = "".join(hands[i][5:])
        if True in [royal_flush(p1), royal_flush(p2)]: # check for royal flush
            wins[i] = [royal_flush(p1), royal_flush(p2)].index(True) + 1
            continue
        sf = [(straight(p1) and same_suit(p1)), (straight(p2) and same_suit(p2))]
        if True in sf: # straight flush
            wins[i] = sf.index(True) + 1
            continue
        four_of_a_kind = ["4 of " in values_count(p1), "4 of " in values_count(p2)]
        if True in four_of_a_kind:
            print("four of a kind") # no four of a kind case, skip coding
            continue
        fh = [("3 of" in values_count(p1) and "2 of" in values_count(p1)), ("3 of" in values_count(p2) and "2 of" in values_count(p2))]
        if True in fh: # full house
            if sum(fh) == 2:
                print("double full house") # no such case, skip coding
            else:
                 wins[i] = fh.index(True) + 1
            continue
        if True in [same_suit(p1), same_suit(p2)]: # flush
            wins[i] = [same_suit(p1), same_suit(p2)].index(True) + 1
            continue
        if True in [straight(p1), straight(p2)]: # straight
            if sum([straight(p1), straight(p2)]) == 2:
                wins[i] = high_card(values_count(p1), values_count(p2)) + 1
            else:
                wins[i] = [straight(p1), straight(p2)].index(True) + 1
            continue
        three_of_a_kind = ["3 of " in values_count(p1), "3 of " in values_count(p2)]
        if True in three_of_a_kind:
            if sum(three_of_a_kind) == 2:
                print("double three of a kind") # no such case, skip coding
            else:
                 wins[i] = three_of_a_kind.index(True) + 1
            continue
        tp = [values_count(p1).count("2 of") == 2, values_count(p2).count("2 of") == 2]
        if True in tp:
            if sum(tp) == 2:
                print("double two pairs") # no such case
            else:
                wins[i] = tp.index(True) + 1
            continue
        op = [values_count(p1).count("2 of") == 1, values_count(p2).count("2 of") == 1]
        if True in op:
            if sum(op) == 2:
                wins[i] = high_card(values_count(p1), values_count(p2)) + 1
            else:
                wins[i] = op.index(True) + 1
            continue
        wins[i] = high_card(values_count(p1), values_count(p2)) + 1
    return (wins)

wins = test_hands(hands)
print((wins == 1).sum())
