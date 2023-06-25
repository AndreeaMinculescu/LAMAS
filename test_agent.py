from agent import Agent
from card import Deck, print_arr_cards
from knowledge_base import KnowledgeBase
from announcement import PublicAnnouncement, AnnouncementType
from statistics import mean
import random
import pickle

############ Testing environment, not part of the main pipeline #####################
def make_announcements(announcements, players):
    for announcement in announcements:
        sender = announcement.sender
        for player in players:
            if player.name != sender.name:
                # print(f"KB of {player.name} before announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")
                # print(f"Player {player.name} recieved announcement: {announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}")
                player.recieve_announcement(announcement)
                # print(f"KB of {player.name} after announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")


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
turns = []
kb_greedy = False
blocking = False
no_moves_count = 0

for config in [[[True, True], [True, True], [True, True], "KB Blocking"],
               [[True, False], [False, False], [False, False], "1 KB Greedy vs 2 Greedy"],
               [[True, True], [False, False], [False, False], "1 KB Blocking vs 2 Greedy"],
               [[True, True], [True, False], [True, False], "1 KB Blocking vs 2 KB Greedy"]]:

    for seed in [123, 222, 666, 42, 27, 35, 49]:
        random.seed(seed)

        for _ in range(1000):
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
                    # print("\n   NEXT TURN: player 1 turn")
                    announcements = player.greedy_strategy(verbose=False, kb_based=config[0][0], blocking=config[0][1])
                if turn % 3 == 1:
                    player = player2
                    # kb_greedy = True
                    # print("\n   NEXT TURN: player 2 turn")
                    announcements = player.greedy_strategy(verbose=False, kb_based=config[1][0], blocking=config[1][1])
                if turn % 3 == 2:
                    # kb_greedy = True
                    # print("\n   NEXT TURN player 3 turn")
                    player = player3
                    announcements = player.greedy_strategy(verbose=False, kb_based=config[2][0], blocking=config[2][1])

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

                if turn > 10_000:
                    break

            p1_score.append(player1.score)
            p2_score.append(player2.score)
            p3_score.append(player3.score)

    print()
    print("Player 1 score: ", sum(p1_score))
    print("Player 2 score: ", sum(p2_score))
    print("Player 3 score: ", sum(p3_score))

    final_data = {"title": config[3],
                  "p1": p1_score,
                  "p2": p2_score,
                  "p3": p3_score}

    with open(f"./data/{config[3].replace(' ', '_')}.pickl", "wb") as f:
        pickle.dump(final_data, f)
    
