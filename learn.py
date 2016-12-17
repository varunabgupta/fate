from cell_mdp2 import CellMDP
from markov_util import ValueIteration
import csv

mdp = CellMDP('data/raw.csv', 'data/celltypes.txt', 'data/genes.txt')
value_iteration = ValueIteration()
value_iteration.solve(mdp, epsilon = 1)

with open('results/norm/optimal_policy_norm3.csv', 'w') as f:
    writer = csv.writer(f)
    for k,v in value_iteration.pi.iteritems():
        writer.writerow([k] + [v])

with open('results/norm/optimal_values_norm3.csv', 'w') as f:
    writer = csv.writer(f)
    for k,v in value_iteration.V.iteritems():
        writer.writerow([k] + [v])