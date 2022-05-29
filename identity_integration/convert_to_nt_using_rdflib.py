"""
convert file from ttl to nt using rdflib (parser will load entire file into memory, not useful for large files)
"""
from rdflib import Graph
import sys

SAMEAS = 'http://www.w3.org/2002/07/owl#sameAs'
SAMEAS_1 = 'http://schema.org/sameAs'
EXACTMATCH = 'http://www.w3.org/2004/02/skos/core#exactMatch'


def count_triples_and_serialize(path):
	new_g = Graph()
	g = Graph()

	g.parse(path)
	

	count_owl = 0
	count_skos = 0

	for s,p,o in g.triples((None, None, None)):
		if p.toPython() == SAMEAS or p.toPython() == SAMEAS_1:
			count_owl += 1
			new_g.add((s,p,o))
		elif p.toPython() == EXACTMATCH:
			count_skos += 1
			new_g.add((s,p,o))

	print(path, " has ", len(g), " triples and ", count_owl , " amount of sameAs triples,", count_skos , " amount of skos:exacthMatch triples")
	new_g.serialize(destination = f"converted_nt/{file.split('.')[0]}.nt", format="nt11", encoding='utf-8')

files = sys.argv[1:]
for file in files:
	count_triples_and_serialize(file)
