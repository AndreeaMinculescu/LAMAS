import pygame
from card import *

pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
run = True

deck = Deck()
table_cards = deck.deal_table()
play_cards = deck.deal_cards_player()

card_back = pygame.image.load('card_design/BACK.png')
card_back = pygame.transform.scale(card_back, (table_cards[0].image.get_width(), table_cards[0].image.get_height()))

model_icon = pygame.image.load('card_design/model_icon.png')
model_icon = pygame.transform.scale(model_icon, (int(model_icon.get_width()/2), model_icon.get_height()/2))

first_card = None


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos, font, bg="black"):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        window.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return deck.deal_table()
        return None


button1 = Button(
    "Next turn",
    (100, 100),
    font=30,
    bg="black")

def display_cards():
    card_coord = []
    w, h = window.get_width() / 2 - 4 * play_cards[0].image.get_width(), 0
    for idx, card in enumerate(table_cards):
        window.blit(card.image, (w := w + card.image.get_width() + 15, h))
        card_coord.append((card, (w, h)))

    w, h = window.get_width() / 2 - 3 * play_cards[0].image.get_width(), window.get_height() - 1.5 * play_cards[
        0].image.get_width()
    for idx, card in enumerate(play_cards):
        window.blit(card.image, (w := w + card.image.get_width() + 15, h))
        card_coord.append((card, (w, h)))
    return card_coord

while run:
    pygame.display.set_caption("Kemps!")
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False


        window.fill((15, 0, 169))

        model_one = pygame.transform.rotate(card_back, -90)
        window.blit(model_one, (0, window.get_height()/2 - model_one.get_height()/2))
        model_two = pygame.transform.rotate(card_back, 90)
        window.blit(model_two, (window.get_width() - model_two.get_width(), window.get_height() / 2 - model_two.get_height() / 2))

        card_coord = display_cards()


        pos = None
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
        for card, coord in card_coord:
            rect_coord = pygame.Rect(coord[0], coord[1], card.image.get_width(), card.image.get_height())
            if pos is not None and rect_coord.collidepoint(pos):
                if first_card is None:
                    first_card = card
                else:
                    if card in table_cards:
                        table_cards[table_cards.index(card)] = first_card
                    else:
                        play_cards[play_cards.index(card)] = first_card

                    if first_card in table_cards:
                        table_cards[table_cards.index(first_card)] = card
                    else:
                        play_cards[play_cards.index(first_card)] = card

                    _ = display_cards()
                    first_card = None

        if new_cards := button1.click(event):
            table_cards = new_cards
        button1.show()
        pygame.display.update()


pygame.quit()
