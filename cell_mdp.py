class CellMDP(util.MDP):
    def __init__(self, cells_file, types_file, genes_file, discount):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.data, self.genes = ingest(cells_file, types_file, genes_file)
        self.discount = discount

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        cell_type = state(1)
        if cell_type == 'HF':
            return ['Stay', '4G', '4GF']
        if cell_type == '4G' or cell_type == '4GF':
            return ['Stay']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        total_card_value_in_hand, next_card_index_if_peeked, deck_card_counts = state

        if deck_card_counts is None:
            return []

        if action == 'Quit':
            return [((total_card_value_in_hand, None, None), 1, total_card_value_in_hand)]

        if action == 'Peak' and next_card_index_if_peeked is not None:
            return []

        if action == 'Take' and next_card_index_if_peeked is not None:
            card_value = self.cardValues[next_card_index_if_peeked]
            if total_card_value_in_hand + card_value > self.threshold:
                return [((total_card_value_in_hand + card_value, None, None), 1, 0)]
            else:
                deck_card_counts_list = list(deck_card_counts)
                deck_card_counts_list[next_card_index_if_peeked] -= 1
                if sum(deck_card_counts_list) > 0:
                    return [((total_card_value_in_hand + card_value, None, tuple(deck_card_counts_list)), 1, 0)]
                else:
                    return [((total_card_value_in_hand + card_value, None, None), 1, total_card_value_in_hand + card_value)]

        total_num_cards = float(sum(deck_card_counts))
        probabilities = [deck_card_counts[card_index]/total_num_cards for card_index in range(len(self.cardValues))]
        if action == 'Peek' and next_card_index_if_peeked is None:
            return [((total_card_value_in_hand, peeked_index, deck_card_counts), probabilities[peeked_index], -1 * self.peekCost) for peeked_index in range(len(self.cardValues)) if probabilities[peeked_index] > 0] 

        results = []
        for card_index in range(len(self.cardValues)):
            if probabilities[card_index] > 0:
                card_value = self.cardValues[card_index]
                if total_card_value_in_hand + card_value > self.threshold:
                    results.append(((total_card_value_in_hand + card_value, None, None), probabilities[card_index], 0))
                else:
                    deck_card_counts_list = list(deck_card_counts)
                    deck_card_counts_list[card_index] -= 1
                    if sum(deck_card_counts_list) > 0:
                        results.append(((total_card_value_in_hand + card_value, None, tuple(deck_card_counts_list)), probabilities[card_index], 0))
                    else:
                        results.append(((total_card_value_in_hand + card_value, None, None), probabilities[card_index], total_card_value_in_hand + card_value))
      
        return results
        # END_YOUR_CODE

    def discount(self):
        return self.discount
