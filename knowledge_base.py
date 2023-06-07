from card import Card

class KnowledgeBase:

    def __init__(self, player, other_players, all_cards:list[Card]):

        self.player = player
        self.other_players = other_players
        self.all_cards = all_cards
        self.knowledge = {}
        self.game_model = None

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
        player knows that cards on the table are in no ones hands
        and cards not on the table and not in players hands are in someone's hand possibly but not his own
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
            print("card on table: ", t)                        

        # cards not on the table or the players hands can be in anyone but the player's hand
        remainder_cards = list(set([(i.suit,i.value) for i in self.all_cards]) - set([(i.suit,i.value) for i in self.player.cards]) - set([(i.suit,i.value) for i in self.player.table]))
        for card in self.all_cards:
            if (card.suit, card.value) in remainder_cards:
                self.knowledge[(card.suit, card.value)] = kb1 


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


    def get_card_knowledge(self, card):
        if (card.suit, card.value) not in self.knowledge.keys():
            s = "Trying to change knowledge of a card which does not exist in KB of " + self.player.name
            raise Exception(s)

        for c, knowledge in self.knowledge.items():
            if c == (card.suit, card.value):
                return knowledge 

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




