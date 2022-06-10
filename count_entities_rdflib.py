import rdflib
import sys
import time
"""
arg 1 = format for rdflib nt11, turtle, etc.
arg 2, .., N = files to count unique entities
"""
FORMAT = sys.argv[1]

for file in sys.argv[2:]:
    print(f"processing {file}")
    start = time.time()
    g = rdflib.Graph().parse(file, FORMAT)
    
    entities = set()
    for (s,_,o) in g.triples((None,None,None)):
        entities.add(s.toPython())
        entities.add(o.toPython())
    print(f"{file} has {len(entities)} entities.")
    
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
