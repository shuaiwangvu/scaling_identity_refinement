"""
uses rdflib parser to validate rdf triples
argument 1 is the format specified by rdflib e.g., 'nt11'
argument 2+ are the files you wish to validate
"""
import sys
from rdflib import Graph
import rdflib

def validate_file(file):
    count_lines = 0
    with open(file, 'r') as infile:
        for line in infile:
            count_lines += 1
            try:
                Graph().parse(data=line, format=FORMAT)            
            except rdflib.plugins.parsers.ntriples.ParseError as e:
                print(f"error in line {count_lines}: {e}")

FORMAT = sys.argv[1]

for file in sys.argv[2:]:
    validate_file(file)