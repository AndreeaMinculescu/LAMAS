import numpy as np
import random
class Agent:
  
    def __init__(self, cards, table):
        # cards is a list of 4 card objects 
        self.cards = cards
        # table is a list of 6 card objects on the table
        self.table = table

def greedy_strategy():
    """ 
    Find all common numbers (occurence more than once) in all the cards visible 
    to the agent (their cards and the cards on table) and then pick up the same 
    number from the pile on the table otherwise don't do anything. While 
    swapping, make sure you do not swap out any possible wanted cards. If there 
    are multiple common numbers to discard from agent's hand then choose a random 
    one to discard.
    """

    # TODO: adjust to andreea's swap code and agent env 

    card_values = [1,2,3,4]
    table_values = [8,6,12,12,11,6]

    all_values = card_values + table_values

    possible_wants_1 = sorted([value for value in all_values if all_values.count(value) > 1], reverse= True)
    possible_wants = []

    # first give priority to the wants which are in starting hand
    for want in possible_wants_1:
        if want in card_values:
            possible_wants.append(want)

    possible_wants.extend([i for i in possible_wants_1 if i not in possible_wants])

    print("Wanted cards: ", possible_wants)
    print("Cards on table: ", table_values)
    print("Cards in hand: ", card_values)
    print("------------------------------------")

    for want in possible_wants:
        print("Current wanted card: ", want)
        
        if want in table_values:

            discards = [value for value in card_values if card_values.count(value) == 1 and value not in possible_wants]

            if want in card_values:
                discards = [value for value in card_values if value != want and value not in possible_wants]

            if discards:
                swap = random.choice(discards)
                # the card number to swap is the var swap
                # the card number wanted is the var want
                idx1 = card_values.index(swap)
                idx2 = table_values.index(want)

                card_values[idx1] = want
                table_values[idx2] = swap

            else:
                print("Nothing to discard, current hand has wanted cards")
                return

        else:
            print(f"Skip {want} since not on table")

        print("Cards on table: ", table_values)
        print("Cards in hand: ", card_values)
        print()

# test
greedy_strategy()