import collections
import csv
import numpy
import math

def ingest_mdp(cells_filename, types_filename, genes_filename):
	data_table = get_states(cells_filename)
	types_list = get_vec(types_filename)
	genes_list = get_vec(genes_filename)

	data_dict = collections.defaultdict(set)
	gene_expression_dict = collections.defaultdict(list)
	rewards = collections.defaultdict(float)

	for i in range(0, len(data_table)):
		cell_type = types_list[i]
		cell_gene_profile = data_table[i]
		cell_gene_state = []
		for gene in genes_list:
			cell_gene_state.append(float(cell_gene_profile[gene]))
			gene_expression_dict[gene].append(float(cell_gene_profile[gene]))
		data_dict[cell_type].add((tuple(cell_gene_state), cell_type))

	spread_weights = compute_spread_weights(gene_expression_dict, genes_list)
	return (data_dict, genes_list, spread_weights)

def ingest_search(cells_filename, types_filename, genes_filename):
	data_table = get_states(cells_filename)
	types_list = get_vec(types_filename)
	genes_list = get_vec(genes_filename)

	data_dict = collections.defaultdict(set)
	gene_expression_dict = collections.defaultdict(list)

	for i in range(0, len(data_table)):
		cell_type = types_list[i]
		cell_gene_profile = data_table[i]
		cell_gene_state = []
		for gene in genes_list:
			cell_gene_state.append(float(cell_gene_profile[gene]))
			gene_expression_dict[gene].append(float(cell_gene_profile[gene]))
		data_dict[cell_type].add((tuple(cell_gene_state), cell_type))

	spread_weights = compute_spread_weights(gene_expression_dict, genes_list)
	transition_probabilities_dict = collections.defaultdict(dict)

	for cell_type, current_set in data_dict.iteritems():
		if cell_type == 'PS':
			next_set = data_dict['NP'].union(current_set)
		if cell_type == 'NP':
			next_set = data_dict['HF'].union(current_set)
		if cell_type == 'HF':
			next_set = data_dict['4G'].union(current_set)
			next_set = next_set.union(data_dict['4GF'])
		for cell_state in current_set:
			if cell_type == '4G' or cell_type == '4GF':
				next_set = {(cell_state[0], 'FATE')}
			else: 
				next_set.remove(cell_state)
			transitions = transition_probabilities(cell_state, next_set, spread_weights, genes_list)
			transition_probabilities_dict[cell_state] = transitions
			if cell_type != '4G' and cell_type != '4GF': next_set.add(cell_state)

	return (data_dict, genes_list, transition_probabilities_dict)

def get_states(cells_filename):
	data_table = []
	with open(cells_filename, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			row.pop('Cell') # remove cell name
			data_table.append(row)
	return data_table

def get_vec(vec_filename):
	info = []
	with open(vec_filename, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			info.append(row[0])
	return info

def compute_spread_weights(gene_expression_dict, genes_list):
	spread_dict = {}
	spread_weight = []

	# This takes every gene's expression value list and computes the standard deviation.
	for gene in genes_list:
		spread_weight.append(numpy.std(gene_expression_dict[gene]))

	# Normalize
	spread_weight = spread_weight/sum(spread_weight)

	# Convert into a dictionary for easy access
	for i in range(0, len(genes_list)):
		gene = genes_list[i]
		spread_dict[gene] = spread_weight[i]

	print(spread_dict)

	return spread_dict

# This function takes in the names of our two cells of interest and then computes a weighted euclidean distance. 
def inverse_distance(cell1, cell2, spread_weights, genes_list):
    dist_sum = 0
    for i in range(len(cell1)):
        alpha_i = spread_weights[genes_list[i]]
        dist_sum += ((cell1[i] - cell2[i])**2)/alpha_i
    dist_sum = 1 if dist_sum == 0 else dist_sum
    return 1/(math.sqrt(dist_sum))

def transition_probabilities(current_state, next_states_set, spread_weights, genes_list):
    inverse_distances = collections.defaultdict(float)
    for next_state in next_states_set:
        inverse_distances[next_state] = inverse_distance(current_state[0], next_state[0], spread_weights, genes_list)
    normalizer = sum(inverse_distances.itervalues())
    transition_probabilities = collections.defaultdict(float)
    for next_state, inverse_dist in inverse_distances.iteritems():
        transition_probabilities[next_state] = inverse_dist/normalizer
    return transition_probabilities