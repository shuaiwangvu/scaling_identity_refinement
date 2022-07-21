import networkx as nx
import pickle
import argparse

#arguments for graph input
parser = argparse.ArgumentParser()
parser.add_argument("graph", help="path to graph pickle file")
args = parser.parse_args()
redi_graph = pickle.load(open(args.graph, "rb"))
count_redirected_nodes = 0
for n in redi_graph.nodes():
    if redi_graph.nodes[n]['remark'] == 'redirect_until_timeout':
        count_redirected_nodes += 1
    elif redi_graph.nodes[n]['remark'] == 'redirect_until_not_found':
        count_redirected_nodes += 1
    elif redi_graph.nodes[n]['remark'] == 'redirect_until_error':
        count_redirected_nodes += 1
    elif redi_graph.nodes[n]['remark'] == 'redirect_until_found':
        count_redirected_nodes += 1
print(f"redirected node {count_redirected_nodes}")