from agent import Agent
from card import Deck
from knowledge_base import KnowledgeBase
from announcement import PublicAnnouncement, AnnouncementType
from statistics import mean

def make_announcements(announcements, players):
    for announcement in announcements:
        sender = announcement.sender
        for player in players:
            if player.name != sender.name:
                print(f"KB of {player.name} before announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")
                print(f"Player {player.name} recieved announcement: {announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}")
                player.recieve_announcement(announcement)
                print(f"KB of {player.name} after announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")


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
kb_greedy = False

for _ in range(1):
    print("\n############### NEW GAME ####################")
    player1, player2, player3, deck = init_game()
    turn = 0

    while True:
        print("\n############### New round ####################")

        if turn % 3 == 0:
            player = player1
            kb_greedy = True
            print("player 1 turn")
        if turn % 3 == 1:
            kb_greedy = True
            print("player 2 turn")
            player = player2
        if turn % 3 == 2:
            kb_greedy = True
            print("player 3 turn")
            player = player3

        print("discard pile: ", [(card.value, card.suit) for card in list(deck.discarded)])
        announcements = player.greedy_strategy(verbose=False, kb_based=kb_greedy)
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

        

        deck.deal_table()

        # remember which cards have been discarded
        player1.kb.update_discard_pile(list(deck.discarded))
        player2.kb.update_discard_pile(list(deck.discarded))
        player3.kb.update_discard_pile(list(deck.discarded))

        player1.table = deck.table_cards
        player2.table = deck.table_cards
        player3.table = deck.table_cards

        player1.kb.set_knowledge_of_other_cards()
        player2.kb.set_knowledge_of_other_cards()
        player3.kb.set_knowledge_of_other_cards()

        # print("discard pile: ", [(card.value, card.suit) for card in list(deck.discarded)])

        turn += 1

    p1_score.append(player1.score)
    p2_score.append(player2.score)
    p3_score.append(player3.score)

print("Player 1 score: ", sum(p1_score))
print("Player 2 score: ", sum(p2_score))
print("Player 3 score: ", sum(p3_score))
    
