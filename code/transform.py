import csv
import collections
from ast import literal_eval as make_tuple

start_to_result = collections.defaultdict(str)

with open('results/norm/actions_norm.csv', 'r') as f:
    reader = csv.reader(f)    
    for row in reader:
        start_state, start_type = make_tuple(row[0])
        end_state, end_type = make_tuple(row[-2])
        start_to_result[start_state] = end_type

with open('results/norm/transformed_norm.csv', 'w') as f:
    writer = csv.writer(f)
    for k,v in start_to_result.iteritems():
        writer.writerow(k + (v,))
