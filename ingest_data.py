import collections
import csv

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

def get_states(cells_filename):
	data_table = []
	with open(cells_filename, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			data_table.append(row)
	return data_table

def get_vec(vec_filename):
	info = []
	with open(vec_filename, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			info.append(row[0])
	return info
