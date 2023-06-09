import operator
from collections import Counter
from knowledge_base import KnowledgeBase
from announcement import PublicAnnouncement, AnnouncementType
import numpy as np
import random

class Agent:
  
    def __init__(self, name, cards, table):
        self.name = name
        # cards is a list of 4 card objects 
        self.cards = cards
        # table is a list of 6 card objects on the table
        self.table = table
        self.score = 0
        self.kb = None
        
    def check_kemps(self):
        if len(set([card.value for card in self.cards])) == 1:
            self.score += 1
            return 1
        return 0

    def greedy_strategy(self, verbose=False, kb_based=False):
        """
        Find all common numbers (most occurances) in all the cards visible
        to the agent (their cards and the cards on table) and then pick up the same
        number from the pile on the table otherwise don't do anything. While
        swapping, make sure you do not swap out any possible wanted cards. If there
        are multiple common numbers to discard from agent's hand then choose a random
        one to discard.
        """
        card_list = self.cards
        table_list = self.table
        announcements = []

        card_value = [card.value for card in self.cards]

        all_cards = card_list + table_list
        all_values = [card.value for card in all_cards]
        most_freq = Counter(getattr(card, 'value') for card in all_cards)
        most_freq = max(most_freq.values())

        # most priority given to the cards which occur most frequently
        possible_wants_1 = sorted([card for card in all_cards if all_values.count(card.value) >= most_freq], key=operator.attrgetter('value'), reverse= True)
        possible_wants = []

        # first give priority to the wanted cards number on table which are also in starting hand
        for want in possible_wants_1:
            if want in card_list:
                possible_wants.append(want)

        possible_wants.extend([i for i in possible_wants_1 if i not in possible_wants])
        possible_wants = sorted([card for card in possible_wants], key=operator.attrgetter('value'), reverse=True)

        print("Wanted cards: ", [(card.value, card.suit) for card in possible_wants])
        print("Cards on table: ", [(card.value, card.suit) for card in table_list])
        print("Cards in hand: ", [(card.value, card.suit) for card in card_list])
        print("------------------------------------")

        # if strategy kb based remove all cards in possible wants which agent thinks all other players might have
        if kb_based:
            possible_wants_values = sorted(list(set([card.value for card in possible_wants])), reverse=True)

            for value in possible_wants_values:
                print("Looking at value: ", value)
                # print(self.kb)
                if self.kb.check_players_have_number(value) :
                    print("Both have value so removing ", value )
                    possible_wants = sorted([card for card in possible_wants if card.value != value], key=operator.attrgetter('value'), reverse=True)
                    print("New wanted cards: ", [(card.value, card.suit) for card in possible_wants])

        for want in possible_wants:
            if verbose:
                print("Current wanted card: ", (want.value, want.suit))

            if want in table_list:

                discards = [card for card in card_list if card_value.count(card.value) < most_freq
                            and card not in possible_wants]

                if want in card_list:
                    discards = [card for card in card_list if card != want and card not in possible_wants]

                if discards:
                    swap = random.choice(discards)
                    # swap cards from hand to table
                    idx1 = card_list.index(swap)
                    idx2 = table_list.index(want)
                    card_list[idx1] = want
                    table_list[idx2] = swap

                    # make public announcement
                    announcements.append(PublicAnnouncement(self, want, AnnouncementType.PICKED))
                    announcements.append(PublicAnnouncement(self, swap, AnnouncementType.DISCARDED))
                    
                    # update own knowledge base
                    # print(f"before updating {self.name} kb: {self.kb}")                                                          
                    self.kb.set_card_knowledge_of_individual(want, self)
                    self.kb.set_discard_knowledge(swap, self)
                    # print(f"after updating {self.name} kb: {self.kb}")

                else:
                    if verbose:
                        print("Nothing to discard, current hand has wanted cards")

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

        return announcements


    def recieve_announcement(self, announcement):

        t = announcement.type
        sender = announcement.sender
        card = announcement.card
        if t == AnnouncementType.PICKED:
            # sender picked the card so no one else has it
            self.kb.set_card_knowledge_of_individual(card, sender)

        if t == AnnouncementType.DISCARDED:
            # sender discarded the card so the sender does not have it
            # if card on table then no one has it
            self.kb.set_discard_knowledge(card, sender)
        
    def check_strategies(players):
        pass
