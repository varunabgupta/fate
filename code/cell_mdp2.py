import collections
import math
import markov_util
import ingest_data
import random


class CellMDP(markov_util.MDP):
    def __init__(self, cells_file, types_file, genes_file):
        self.data, self.genes, self.spread_weights = ingest_data.ingest_mdp(cells_file, types_file, genes_file)

    # Return the start state.
    def startState(self):
        # return random.sample(self.data['HF'], 1)[0]  # sample a random starting PS state
        return (0, 'START')  

    # Return set of actions possible from |state|.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        cell_type = state[1]
        if cell_type == 'START':
            return ['Evolve']
        if cell_type == 'HF':
            return ['4G', '4GF']
        return ['Stay', 'Evolve']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        gene_profile, cell_type = state
        results = []

        # end states
        if cell_type == '4G' or cell_type == '4GF':
            return results

        if cell_type == 'START':
            next_states_set = self.data['PS']    
        elif action == 'Stay':
            next_states_set = self.data[cell_type]
            next_states_set.remove(state) # remove current state from next possible states
        elif cell_type == 'PS':
            next_states_set = self.data['NP']
        elif cell_type == 'NP':
            next_states_set = self.data['HF']
        elif cell_type == 'HF':
            if action == '4G':
                next_states_set = self.data['4G']
            if action == '4GF':
                next_states_set = self.data['4GF']\

        transition_probabilities, rewards = self.transition_probabilities_and_rewards(state, next_states_set)
        for next_state in transition_probabilities:
            results.append((next_state, transition_probabilities[next_state], rewards[next_state]))
        if cell_type != 'START' and action == 'Stay': next_states_set.add(state) # add back in 
        return results

    def transition_probabilities_and_rewards(self, current_state, next_states_set):
        inverse_distances = collections.defaultdict(float)
        rewards = collections.defaultdict(float)
        for next_state in next_states_set:
            inverse_distance, reward = self.inverse_distance(current_state[0], next_state[0]) if current_state[1] != 'START' else (1, 1)
            inverse_distances[next_state] = inverse_distance
            rewards[next_state] = reward #if (next_state[1] != '4G' and next_state[1] != '4GF') else reward * 2
        normalizer = sum(inverse_distances.itervalues())
        transition_probabilities = collections.defaultdict(float)
        for next_state, inverse_distance in inverse_distances.iteritems():
            transition_probabilities[next_state] = inverse_distance/normalizer
        return (transition_probabilities, rewards)

    # This function takes in the names of our two cells of interest and then computes a weighted euclidean distance. 
    def inverse_distance(self, cell1, cell2):
        dist_sum = 0
        endothelial_reward_sum = 0
        erythroid_reward_sum = 0
        endothelial_genes = [2, 5, 19, 40, 41]
        erythroid_genes = [13, 15, 16, 21, 32, 33]
        for i in range(len(cell1)):
            alpha_i = self.spread_weights[self.genes[i]]
            diff = cell2[i] - cell1[i]
            dist_sum += (diff**2)/alpha_i
            # endothelial_reward_sum = endothelial_reward_sum + alpha_i * cell2[i] if i in endothelial_genes else endothelial_reward_sum
            # erythroid_reward_sum = erythroid_reward_sum + alpha_i * cell2[i] if i in erythroid_genes else erythroid_reward_sum
            endothelial_reward_sum = endothelial_reward_sum + alpha_i * diff if i in endothelial_genes else endothelial_reward_sum
            erythroid_reward_sum = erythroid_reward_sum + alpha_i * diff if i in erythroid_genes else erythroid_reward_sum           
        return (1/(math.sqrt(dist_sum)), abs(endothelial_reward_sum - erythroid_reward_sum))

# Cdh5 2
# Erg 5
# Hoxb4 19
# Sox17 40
# Sox7 41

# Gata1  13
# Gf11b 15
# Hemoglob 16
# Ikaros 21
# Myb 32
# Nfe2 33

# reward abs(delta - delta)

# endothelial <- c("Cdh5", "Erg", "HoxB4", "Sox7", "Sox17")
# erythroid <- c("Gata1", "Gfi1b", "HbbbH1", "Ikaros", "Myb", "Nfe2")


    def discount(self):
        return 0.9
