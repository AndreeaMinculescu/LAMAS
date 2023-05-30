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


class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suits:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
        random.shuffle(self.cards)

    def deal_table(self):
        return [self.cards.pop() for _ in range(6)]

    def deal_cards_player(self):
        return [self.cards.pop() for _ in range(4)]



