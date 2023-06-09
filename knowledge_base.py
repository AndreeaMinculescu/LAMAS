from card import Card
import random
class KnowledgeBase:

    def __init__(self, player, other_players, all_cards:list[Card]):
        """
        KB is a dictionary of dictionaries, for each card possible (52) in a deck
        keep track of who has the card
        """
        self.player = player
        self.other_players = other_players
        self.all_cards = all_cards
        self.knowledge = {}
        self.game_model = None
        self.discard_cards = []
        
        for c in self.all_cards:
            # ASSUMPTION: theres always three players
            # in the beginning (before looking at your own cards and cards on table) 
            # nothing is possible
            kb = {
                    self.player.name: None,
                    self.other_players[0].name: None,
                    self.other_players[1].name: None
                 }

            self.knowledge[(c.suit, c.value)] = kb
            
        self.set_knowledge_of_other_cards()
        self.set_knowledge_own_deck()
    
    def __str__(self):
        return f""" 
                Player: {self.player.name}
                Other players: {[i.name for i in self.other_players]}
                Cards: {len(self.all_cards)}
                Knowledge: {[(i, [(j, l) for j,l in k.items()]) for i, k in self.knowledge.items()]}
                """

    def set_knowledge_of_other_cards(self):
        """
        player knows that cards on the table are in no ones hands,
        cards in discard pile are in no ones hand,
        and cards not on the table and not in players hands and not in the discard pile are in someone's hand possibly
        """
        # ASSUMPTION: theres always three players
        kb1 = {
                self.player.name: False,
                self.other_players[0].name: True,
                self.other_players[1].name: True
             }

        kb2 = {
                self.player.name: False,
                self.other_players[0].name: False,
                self.other_players[1].name: False
             }

        # cards on table in no ones hand
        for t in self.player.table:    
            self.knowledge[(t.suit, t.value)] = kb2 

        # cards in discard pile in no ones hand
        for t in self.discard_cards:
            self.knowledge[(t[1], t[0])] = kb2 

        # cards not on the table or not in the players hands or not in discard pile can be in anyone but the player's hand
        remainder_cards = list(set([(i.suit,i.value) for i in self.all_cards]) - set([(i.suit,i.value) for i in self.player.cards]) - set([(i.suit,i.value) for i in self.player.table]) - set(self.discard_cards))
        for card in self.all_cards:
            if (card.suit, card.value) in remainder_cards:
                self.knowledge[(card.suit, card.value)] = kb1 

    def update_discard_pile(self, discards):
        """
        Update knowledge about what does in the discarded pile, equivalent of seeing the table being reset
        """
        kb = {
                self.player.name: False,
                self.other_players[0].name: False,
                self.other_players[1].name: False
             }
        # print("discards: ", [(card.value, card.suit) for card in discards])
        for card in discards:
            # no one has cards which are in discard pile
            self.knowledge[(card.suit, card.value)] = kb
            self.discard_cards.append((card.suit, card.value))

    def set_knowledge_own_deck(self):
        """
        player knows the cards in their hand are not in other players hands
        """
        # ASSUMPTION: theres always three players
        kb = {
                self.player.name: True,
                self.other_players[0].name: False,
                self.other_players[1].name: False
             }

        for card in self.player.cards:
            self.knowledge[(card.suit, card.value)] = kb

    def set_card_knowledge_of_individual(self, card, player):
        """
        Change the knowledge of a given card for a given player, equivalent to seeing someone pick up a card
        """
        if (card.suit, card.value) not in self.knowledge.keys():
            s = f"Trying to change knowledge of a {(card.value, card.suit)} which does not exist in KB of " + self.player.name
            raise Exception(s)
        # ASSUMPTION: theres always three players
        kb = {
                self.player.name: False,
                self.other_players[0].name: False,
                self.other_players[1].name: False
             }

        kb[player.name] = True
        self.knowledge[(card.suit, card.value)] = kb
        

    def set_discard_knowledge(self, card, player):
        """
        Change the knowledge of a given card for a given player, equivalent to seeing someone discard a card
        """
        if (card.suit, card.value) not in self.knowledge.keys():
            s = "Trying to change knowledge of a card which does not exist in KB of " + self.player.name
            raise Exception(s)

        kb = self.knowledge[(card.suit, card.value)]

        # discarded cards go on table so no-one has them
        kb = {
                self.player.name: False,
                self.other_players[0].name: False,
                self.other_players[1].name: False
             }

        self.knowledge[(card.suit, card.value)] = kb 


    def check_players_have_number(self, value):
        """
        Check to see if both other players have a certain value
        """
        p1 = False
        p2 = False
        
        for c, kb in self.knowledge.items():
            if c[1] == value:
                # ... if another player has value
                print(c)
                print(kb)

                p1 = kb[self.other_players[0].name]
                p2 = kb[self.other_players[1].name]

                if p1 and p2:
                    return True

        return False


