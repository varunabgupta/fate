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
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        cell_type = state(1)
        if cell_type == 'HF':
            return ['Stay', '4G', '4GF']
        return ['Stay', 'Evolve']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        gene_profile, cell_type = state

        if cell_type == '4G' or cell_type == '4GF':
            return []

        results = []
        if action == 'Stay':
            next_states_set = self.data[cell_type]
            next_states_set.remove(state) # remove current state from next possible states
            transition_probabilities = self.transition_probabilities(state, next_states_set)
            for next_state, transition_probability in transition_probabilities.iteritems():
                results.append((next_state, transition_probability, 1))
            next_states_set.add(state) # add back in
            return results

        # Evolve case, modify later to be systematic and generalized
        if state == 'PS':
            return results
        if state == 'NP':
            return results
        if state == 'HF':
            if action == '4G':
                return results
            if action == '4GF':
                return results

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
