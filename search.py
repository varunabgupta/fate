from cell_search import CellSearch
from search_util import UniformCostSearch
import csv
import ingest_data
import collections
import json

cells_file = 'norm.csv'
types_file = 'celltypes.txt'
genes_file = 'genes.txt'

data, genes, transitions = ingest_data.ingest(cells_file, types_file, genes_file)

num_states_explored = collections.defaultdict(int)
total_cost = collections.defaultdict(float)
actions = collections.defaultdict(list)

for cell_type in data:
    if cell_type != '4G' and cell_type != '4GF':
        for starting_state in data[cell_type]:
            cs = CellSearch(data, genes, transitions, starting_state)
            ucs = UniformCostSearch(verbose = 1)
            ucs.solve(cs)
            num_states_explored[starting_state] = ucs.numStatesExplored
            total_cost[starting_state] = ucs.totalCost
            actions[starting_state] = ucs.actions

# json.dump(num_states_explored, open('num_states_explored.json', 'w'))
# json.dump(total_cost, open('total_cost.json', 'w'))
# json.dump(actions, open('actions.json', 'w'))

with open('num_states_explored_norm.csv', 'w') as f:
    writer = csv.writer(f)    
    for k,v in num_states_explored.iteritems():
        writer.writerow([k] + [v])

with open('total_cost_norm.csv', 'w') as f:
    writer = csv.writer(f)    
    for k,v in total_cost.iteritems():
        writer.writerow([k] + [v])

with open('actions_norm.csv', 'w') as f:
    writer = csv.writer(f)    
    for k,v in actions.iteritems():
        writer.writerow([k] + v)