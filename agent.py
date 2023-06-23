import operator
from collections import Counter
from announcement import PublicAnnouncement, AnnouncementType
import random


class Agent:
    """ Class that stores an agent's knowledge (the user is also an agent) """

    def __init__(self, name, cards, table):
        # name is an identifier for the agent
        self.name = name
        # cards is a list of 4 card objects (cards in the agent's hand)
        self.cards = cards
        # table is a list of 6 card objects on the table
        self.table = table
        # score is the score of the agent (+1 for each Kemps)
        self.score = 0
        # kb is the knowledge base of the agent (keep track of which cards are in other players' hands and in the
        # discard pile
        self.kb = None
        # do_no_collect is a set recording all value of cards collected by the other players
        self.do_not_collect = set()

    def check_kemps(self):
        """
        Check if the agent has Kemps (i.e. 4 cards with the same value)
        :param self: the agent
        :return: True is Kemps, False otherwise
        """

        if len(set([card.value for card in self.cards])) == 1:
            self.score += 1
            return 1
        return 0

    def greedy_strategy(self, verbose=False, kb_based=False):
        """
        Find all common numbers (most occurances) in all the cards visible to the agent (their cards and the cards on
        table) and then pick up the same number from the pile on the table otherwise don't do anything. While
        swapping, make sure you do not swap out any possible wanted cards. If there are multiple common numbers to
        discard from agent's hand then choose a random one to discard.
        :param self: the agent
        :param verbose: if True, print extra information regarding the choices of the agent
        :param kb_based: if True, then the agent takes advantage of the information in the knowledge base
        :return: a list of announcements (i.e. agent moves)
        """

        def new_print(*val):
            nonlocal verbose
            if verbose:
                print(*val)

        print = new_print

        card_list = self.cards
        table_list = self.table
        announcements = []

        # find the values that appear most often
        all_cards = card_list + table_list
        all_values = [card.value for card in all_cards]
        most_freq = Counter(getattr(card, 'value') for card in all_cards)
        most_freq = max(most_freq.values())

        # most priority given to the cards which occur most frequently
        possible_wants = sorted([card for card in all_cards if all_values.count(card.value) >= most_freq],
                                key=operator.attrgetter('value'), reverse=True)

        print("Wanted cards: ", [(card.value, card.suit) for card in possible_wants])
        print("Cards on table: ", [(card.value, card.suit) for card in table_list])
        print("Cards in hand: ", [(card.value, card.suit) for card in card_list])
        print("------------------------------------")

        # if strategy kb based remove all cards in possible wants which agent thinks all other players might have
        if kb_based:
            possible_wants_values = sorted(list(set([card.value for card in possible_wants])), reverse=True)
            print("No collect list: ", list(self.do_not_collect))

            for value in possible_wants_values:
                print("Looking at value: ", value)

                if value in list(self.do_not_collect):
                    print("number in do not collect: ", value)
                    possible_wants = sorted([card for card in possible_wants if card.value != value],
                                            key=operator.attrgetter('value'), reverse=True)
                    print("New wanted cards: ", [(card.value, card.suit) for card in possible_wants])
                    continue

                if self.kb.check_players_have_number(value):
                    print("Both have value so removing ", value)
                    possible_wants = sorted([card for card in possible_wants if card.value != value],
                                            key=operator.attrgetter('value'), reverse=True)
                    print("New wanted cards: ", [(card.value, card.suit) for card in possible_wants])

        # get pairs of cards to pick from the table and discard from hand
        for want in possible_wants:
            print("Current wanted card: ", (want.value, want.suit))

            # if the wanted card is on table and not already in hand
            if want in table_list:
                # find cards that can be discarded (i.e. cards that do not occur enough times)
                # discards = [card for card in card_list if card not in possible_wants]
                most_freq_hand = max(Counter(getattr(card, 'value') for card in card_list).values())
                discards = []
                if most_freq_hand < most_freq:
                    discards = [card for card in card_list if card.value != want.value]

                # case 1: there are cards that can be discarded
                if discards:
                    # randomly choose a card to discard
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
                    self.kb.set_card_knowledge_of_individual(want, self)
                    self.kb.set_discard_knowledge(swap)

                # case 2: there are no cards to discard
                else:
                    print("Nothing to discard, current hand has wanted cards")

            # if the wanted card is already in hand, then do nowthing
            else:
                print(f"Skip {(want.value, want.suit)} since not on table")

            print("Cards on table: ", [(card.value, card.suit) for card in table_list])
            print("Cards in hand: ", [(card.value, card.suit) for card in card_list])
            print()

        print("End of round - cards on table: ", [(card.value, card.suit) for card in table_list])
        print("End of round - cards in hand: ", [(card.value, card.suit) for card in card_list])
        # update card list
        self.cards = card_list
        self.table = table_list

        return announcements

    def recieve_announcement(self, announcement):
        """
        Update knowledge base according to moves of other agents
        :param self: the agent
        :param announcement: an announcement (i.e. a move of an agent)
        :return: None
        """

        t = announcement.type
        sender = announcement.sender
        card = announcement.card

        # sender picked the card so no one else has it
        if t == AnnouncementType.PICKED:
            self.do_not_collect.add(card.value)
            self.kb.set_card_knowledge_of_individual(card, sender)

        # sender discarded the card so the sender does not have it
        # if card on table then no one has it
        if t == AnnouncementType.DISCARDED:
            self.do_not_collect.discard(card.value)
            self.kb.set_discard_knowledge(card)

        # sender has a Kemps, so the cards involved in that Kemps cannot be collected by the agent
        if t == AnnouncementType.KEMPS:
            self.do_not_collect.add(card.value)