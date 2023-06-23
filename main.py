import pygame
from card import *
from view import Button, display_cards, swap_cards, display_text
from agent import Agent
from knowledge_base import KnowledgeBase
from announcement import PublicAnnouncement, AnnouncementType, make_announcements
import time


def init_game(deck):
    """
    Initialize agents and knowledge bases
    :param deck: deck of cards
    :return: the three players (user included)
    """

    user = Agent("user", deck.deal_cards_player(), deck.table_cards)
    player2 = Agent("p2", deck.deal_cards_player(), deck.table_cards)
    player3 = Agent("p3", deck.deal_cards_player(), deck.table_cards)
    print("user ")
    print_arr_cards(user.cards)
    print("player1 ")
    print_arr_cards(player2.cards)
    print("player2 ")
    print_arr_cards(player3.cards)

    user.kb = KnowledgeBase(user, [player2, player3], deck.whole_deck)
    player2.kb = KnowledgeBase(player2, [user, player3], deck.whole_deck)
    player3.kb = KnowledgeBase(player3, [user, player2], deck.whole_deck)
    return user, player2, player3


# initialize pygame screen
pygame.init()
SIZE = (1400, 800)
window = pygame.display.set_mode(SIZE)
# set background colour
window.fill((15, 0, 169))

# initialize deck of cards
deck = Deck()

# for swap events
first_card = None

# get image of the back of the deck of cards (as placeholders for the models)
card_back = pygame.image.load('card_design/BACK.png')
card_back = pygame.transform.scale(card_back, (deck.cards[0].image.get_width(), deck.cards[0].image.get_height()))

# initialize "Next turn" button (for user)
button_turn = Button("Next turn", (10, card_back.get_height()/2), font=30)

# initialize players and game
user, player2, player3 = init_game(deck)
kb_greedy = False
turn = 0
end_game = False
no_moves_count = 0
deck.deal_table()

while not end_game:
    # set name of pygame screen
    pygame.display.set_caption("Kemps!")
    window.fill((15, 0, 169))

    # visualize players (placeholders)
    model_one = pygame.transform.rotate(card_back, -90)
    window.blit(model_one, (0, window.get_height() / 2 - model_one.get_height() / 2))
    model_two = pygame.transform.rotate(card_back, 90)
    window.blit(model_two,
                (window.get_width() - model_two.get_width(), window.get_height() / 2 - model_two.get_height() / 2))

    # display cards and get card coordinated
    card_coord = display_cards(window, user.cards, deck)

    # every three turn reset cards on table
    if no_moves_count == 3:
        deck.deal_table()
        user.kb.set_knowledge_of_other_cards()
        player2.kb.set_knowledge_of_other_cards()
        player3.kb.set_knowledge_of_other_cards()
        no_moves_count = 0

    init_cards = deck.table_cards[:]
    # update knowledge base of players given new set of cards and list of discarded cards
    user.kb.update_discard_pile(list(deck.discarded) + deck.table_cards)
    player2.kb.update_discard_pile(list(deck.discarded) + deck.table_cards)
    player3.kb.update_discard_pile(list(deck.discarded) + deck.table_cards)

    user.table = deck.table_cards
    player2.table = deck.table_cards
    player3.table = deck.table_cards

    announcements = []

    # handle user's turn
    if turn % 3 == 0:
        run = True
        while run:
            for event in pygame.event.get():

                # handle game exit
                if event.type == pygame.QUIT:
                    run = False
                    end_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        end_game = True

                # handle next turn
                if button_turn.click(event):
                    run = False
                button_turn.show(window)

                # handle player swap events and update cards view
                pos = None
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                initial_cards = user.cards
                initial_table = deck.table_cards
                first_card, user.cards, first_swap, second_swap = swap_cards(first_card, card_coord, pos, user.cards, deck)
                _ = display_cards(window, user.cards, deck)

                # create public announcements for swap events (to update agents' kbs)
                if first_swap:
                    if first_swap in user.cards:
                        announcements.append(PublicAnnouncement(user, first_swap, AnnouncementType.PICKED))
                        announcements.append(PublicAnnouncement(user, second_swap, AnnouncementType.DISCARDED))
                    if first_swap in deck.table_cards:
                        announcements.append(PublicAnnouncement(user, second_swap, AnnouncementType.PICKED))
                        announcements.append(PublicAnnouncement(user, first_swap, AnnouncementType.DISCARDED))

                # check for Kemps and create public announcement
                if user.check_kemps():
                    announcements.append(PublicAnnouncement(user, user.cards[0], AnnouncementType.KEMPS))
                    user.cards = deck.deal_cards_player()
                    if user.cards:
                        user.kb.set_knowledge_own_deck()
                        _ = display_cards(window, user.cards, deck)
                    else:
                        end_game = True
                    run = False

                # update all agent kbs
                make_announcements(announcements, [user, player2, player3])

                # update game
                display_text(window, "Your turn")
                pygame.display.update()

    # handle models' turn
    else:
        # decide which agent's turn it is (model 1 or 2)
        if turn % 3 == 1:
            # kb_greedy = True
            text = "Model 1 turn \n"
            player = player2
        if turn % 3 == 2:
            # kb_greedy = True
            text = "Model 2 turn \n"
            player = player3

        # update table card view (before any moves made)
        player.table = deck.table_cards
        _ = display_cards(window, player.cards, deck, only_table=True)
        display_text(window, text)
        pygame.display.update()
        # give user time to read cards on table
        time.sleep(3)

        # run greedy strategy
        announcements = player.greedy_strategy(verbose=False, kb_based=kb_greedy)

        # check Kemps and create public announcement
        if player.check_kemps():
            announcements.append(PublicAnnouncement(player, player.cards[0], AnnouncementType.KEMPS))
            if cards := deck.deal_cards_player():
                # give new cards to player and update knowledge
                player.kb.set_knowledge_own_deck()
                player.cards = cards
            else:
                end_game = True

        # update all kbs
        make_announcements(announcements, [user, player2, player3])

        # update table card view (after moves made
        _ = display_cards(window, player.cards, deck, only_table=True)

        # display text to user regarding agents' actions (for readibility)
        if announcements:
            for ann in announcements:
                print(ann.type)
                if ann.type == AnnouncementType.PICKED:
                    text += f"Model picked card <{ann.card.value}, {ann.card.suit.name}> \n"
                elif ann.type == AnnouncementType.DISCARDED:
                    text += f"Model discarded card <{ann.card.value}, {ann.card.suit.name}> \n"
                else:
                    text += f"Kemps with number {ann.card.value}! \n"
        else:
            text += "No moves made. \n"
        display_text(window, text)
        pygame.display.update()

        # give user time to process the moves of the model
        time.sleep(5)

    # start next turn
    if deck.table_cards == init_cards:
        no_moves_count += 1
    else:
        no_moves_count = 0
    turn += 1

print("User score: ", user.score)
print("Model 2 score: ", player2.score)
print("Model 3 score: ", player3.score)

pygame.quit()
