import pygame

class Button:
    """Create a button"""

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
        window.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False


def display_cards(window, play_cards, deck):
    card_coord = []
    w, h = window.get_width() / 2 - 4 * play_cards[0].image.get_width(), 0
    for idx, card in enumerate(deck.table_cards):
        window.blit(card.image, (w := w + card.image.get_width() + 15, h))
        card_coord.append((card, (w, h)))

    w, h = window.get_width() / 2 - 3 * play_cards[0].image.get_width(), window.get_height() - 1.5 * play_cards[
        0].image.get_width()
    for idx, card in enumerate(play_cards):
        window.blit(card.image, (w := w + card.image.get_width() + 15, h))
        card_coord.append((card, (w, h)))
    return card_coord


def swap_cards(first_card, card_coord, mouse_pos, play_cards, deck):
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

                    first_card = None

    return first_card, play_cards
