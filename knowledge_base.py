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
            kb = {
                    self.player: False,
                    self.other_players[0]: False,
                    self.other_players[1]: False
                 }

            self.knowledge[c] = kb

        self.set_knowledge_of_other_cards()
        self.set_knowledge_own_deck()
    
    def __str__(self):
        return f""" 
                Player: {self.player.name}
                Other players: {[i.name for i in self.other_players]}
                Cards: {len(self.all_cards)}
                Knowledge: {[(i.value, i.suit, [(j.name,l) for j,l in k.items()]) for i, k in self.knowledge.items()]}
                """

    def set_knowledge_of_other_cards(self):
        """
        player knows that cards not in their hand and cards 
        not on the table can be in all other players hands
        """
        kb = {
                self.player: False,
                self.other_players[0]: True,
                self.other_players[1]: True
             }

        for card in self.all_cards:
            if card not in self.player.cards and card not in self.player.table:
                self.knowledge[card] = kb


    def set_knowledge_own_deck(self):
        """
        player knows the cards in their hand are not in other players hands
        """
        # ASSUMPTION: theres always three players
        kb = {
                self.player: True,
                self.other_players[0]: False,
                self.other_players[1]: False
             }

        for card in self.player.cards:
            self.knowledge[card] = kb


    def set_card_knowledge_of_individual(self, card, player):

        if not card in self.knowledge:
            s = "Trying to change knowledge of a card which does not exist in KB of " + self.player.name
            raise Exception(s)

        kb = {
                self.player: False,
                self.other_players[0]: False,
                self.other_players[1]: False
             }
        kb[player] = True
        self.knowledge[card] = kb