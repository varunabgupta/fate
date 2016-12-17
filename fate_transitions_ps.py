import csv
import collections
import ingest_data
import pprint
from ast import literal_eval as make_tuple

type_chain = {
    'PS': ['NP'],
    'NP': ['HF'],
    'HF': ['4G', '4GF']
}

fate_classes_diffs = collections.defaultdict(dict)

_, genes_list, spread_weights = ingest_data.ingest_mdp('data/raw.csv', 'data/celltypes.txt', 'data/genes.txt')

with open('results/norm/actions_norm.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        current_state, current_type = make_tuple(row[0])
        end_state, end_type = make_tuple(row[-2])
        if current_type == 'PS':
            for ele in row:
                next_types = type_chain[current_type]
                ele_state, ele_type = make_tuple(ele)
                if ele_type in next_types:
                    diffs = [spread_weights[genes_list[i]] * (ele_state[i] - current_state[i]) for i in range(len(ele_state))]
                    if current_type in fate_classes_diffs[end_type]:
                        fate_classes_diffs[end_type][current_type].append(diffs)
                    else:
                        fate_classes_diffs[end_type][current_type] = [diffs]
                    current_state = ele_state
                    current_type = ele_type
                    if ele_type == '4G' or ele_type == '4GF': break

with open('results/norm/fate_transitions_ps_norm.csv', 'w') as f:
    writer = csv.writer(f)
    for fate, start_to_diffs in fate_classes_diffs.iteritems():
        for start, diffs in start_to_diffs.iteritems():
            pprint.pprint(start)
            sum_diffs = [0] * len(diffs[0])
            for list_diff in diffs:
                for i in range(len(list_diff)):
                    sum_diffs[i] += list_diff[i]
            # normalize
            avg_diffs = []
            for sum_diff in sum_diffs:
                avg_diffs.append(sum_diff/len(diffs))

            writer.writerow([fate] + [start] + avg_diffs)
