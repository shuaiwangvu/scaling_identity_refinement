from rdflib import Graph, URIRef

sameas = 'http://www.w3.org/2002/07/owl#sameAs'
exactmatch = 'http://www.w3.org/2004/02/skos/core#exactMatch'


def count_triples(path):
	g = Graph()

	g.parse(path, format="turtle")
	

	count_owl = 0
	count_skos = 0
	for s,p,o in g.triples((None, URIRef(sameas), None)):
		if p.toPython() == sameas:
			count_owl += 1
			new_g.add((s,p,o))
		elif p.toPython() == exactmatch:
			count_skos += 1
			new_g.add((s,p,o))
	print(path, " has ", len(g), " triples and ", count_owl , " amount of sameAs triples", count_skos , " amount of skos:exacthMatch triples")

files = ["commons-sameas-links_lang=nl", 'commons-sameas-links_lang=es', 'commons-sameas-links_lang=de', 'commons-sameas-links_lang=fr', 'commons-sameas-links_lang=pt',
'commons-sameas-links_lang=en','commons-sameas-links_lang=ja']
format = ".ttl"
for file in files:
	new_g = Graph()
	count_triples(f"{file}{format}")
	new_g.serialize(destination=f"converted_nt/{file}.nt", format="nt")
