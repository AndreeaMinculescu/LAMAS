from agent import Agent
from card import Deck
from knowledge_base import KnowledgeBase
from announcement import PublicAnnouncement

def make_announcements(announcements, players):
    for announcement in announcements:
        sender = announcement.sender
        for player in players:
            if player != sender:
                print(f"KB of {player.name} before announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")
                print(f"Player {player.name} recieved announcement: {announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}")
                player.recieve_announcement(announcement)
                print(f"KB of {player.name} after announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")
            
deck = Deck()
deck.deal_table()

player1 = Agent("p1", deck.deal_cards_player([]), deck.table_cards)
player2 = Agent("p2", deck.deal_cards_player([]), deck.table_cards)
player3 = Agent("p3", deck.deal_cards_player([]), deck.table_cards)

player1.kb = KnowledgeBase(player1, [player2, player3], deck.whole_deck)
player2.kb = KnowledgeBase(player2, [player1, player3], deck.whole_deck)
player3.kb = KnowledgeBase(player3, [player1, player2], deck.whole_deck)

print(player1.kb)
print(player2.kb)
print(player3.kb)

turn = 0

# while len(deck.cards) + len(deck.discarded) >= 6:
for _ in range(3):
    print("\n############### New round ####################")
    
    if turn == 0:
        player = player1
        print("player 1 turn")
    if turn == 1:
        print("player 2 turn")
        player = player2
    if turn == 2:
        print("player 3 turn")
        player = player3
        turn = 0

    announcements = player.greedy_strategy(verbose=True)
    make_announcements(announcements, [player1,player2,player3])
    if player.check_kemps():
        print("Kemps!")
        player.score += 1
        player.cards = deck.deal_cards_player(player.cards)
    
    deck.deal_table()
    player1.table = deck.table_cards
    player2.table = deck.table_cards
    player3.table = deck.table_cards

    turn += 1

print("Number of turns: ", turn)
print("Player 1 score: ", player1.score)
print("Player 2 score: ", player2.score)
print("Player 3 score: ", player3.score)
    
