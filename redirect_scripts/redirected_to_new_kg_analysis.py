import networkx as nx
import pickle
import argparse
import rocksdb
import csv
import time

# function that checks if a string is a key in db 13658


def is_key(node):
    # remove the \n at the end of the string
    raw_node = node
    node = node[:-1]
    key = db.get(node.encode())
    if key:
        redirected_to_new_kg.add(node)
    elif db.get(raw_node.encode()):
        redirected_to_new_kg(raw_node)
    


parser = argparse.ArgumentParser()
parser.add_argument("graph", help="path to graph pickle file")
parser.add_argument("rocksdbfile", help="rocksdb mapping IS")
parser.add_argument("out", help="entities that are in the new kg")
args = parser.parse_args()

start = time.time()
db = rocksdb.DB(args.rocksdbfile, rocksdb.Options(create_if_missing=False))

redirected_to_new_kg = set()
redi_graph = pickle.load(open(args.graph, "rb"))
for n in redi_graph.nodes():
    if redi_graph.nodes[n]['remark'] == 'found_without_redirect':
        is_key(n)
    elif redi_graph.nodes[n]['remark'] == 'redirect_until_timeout':
        is_key(n)
    elif redi_graph.nodes[n]['remark'] == 'redirect_until_not_found':
        is_key(n)
    elif redi_graph.nodes[n]['remark'] == 'redirect_until_error':
        is_key(n)
    elif redi_graph.nodes[n]['remark'] == 'redirect_until_found':
        is_key(n)

with open(args.out, 'w', encoding='utf-8') as out:
    writer = csv.writer(out)
    for el in redirected_to_new_kg:
        writer.writerow([el])
print(f"wrote {len(redirected_to_new_kg)}")
print(f'finished processing')
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(
    int(hours), int(minutes), seconds)
print("Time taken = ", time_formated)
