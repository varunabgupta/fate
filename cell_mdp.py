import collections
import csv
import numpy
from ingest_data import ingest,get_states,get_vec,normalize_spread


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
        self.spread_weights = normalize_spread(cells_file, genes_file):

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
        return ['Stay', 'Evolve']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        gene_profile, cell_type = state

        if cell_type == '4G' or cell_type == '4GF':
            return []

        return []
        # END_YOUR_CODE

    def transition_probabilities(self, current_state, next_states_set):
        inverse_distances = collections.defaultdict(float)
        for next_state in next_states_set:
            inverse_distances[next_state] = self.transition_probability(current_state[0], next_state[0])
        normalizer = sum(inverse_distances.itervalues())
        transition_probabilities = collections.defaultdict(float)
        for next_state, inverse_distance in inverse_distances.iteritems():
            transition_probabilities[next_state] = inverse_distance/normalizer
        return transition_probabilities

    # This function takes in the names of our two cells of interest and then computes a weighted euclidean distance. 
    def transition_probability(self, cell1, cell2):
        spread_weights = self.spread_weights
        cell_dict = self.cell_dict

        dist_sum = 0
        for i in range(len(cell1)):
            alpha_i = spread_weights[self.genes[i]]
            dist_sum += ((cell1[i] - cell2[i])**2)/alpha_i

        return 1/(numpy.sqrt(dist_sum))


    def discount(self):
        return self.discount
