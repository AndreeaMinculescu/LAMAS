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

        w, h = window.get_width()/2 - 4 * play_cards[0].image.get_width(), 0
        for idx, card in enumerate(table_cards):
            window.blit(card.image, (w := w+card.image.get_width()+15, h))

        w, h = window.get_width()/2 - 3 * play_cards[0].image.get_width(), window.get_height() - 1.5 * play_cards[0].image.get_width()
        for idx, card in enumerate(play_cards):
            window.blit(card.image, (w := w+card.image.get_width()+15, h))


        pygame.display.update()


pygame.quit()
