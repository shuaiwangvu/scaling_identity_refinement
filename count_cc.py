import networkx as nx
import sys
from hdt import HDTDocument
from collections import Counter
import csv
import time

def check_two_cc(so, hdt_metalink):
    for el in so:
        triples, cardinality_s = hdt_metalink.search_triples(el, "", "")
        
        print(cardinality_s, [x for x in triples])
        if cardinality_s > 1:
            return False

        _, cardinality_o = hdt_metalink.search_triples("", "", el)
        if cardinality_o > 1:
            return False
    return True

for file in sys.argv[1:]:
    print(f'processing {file}')
    start = time.time()

    hdt_metalink = HDTDocument(file)
    triples, _ = hdt_metalink.search_triples("", "", "")

    G = nx.Graph()
    for (s, _, o) in triples:
        if check_two_cc([s,o], hdt_metalink):
            pass
        else:
            G.add_edge(s, o)

    print(f'nxconnectec_components: {[c for c in nx.connected_components(G)]}')
    cc = [len(c) for c in nx.connected_components(G)]
    cc = sorted(cc)

    with open(f"{file.split('.')[0]}_cc_count.tsv", 'w') as out:
        tsv = csv.writer(out, delimiter='\t')
        for key,value in Counter(cc).items():
            tsv.writerow([key, value])
            
    print(f'finished processing {file}: {Counter(cc)}')
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
    print("Time taken = ", time_formated)