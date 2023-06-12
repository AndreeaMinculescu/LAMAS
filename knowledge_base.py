from card import Card


class KnowledgeBase:
    """
    Class to store the knowledge base of an agent
    KB is a dictionary of dictionaries. For each card possible (52) in a deck keep track of who has the card
    """
    def __init__(self, player, other_players, all_cards:list[Card]):
        # player is the agent from which perspective the kb is built
        self.player = player
        # other_players are the other two player
        self.other_players = other_players
        # all_cards is a list of all 52 cards
        self.all_cards = all_cards
        # knowledge is the kb dictionary
        self.knowledge = {}
        # discard_cards is a set of all discarded cards so far
        self.discard_cards = set()
        
        for c in self.all_cards:
            # ASSUMPTIONS:
            # 1) there are always three players
            # 2) in the beginning (before looking at your own cards and cards on table) the agent assumes that the other
            # agents have all cards not in the player's hand, until information pointing to the contrary becomes
            # available
            kb = {
                    self.player.name: None,
                    self.other_players[0].name: None,
                    self.other_players[1].name: None
                 }

            self.knowledge[(c.suit, c.value)] = kb

        # initialize knowledge base
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
        Function that updates the kb of the player according to the following assumptions:
        player knows that 1) cards on the table are in no ones hands, 2) cards in discard pile are in no ones hand,
        and 3) cards not on the table, not in player's hand and not in the discard pile are in someone's hand possibly
        :param self: the knowledge base of the player
        :return: None
        """
        # ASSUMPTION: there are always three players
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

        # cards not on the table, not in the players hands and not in discard pile can be in anyone's but the
        # player's hand
        remainder_cards = list(set([(i.suit,i.value) for i in self.all_cards]) -
                               set([(i.suit,i.value) for i in self.player.cards]) -
                               set([(i.suit,i.value) for i in self.player.table]) -
                               set(self.discard_cards))
        for card in self.all_cards:
            if (card.suit, card.value) in remainder_cards:
                self.knowledge[(card.suit, card.value)] = kb1

    def update_discard_pile(self, discards):
        """
        Update knowledge about what goes in the discarded pile, equivalent to seeing the table cards being changed
        :param self: the knowledge base of the player
        :param discards: a list of discarded cards
        :return: None
        """

        kb = {
                self.player.name: False,
                self.other_players[0].name: False,
                self.other_players[1].name: False
             }
        # no one has cards which are in discard pile
        for card in discards:
            self.knowledge[(card.suit, card.value)] = kb
            self.discard_cards.add((card.suit, card.value))

    def set_knowledge_own_deck(self):
        """
        Function that updates the kb of the player according to the following assumption:
        player knows the cards in their hand are not in other models' hands
        :param self: the knowledge base of the player
        :return: None
        """
        # ASSUMPTION: there are always three players
        kb = {
                self.player.name: True,
                self.other_players[0].name: False,
                self.other_players[1].name: False
             }
        # the cards in the player's hand are not in other models' hands
        for card in self.player.cards:
            self.knowledge[(card.suit, card.value)] = kb

    def set_card_knowledge_of_individual(self, card, player):
        """
        Change the knowledge of a given card for a given player, equivalent to seeing someone pick up a card
        :param self: the knowledge base of the player
        :param card: card that was picked from the table
        :param player: agent that picked the card
        :return: None
        """
        if (card.suit, card.value) not in self.knowledge.keys():
            s = f"Trying to change knowledge of a {(card.value, card.suit)} which does not exist in KB of " + self.player.name
            raise Exception(s)

        kb = {
                self.player.name: False,
                self.other_players[0].name: False,
                self.other_players[1].name: False
             }

        kb[player.name] = True
        self.knowledge[(card.suit, card.value)] = kb

    def set_discard_knowledge(self, card):
        """
        Change the knowledge of a given card for a given player, equivalent to seeing someone discard a card
        :param self: the knowledge base of the player
        :param card: card that was discorded from the table
        :return: None
        """
        if (card.suit, card.value) not in self.knowledge.keys():
            s = "Trying to change knowledge of a card which does not exist in KB of " + self.player.name
            raise Exception(s)

        # discarded cards go on table so no-one has them
        kb = {
                self.player.name: False,
                self.other_players[0].name: False,
                self.other_players[1].name: False
             }

        self.knowledge[(card.suit, card.value)] = kb

    def check_players_have_number(self, value):
        """
        Check to see if the other players are collecting a certain value
        :param self: the knowledge base of the player
        :param value: the value
        :return: True if the other players are collecting the value, False otherwise
        """
        
        for c, kb in self.knowledge.items():
            if c[1] == value:
                # ... if another player has value
                print(f"{c}: {kb}")
                p1 = kb[self.other_players[0].name]
                p2 = kb[self.other_players[1].name]

                if p1 and p2:
                    return True

        return False
