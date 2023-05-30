class Agent:
  
    def __init__(self, cards, table):
        # cards is a list of 4 card objects 
        self.cards = cards
        # table is a list of 6 card objects on the table
        self.table = table

    def greedy_strategy():
        """
        Find the most common number in all the cards visible to 
        the agent (their cards and the cards on table) and then 
        pick up the same number from the pile on the table otherwise
        don't do anything. If there are multiple common numbers take the 
        first one.
        """

        card_values = [i.value for i in self.cards]
        table_values = [i.vale for i in self.table]

        all_values = card_values + table_values

        # most frequent number visible to you
        most_freq = max(set(all_values), key=all_values.count)

        for card in self.table:
            if most_freq == card.value:

                # do swap 





