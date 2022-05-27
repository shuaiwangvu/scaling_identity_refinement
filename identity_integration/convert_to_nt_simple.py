"""
convert file from ttl to nt, will check if triple is valid nt triple, invalid triples are ignored
first arg for rdf format (nt11 for nt 1.1)
rest args are files for processing
"""
import sys
from rdflib import Graph
from rdflib.plugins.parsers.ntriples import ParseError

SAMEAS = 'http://www.w3.org/2002/07/owl#sameAs'
EXACTMATCH = 'http://www.w3.org/2004/02/skos/core#exactMatch'
FORMAT = sys.argv[1]

def convert_to_nt(filename):
    print ('processing file ', filename)

    total_triples = 0
    sameas_triples = 0
    exactmatch_triples = 0
    invalid_triples = 0

    with open(f"converted_nt/{filename.split('.')[0]}.nt", 'a') as new_file:
        with open(filename, 'r') as infile:
            for line in infile:
                try: 
                    if '<' in line:
                        if SAMEAS in line:
                            Graph().parse(data=line, format=FORMAT)
                            sameas_triples += 1
                            new_file.write(line)
                        elif EXACTMATCH in line:
                            Graph().parse(data=line, format=FORMAT)
                            exactmatch_triples += 1
                            new_file.write(line)
                        total_triples += 1
                        if total_triples % 10000000 == 0:
                            print ('\tprocessed ', total_triples, ' lines')
                except ParseError:
                    invalid_triples += 1
            print(f"{filename} has {total_triples} total triples, {sameas_triples} owl:sameAs triples and, {exactmatch_triples} skos:exactMatch triples, and {invalid_triples} invalid triples")



for file in sys.argv[2:]:
    convert_to_nt(file)