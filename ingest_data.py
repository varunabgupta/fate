import collections
import csv
import numpy

def ingest(cells_filename, types_filename, genes_filename):
	data_table = get_states(cells_filename)
	types_list = get_vec(types_filename)
	genes_list = get_vec(genes_filename)
	data_dict = collections.defaultdict(set)
	for i in range(0, len(data_table)):
		cell_type = types_list[i]
		cell_gene_profile = data_table[i]
		cell_gene_state = []
		for gene in genes_list:
			cell_gene_state.append(cell_gene_profile[gene])
		data_dict[cell_type].add((tuple(cell_gene_state), cell_type))
	return (data_dict, genes_list)

# THERE IS A BUG HERE: when iterating through, it treats the "Cell" column, the first one, as a gene and adds its value accordingly. 
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

def normalize_spread(cells_filename,genes_filename):
	data_table = get_states(cells_filename)
	genes_list = get_vec(genes_filename)

	# This initializes our gene expression dictionary, which will map each gene to a list of all expression values in our data set.
	gene_expression_dict = {}
	for gene in genes_list:
		gene_expression_dict[gene] = []

	# This loops through each cell in our data table, loops through each gene in each cell, and then adds the gene expression value to the gene expression dictionary for each gene. 
	for i in range(0, len(data_table)):
		cell = data_table[i]
		for gene in cell:
			# Can remove this once bug is fixed #
			if gene != "Cell":
				gene_expression_dict[gene].append(float(cell[gene]))
	return compute_spread_weights(gene_expression_dict,genes_list)

def compute_spread_weights(gene_expression_dict,genes_list):
	spread_dict = {}
	spread_weight = []

	# This takes every gene's expression value list and computes the standard deviation.
	for gene in gene_expression_dict:
		value_set = gene_expression_dict[gene]
		spread_weight.append(numpy.std(value_set))

	# Normalize
	spread_weight = spread_weight/sum(spread_weight)

	# Convert into a dictionary for easy access
	for i in range(0, len(genes_list)):
		gene = genes_list[i]
		spread_dict[gene] = spread_weight[i]

	return spread_dict


















