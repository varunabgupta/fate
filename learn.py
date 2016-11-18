from cell_mdp import CellMDP
from markov_util import ValueIteration

mdp = CellMDP('raw.csv', 'celltypes.txt', 'genes.txt')
value_iteration = ValueIteration()
value_iteration.solve(mdp, epsilon = 0.01)
print(value_iteration.pi)