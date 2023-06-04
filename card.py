from enum import Enum
import random
import pygame


class Suits(Enum):
    CLUB = 0
    SPADE = 1
    HEART = 2
    DIAMOND = 3


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.image = pygame.image.load('card_design/' + self.suit.name + '-' + str(self.value) + '.svg')
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.75), int(self.image.get_height()*0.75)))

    def __str__(self):
        return f'{self.suit}, {self.value}'


class Deck:
    def __init__(self):
        self.cards = []
        self.discarded = set()
        self.table_cards = []
        for suit in Suits:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
        random.shuffle(self.cards)

    def deal_table(self):
        self.discarded.update(self.table_cards)
        if len(self.cards) >= 6:
            self.table_cards = [self.cards.pop() for _ in range(6)]
        else:
            print("in else deal")
            self.cards.extend(self.discarded)
            random.shuffle(self.cards)
            self.table_cards = [self.cards.pop() for _ in range(6)]
            self.discarded = set()

    def deal_cards_player(self, play_cards):
        if len(self.cards) + len(self.discarded) >= 4:
            if len(self.cards) >= 4:
                return [self.cards.pop() for _ in range(4)]
            else:
                self.cards.extend(self.discarded)
                random.shuffle(self.cards)
                self.discarded = set()
                return [self.cards.pop() for _ in range(4)]
        else:
            return None



