from agent import Agent
from card import Deck, print_arr_cards, Card, Suits
from knowledge_base import KnowledgeBase
from announcement import PublicAnnouncement, AnnouncementType, make_announcements
from statistics import mean
import random

############ Testing environment, not part of the main pipeline #####################

def init_game():
    deck = Deck()
    deck.deal_table()

    player1 = Agent("p1", deck.deal_cards_player(), deck.table_cards)
    player2 = Agent("p2", deck.deal_cards_player(), deck.table_cards)
    player3 = Agent("p3", deck.deal_cards_player(), deck.table_cards)

    player1.kb = KnowledgeBase(player1, [player2, player3], deck.whole_deck)
    player2.kb = KnowledgeBase(player2, [player1, player3], deck.whole_deck)
    player3.kb = KnowledgeBase(player3, [player1, player2], deck.whole_deck)
    return player1, player2, player3, deck


p1_score = []
p2_score = []
p3_score = []
kb_greedy = True
blocking = True
verbose = True
no_moves_count = 0

# for seed in [123, 222, 666, 42, 27, 35, 49]:
for seed in [1]:
    # random.seed(seed)

    for _ in range(1):
        print(f"\n############### NEW GAME: {seed}: {_} ####################")
        player1, player2, player3, deck = init_game()
        turn = 0

        while True:
            # print("\n############### New round ####################")
            init_cards = deck.table_cards[:]

            if no_moves_count == 3:
                deck.deal_table()
                player1.kb.set_knowledge_of_other_cards()
                player2.kb.set_knowledge_of_other_cards()
                player3.kb.set_knowledge_of_other_cards()
                no_moves_count = 0

            # remember which cards have been discarded
            player1.kb.update_discard_pile(list(deck.discarded) + deck.table_cards)
            player2.kb.update_discard_pile(list(deck.discarded) + deck.table_cards)
            player3.kb.update_discard_pile(list(deck.discarded) + deck.table_cards)

            player1.table = deck.table_cards
            player2.table = deck.table_cards
            player3.table = deck.table_cards

            if turn % 3 == 0:
                player = player1
                # kb_greedy = True
                print("\n   NEXT TURN: player 1 turn")
                announcements = player.greedy_strategy(verbose=verbose, kb_based=kb_greedy, blocking=blocking)
            if turn % 3 == 1:
                player = player2
                # kb_greedy = True
                print("\n   NEXT TURN: player 2 turn")
                announcements = player.greedy_strategy(verbose=verbose, kb_based=kb_greedy, blocking=blocking)
            if turn % 3 == 2:
                # kb_greedy = True
                print("\n   NEXT TURN player 3 turn")
                player = player3
                announcements = player.greedy_strategy(verbose=verbose, kb_based=kb_greedy, blocking=blocking)

            # print("discard pile: ", [(card.value, card.suit) for card in list(deck.discarded)])
            make_announcements(announcements, [player1, player2, player3])

            # update points
            if player.check_kemps():
                make_announcements([PublicAnnouncement(player, player.cards[0], AnnouncementType.KEMPS)], [player1, player2, player3])
                # print("Kemps!")
                if cards := deck.deal_cards_player():
                    # give new cards to player
                    player.kb.set_knowledge_own_deck()
                    player.cards = cards
                else:
                    break

            if deck.table_cards == init_cards:
                no_moves_count += 1
            else:
                no_moves_count = 0
            turn += 1

        p1_score.append(player1.score)
        p2_score.append(player2.score)
        p3_score.append(player3.score)

print()
print("Player 1 score: ", sum(p1_score))
print("Player 2 score: ", sum(p2_score))
print("Player 3 score: ", sum(p3_score))
    
