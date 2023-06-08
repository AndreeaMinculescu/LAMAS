from agent import Agent
from card import Deck
from knowledge_base import KnowledgeBase
from announcement import PublicAnnouncement
from statistics import mean

def make_announcements(announcements, players):
    for announcement in announcements:
        sender = announcement.sender
        for player in players:
            if player != sender:
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

for _ in range(10):

    player1, player2, player3, deck = init_game()
    turn = 0
    while True:
        print("\n############### New round ####################")

        if turn % 3 == 0:
            player = player1
            print("player 1 turn")
        if turn % 3 == 1:
            print("player 2 turn")
            player = player2
        if turn % 3 == 2:
            print("player 3 turn")
            player = player3

        announcements = player.greedy_strategy(verbose=0)
        make_announcements(announcements, [player1, player2, player3])
        if player.check_kemps():
            print("Kemps!")
            if cards := deck.deal_cards_player():
                player.cards = cards
            else:
                break

        deck.deal_table()
        player1.table = deck.table_cards
        player2.table = deck.table_cards
        player3.table = deck.table_cards

        turn += 1
    p1_score.append(player1.score)
    p2_score.append(player2.score)
    p3_score.append(player3.score)

print("Player 1 score: ", mean(p1_score))
print("Player 2 score: ", mean(p2_score))
print("Player 3 score: ", mean(p3_score))
    
