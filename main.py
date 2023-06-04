import pygame
from card import *
from view import Button, display_cards, swap_cards
from agent import Agent

pygame.init()
SIZE = (1400, 800)
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
run = True

deck = Deck()
deck.deal_table()
player = Agent(deck.deal_cards_player([]), deck.table_cards)
first_card = None # for swap events

card_back = pygame.image.load('card_design/BACK.png')
card_back = pygame.transform.scale(card_back, (deck.table_cards[0].image.get_width(), deck.table_cards[0].image.get_height()))

model_icon = pygame.image.load('card_design/model_icon.png')
model_icon = pygame.transform.scale(model_icon, (int(model_icon.get_width()/2), model_icon.get_height()/2))

button_turn = Button("Next turn", (10, card_back.get_height()/2), font=30)

while run:
    pygame.display.set_caption("Kemps!")
    for event in pygame.event.get():

        # handle game exit
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        # set background colour
        window.fill((15, 0, 169))

        # handle next turn
        if button_turn.click(event):
            deck.deal_table()
        button_turn.show(window)

        # visualize players (placeholders)
        model_one = pygame.transform.rotate(card_back, -90)
        window.blit(model_one, (0, window.get_height()/2 - model_one.get_height()/2))
        model_two = pygame.transform.rotate(card_back, 90)
        window.blit(model_two, (window.get_width() - model_two.get_width(), window.get_height() / 2 - model_two.get_height() / 2))

        # display cards
        card_coord = display_cards(window, player.cards, deck)

        # handle player swap events and update cards view
        pos = None
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
        first_card, player.cards = swap_cards(first_card, card_coord, pos, player.cards, deck)
        _ = display_cards(window, player.cards, deck)

        # check for Kemps
        if player.check_kemps():
            player.cards = deck.deal_cards_player(player.cards)
            deck.deal_table()
            if player.cards:
                _ = display_cards(window, player.cards, deck)
            else:
                run = False

        # update game
        pygame.display.update()

print("Score: ", player.score)
pygame.quit()
