import ingest_data
import csv
import collections
import math
import random
from ast import literal_eval as make_tuple

# def keywithmaxval(d):
#      """ a) create a list of the dict's keys and values; 
#          b) return the key with the max value"""  
#      v=list(d.values())
#      k=list(d.keys())
#      return k[v.index(max(v))]


# def transition_probabilities_and_rewards(current_state, next_states_set):
#     inverse_distances = collections.defaultdict(float)
#     rewards = collections.defaultdict(float)
#     for next_state in next_states_set:
#         calc_inverse_distance, reward = inverse_distance(current_state[0], next_state[0]) if current_state[1] != 'START' else (1, 1)
#         inverse_distances[next_state] = calc_inverse_distance
#         rewards[next_state] = reward #if (next_state[1] != '4G' and next_state[1] != '4GF') else reward * 2
#     normalizer = sum(inverse_distances.itervalues())
#     transition_probabilities = collections.defaultdict(float)
#     for next_state, calc_inverse_distance in inverse_distances.iteritems():
#         transition_probabilities[next_state] = calc_inverse_distance/normalizer
#     return (transition_probabilities, rewards)

# # This function takes in the names of our two cells of interest and then computes a weighted euclidean distance. 
# def inverse_distance(cell1, cell2):
#     dist_sum = 0
#     endothelial_reward_sum = 0
#     erythroid_reward_sum = 0
#     endothelial_genes = [2, 5, 19, 40, 41]
#     erythroid_genes = [13, 15, 16, 21, 32, 33]
#     for i in range(len(cell1)):
#         alpha_i = spread_weights[genes[i]]
#         diff = cell2[i] - cell1[i]
#         dist_sum += (diff**2)/alpha_i
#         # endothelial_reward_sum = endothelial_reward_sum + alpha_i * cell2[i] if i in endothelial_genes else endothelial_reward_sum
#         # erythroid_reward_sum = erythroid_reward_sum + alpha_i * cell2[i] if i in erythroid_genes else erythroid_reward_sum
#         endothelial_reward_sum = endothelial_reward_sum + alpha_i * diff if i in endothelial_genes else endothelial_reward_sum
#         erythroid_reward_sum = erythroid_reward_sum + alpha_i * diff if i in erythroid_genes else erythroid_reward_sum           
#     return (1/(math.sqrt(dist_sum)), abs(endothelial_reward_sum - erythroid_reward_sum))





data, genes, spread_weights = ingest_data.ingest_mdp('data/norm.csv', 'data/celltypes.txt', 'data/genes.txt')

cells_to_decisions = collections.defaultdict(str)
# cells_to_fates = collections.defaultdict(str)

with open('results/norm/optimal_policy_norm3.csv', 'r') as f:
    reader = csv.reader(f)    
    for row in reader:
        start_state = make_tuple(row[0])
        optimal_decision = row[1]
        cells_to_decisions[start_state] = optimal_decision

with open('results/norm/optimal_policy_transformed.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(genes + ['Decision'])
    for k,v in cells_to_decisions.iteritems():
        start_state, start_type = k
        if start_type != 'START':
            writer.writerow([i for i in start_state] + [v])

# for start_state, optimal_decision in cells_to_decisions.iteritems():
#     current_state = start_state
#     current_type = start_state[1]
#     current_decision = optimal_decision
#     stay_count = 0
#     while True:

#         print current_state
#         print current_decision 

#         if current_type == '4G' or current_type == '4GF':
#             cells_to_fates[start_state] = current_type
#             stay_count = 0
#             break
#         elif current_type == 'HF' and optimal_decision != 'Stay':
#             cells_to_fates[start_state] = current_decision
#             stay_count = 0
#             break
#         elif current_decision == 'Stay' and stay_count < 10:
#             stay_count += 1
#             next_states_set = data[current_type]
#             next_states_set.remove(current_state) # remove current state from next possible states
#         elif current_type == 'PS':
#             stay_count = 0
#             next_states_set = data['NP']
#         elif current_type == 'NP':
#             stay_count = 0
#             next_states_set = data['HF']

#         transition_probabilities, rewards = transition_probabilities_and_rewards(current_state, next_states_set)

#         if current_decision == 'Stay': 
#             next_states_set.add(current_state)
        
#         current_state = keywithmaxval(transition_probabilities)
#         current_type = current_state[1]
#         current_decision = cells_to_decisions[current_state]

# print cells_to_fates