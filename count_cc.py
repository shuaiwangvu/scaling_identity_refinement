import networkx as nx
import sys
from hdt import HDTDocument
from collections import Counter
import csv
import time

for file in sys.argv[1:]:
    print(f'processing {file}')
    start = time.time()

    hdt_metalink = HDTDocument(file)
    triples, _ = hdt_metalink.search_triples("", "", "")

    G = nx.Graph()
    for (s, _, o) in triples:
        G.add_edge(s, o)

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