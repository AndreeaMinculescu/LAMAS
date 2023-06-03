import operator
from collections import Counter

import numpy as np
import random
class Agent:
  
    def __init__(self, cards, table):
        # cards is a list of 4 card objects 
        self.cards = cards
        # table is a list of 6 card objects on the table
        self.table = table
        self.score = 0

    def check_kemps(self):
        if len(set([card.value for card in self.cards])) == 1:
            return 1
        return 0

    def greedy_strategy(self, verbose=1):
        """
        Find all common numbers (most occurances) in all the cards visible
        to the agent (their cards and the cards on table) and then pick up the same
        number from the pile on the table otherwise don't do anything. While
        swapping, make sure you do not swap out any possible wanted cards. If there
        are multiple common numbers to discard from agent's hand then choose a random
        one to discard.
        """

        # TODO: adjust to andreea's swap code and agent env

        # card_values = [6,2,11,3]
        # table_values = [8,7,12,12,11,7]
        card_list = self.cards
        table_list = self.table

        card_values = [card.value for card in self.cards]
        table_values = [card.value for card in self.table]

        all_cards = card_list + table_list
        all_values = [card.value for card in all_cards]
        most_freq = Counter(getattr(card, 'value') for card in all_cards)
        most_freq = max(most_freq.values())

        # most priority given to the cards which occur most frequently
        possible_wants_1 = sorted([card for card in all_cards if all_values.count(card.value) >= most_freq], key=operator.attrgetter('value'), reverse= True)
        possible_wants = []


        # first give priority to the wants which are in starting hand
        for want in possible_wants_1:
            if want in card_list:
                possible_wants.append(want)

        possible_wants.extend([i for i in possible_wants_1 if i not in possible_wants])

        print("Wanted cards: ", [(card.value, card.suit) for card in possible_wants])
        print("Cards on table: ", [(card.value, card.suit) for card in table_list])
        print("Cards in hand: ", [(card.value, card.suit) for card in card_list])
        print("------------------------------------")

        for want in possible_wants:
            if verbose:
                print("Current wanted card: ", (want.value, want.suit))

            if want in table_list:

                discards = [card for card in card_list if card_values.count(card.value) == 1 and card not in possible_wants]

                if want in card_list:
                    discards = [card for card in card_list if card != want and card not in possible_wants]

                if discards:
                    swap = random.choice(discards)
                    # the card number to swap is the var swap
                    # the card number wanted is the var want
                    idx1 = card_list.index(swap)
                    idx2 = table_list.index(want)

                    card_list[idx1] = want
                    table_list[idx2] = swap

                else:
                    if verbose:
                        print("Nothing to discard, current hand has wanted cards")
                        # return

            else:
                if verbose:
                    print(f"Skip {(want.value, want.suit)} since not on table")

            if verbose:
                print("Cards on table: ", [(card.value, card.suit) for card in table_list])
                print("Cards in hand: ", [(card.value, card.suit) for card in card_list])
                print()

        print("End of round - cards on table: ", [(card.value, card.suit) for card in table_list])
        print("End of round - cards in hand: ", [(card.value, card.suit) for card in card_list])
        self.cards = card_list
        self.table = table_list
