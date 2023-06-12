import pygame
import ptext

class Button:
    """Initialize a button"""
    def __init__(self, text, pos, font, bg="black"):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, window):
        # display the button
        window.blit(self.surface, (self.x, self.y))

    def click(self, event):
        # handle click event
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False


def display_cards(window, play_cards, deck, only_table=False):
    """
    Display user cards and/or table cards
    :param window: pygame screen
    :param play_cards: user cards
    :param deck: the current card deck
    :param only_table: if True, only update the table cards
    :return: card coordinates
    """
    card_coord = []
    w, h = window.get_width() / 2 - 4 * play_cards[0].image.get_width(), 0
    for idx, card in enumerate(deck.table_cards):
        window.blit(card.image, (w := w + card.image.get_width() + 15, h))
        card_coord.append((card, (w, h)))

    if not only_table:
        w, h = window.get_width() / 2 - 3 * play_cards[0].image.get_width(), window.get_height() - 1.5 * play_cards[
            0].image.get_width()
        for idx, card in enumerate(play_cards):
            window.blit(card.image, (w := w + card.image.get_width() + 15, h))
            card_coord.append((card, (w, h)))
    return card_coord


def swap_cards(first_card, card_coord, mouse_pos, play_cards, deck):
    """
    Handle swap events: update the user cards and the table cards after performing the swap
    :param first_card: card that was clicked first (if None, then the current click is the first)
    :param card_coord: coordinates of all table and user cards
    :param mouse_pos: current position of the mouse
    :param play_cards: the cards of the user
    :param deck: the current deck of cards
    :return: the first click, the user cards and two swapped cards
    """
    flag = False
    for card, coord in card_coord:
        rect_coord = pygame.Rect(coord[0], coord[1], card.image.get_width(), card.image.get_height())
        if mouse_pos is not None and rect_coord.collidepoint(mouse_pos):
            if first_card is None:
                first_card = card
            else:
                if not ((first_card in deck.table_cards and card in deck.table_cards) or
                        (first_card in play_cards and card in play_cards)):
                    temp_table_cards = deck.table_cards[:]
                    if card in temp_table_cards:
                        deck.table_cards[deck.table_cards.index(card)] = first_card
                    else:
                        play_cards[play_cards.index(card)] = first_card

                    if first_card in temp_table_cards:
                        deck.table_cards[deck.table_cards.index(first_card)] = card
                    else:
                        play_cards[play_cards.index(first_card)] = card
                    flag = True
                    swap = card

    if flag:
        return None, play_cards, first_card, swap
    else:
        return first_card, play_cards, None, None


def display_text(window, text):
    """
    Display text on screen for the user (regarding the models' moves)
    :param window: the pygame screen
    :param text: the text to be displayed
    :return: None
    """
    window.fill((15, 0, 169), ((window.get_width() // 4, window.get_height() // 2.5, window.get_width()//2, window.get_height()//4)))
    font = pygame.font.Font('freesansbold.ttf', 26)
    lines = text.splitlines()
    for i, l in enumerate(lines):
        window.blit(font.render(l, True, (0, 0, 128), (255, 255, 255)), (window.get_width() // 4, window.get_height() // 2.5 + 26 * i))
