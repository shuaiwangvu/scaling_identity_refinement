import networkx as nx
import sys
from hdt import HDTDocument
from collections import Counter
import csv
import time

def check_two_cc(so, hdt_metalink):
    for el in so:
        _, cardinality_s = hdt_metalink.search_triples(el, "", "")
        if cardinality_s > 1:
            return False

        _, cardinality_o = hdt_metalink.search_triples("", "", el)
        if cardinality_s + cardinality_o > 1:
            return False
    return True

for file in sys.argv[1:]:
    print(f'processing {file}')
    start = time.time()

    hdt_metalink = HDTDocument(file)
    triples, _ = hdt_metalink.search_triples("", "", "")

    G = nx.Graph()
    cc_for_two = []
    for (s, _, o) in triples:
        if check_two_cc([s,o], hdt_metalink):
            cc_for_two.append(2)
        else:
            G.add_edge(s, o)

    cc = [len(c) for c in nx.connected_components(G)]
    cc = cc_for_two + cc
    cc = sorted(cc)

    with open(f"{file.split('.')[0]}_cc_count.tsv", 'w') as out:
        tsv = csv.writer(out, delimiter='\t')
        tsv.writerow(['connected component size', 'number of occurences'])
        for key,value in Counter(cc).items():
            tsv.writerow([key, value])
            
    print(f'finished processing {file}: {Counter(cc)}')
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
    print("Time taken = ", time_formated)