from enum import Enum
import random
import pygame
# random.seed(40)


class Suits(Enum):
    CLUB = 0
    SPADE = 1
    HEART = 2
    DIAMOND = 3


class Card:
    """ Class that records information regarding a card """
    def __init__(self, suit, value):
        # suit is the suit of a card (can be club, spade, heart or diamond)
        self.suit = suit
        # value is the number of a card
        self.value = value
        # image is used for display purposes
        self.image = pygame.image.load('card_design/' + self.suit.name + '-' + str(self.value) + '.svg')
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.75), int(self.image.get_height()*0.75)))
        # lookup allocates the corresponding symbol for a suit
        self.lookup = {
            Suits.CLUB: '♣',
            Suits.SPADE: '♠',
            Suits.HEART: '♥',
            Suits.DIAMOND: '♦'
        }

    def __str__(self):
        return f'<{self.value}{self.lookup[self.suit]}>'

def print_arr_cards(arr_cards):
    return [(str(card.value) + card.lookup[card.suit]) for card in arr_cards]

class Deck:
    """ Class that records information regarding a deck of cards """
    def __init__(self):
        # cards is a list of cards to draw from
        self.cards = []
        # discarded is the list of discarded cards
        self.discarded = set()
        # table_cards is the list of cards currently on the table that agents can pick from during that round
        # cards + discarded + table_cards make up a full deck of cards (all 52 cards)
        self.table_cards = []
        for suit in Suits:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
        # all cards in a full deck (all 52 cards)
        self.whole_deck = self.cards[:]
        # shuffle cards
        random.shuffle(self.cards)

    def deal_table(self):
        """
        Deal table cards (cards players can pick from)
        :param self: the deck of cards
        :return: None
        """
        # add the cards currently on the table to the discarded pile
        self.discarded.update(self.table_cards)
        # update table cards
        if len(self.cards) >= 6:
            self.table_cards = [self.cards.pop() for _ in range(6)]
        # if no more cards to deal from, then get the discarded and shuffle
        else:
            self.cards.extend(self.discarded)
            random.shuffle(self.cards)
            self.table_cards = [self.cards.pop() for _ in range(6)]
            self.discarded = set()

    def deal_cards_player(self):
        """
        Deal player cards (cards in players' hands)
        :param self: the deck of cards
        :return: list of 4 cards or None
        """
        # if there are enough cards to deal from
        if len(self.cards) + len(self.discarded) >= 4:
            # if there are enough cards in the cards pile, then just draw the top 4 cards
            if len(self.cards) >= 4:
                return [self.cards.pop() for _ in range(4)]
            # if there are not not enough cards in the cards pile, then use the discarded pile and shuffle
            else:
                self.cards.extend(self.discarded)
                random.shuffle(self.cards)
                self.discarded = set()
                return [self.cards.pop() for _ in range(4)]
        # if there are no more cards to deal from, then return None
        else:
            return None
