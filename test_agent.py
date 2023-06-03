from agent import Agent
from card import Deck

deck = Deck()
deck.deal_table()

player1 = Agent(deck.deal_cards_player(), deck.table_cards)
player2 = Agent(deck.deal_cards_player(), deck.table_cards)
turn = 0
while len(deck.cards) + len(deck.discarded) >= 6:
    print("############### New round ####################")
    player = player1
    if turn % 2 == 1:
        player = player2

    player.greedy_strategy(verbose=1)
    if player.check_kemps():
        print("Kemps!")
        player.score += 1
        player.cards = deck.deal_cards_player()
    deck.deal_table()
    player1.table = deck.table_cards
    player2.table = deck.table_cards
    turn += 1

print(turn)
print("Player 1 score: ", player1.score)
print("Player 2 score: ", player2.score)
