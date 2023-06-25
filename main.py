import pygame
from card import *
from view import Button, display_cards, swap_cards, display_text
from agent import Agent
from knowledge_base import KnowledgeBase
from announcement import PublicAnnouncement, AnnouncementType, make_announcements
import time


def init_game():
    """
    Initialize agents and knowledge bases
    :param deck: deck of cards
    :return: the three players (user included)
    """
    # initialize deck of cards
    deck = Deck()
    deck.deal_table()

    user = Agent("user", deck.deal_cards_player(), deck.table_cards)
    player2 = Agent("p2", deck.deal_cards_player(), deck.table_cards)
    player3 = Agent("p3", deck.deal_cards_player(), deck.table_cards)

    user.kb = KnowledgeBase(user, [player2, player3], deck.whole_deck)
    player2.kb = KnowledgeBase(player2, [user, player3], deck.whole_deck)
    player3.kb = KnowledgeBase(player3, [user, player2], deck.whole_deck)

    type_player2 = input('What kind of agent should model 1 be? (options: GREEDY, KB-GREEDY, KB-BLOCKING; default GREEDY) ')
    type_player3 = input('What kind of agent should model 2 be? (options: GREEDY, KB-GREEDY, KB-BLOCKING; default GREEDY) ')

    if type_player2.lower() == "KB-GREEDY".lower():
        player2.kb_greedy = True
    if type_player2.lower() == "KB-BLOCKING".lower():
        player2.blocking = True
        player2.kb_greedy = True

    if type_player3.lower() == "KB-GREEDY".lower():
        player3.kb_greedy = True
    if type_player3.lower() == "KB-BLOCKING".lower():
        player3.blocking = True
        player3.kb_greedy = True

    return user, player2, player3, deck

# initialize players and game
user, player2, player3, deck = init_game()
kb_greedy = False
turn = 0
end_game = False
no_moves_count = 0

# initialize pygame screen
pygame.init()
SIZE = (1400, 800)
window = pygame.display.set_mode(SIZE)
# set background colour
window.fill((15, 0, 169))

# for swap events
first_card = None

# get image of the back of the deck of cards (as placeholders for the models)
card_back = pygame.image.load('card_design/BACK.png')
card_back = pygame.transform.scale(card_back, (deck.cards[0].image.get_width(), deck.cards[0].image.get_height()))

# initialize "Next turn" button (for user)
button_turn = Button("Next turn", (10, card_back.get_height()/2), font=30)

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
        print("\n   NEXT TURN: user turn")
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

                # handle player swap events and update cards view
                pos = None
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                initial_cards = user.cards
                initial_table = deck.table_cards
                first_card, user.cards, first_swap, second_swap = swap_cards(first_card, card_coord, pos,
                                                                                     user.cards, deck, window)
                # handle next turn
                if button_turn.click(event):
                    run = False
                button_turn.show(window)

                model_one = pygame.transform.rotate(card_back, -90)
                window.blit(model_one, (0, window.get_height() / 2 - model_one.get_height() / 2))
                model_two = pygame.transform.rotate(card_back, 90)
                window.blit(model_two,
                            (window.get_width() - model_two.get_width(),
                             window.get_height() / 2 - model_two.get_height() / 2))


                card_coord = display_cards(window, user.cards, deck)

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

                # update game
                display_text(window, " Your turn \n The top cards are table cards (can be seen by all players) \n and "
                                     "the bottom cards are your cards \n Select one table card and one hand card to "
                                     "swap them \n Click on Next turn to end your turn \n Goal: get four cards with the "
                                     "same number \n ESC to exit game.")
                pygame.display.update()

        # update all agent kbs
        make_announcements(announcements, [user, player2, player3])

    # handle models' turn
    else:
        # decide which agent's turn it is (model 1 or 2)
        if turn % 3 == 1:
            # kb_greedy = True
            text = "Model 1 turn \n"
            print("\n   NEXT TURN: model 1 turn")
            player = player2
        if turn % 3 == 2:
            # kb_greedy = True
            text = "Model 2 turn \n"
            print("\n   NEXT TURN: model 2 turn")
            player = player3

        # update table card view (before any moves made)
        player.table = deck.table_cards
        _ = display_cards(window, player.cards, deck, only_table=True)
        display_text(window, text)
        pygame.display.update()
        # give user time to read cards on table
        time.sleep(3)

        # run greedy strategy
        announcements = player.greedy_strategy(verbose=True, kb_based=player.kb_greedy, blocking=player.blocking)

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
