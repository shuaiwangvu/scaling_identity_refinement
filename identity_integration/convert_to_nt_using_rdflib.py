from rdflib import Graph, URIRef

sameas = 'http://www.w3.org/2002/07/owl#sameAs'
exactmatch = 'http://www.w3.org/2004/02/skos/core#exactMatch'


def count_triples(path, new_g):
	g = Graph()

	g.parse(path, format="turtle", encoding='utf-8')
	

	count_owl = 0
	count_skos = 0

	for s,p,o in g.triples((None, None, None)):
		if p.toPython() == sameas:
			count_owl += 1
			new_g.add((s,p,o))
		elif p.toPython() == exactmatch:
			count_skos += 1
			new_g.add((s,p,o))
	print(path, " has ", len(g), " triples and ", count_owl , " amount of sameAs triples,", count_skos , " amount of skos:exacthMatch triples")

files = ["commons-sameas-links_lang=de.ttl","commons-sameas-links_lang=en.ttl","commons-sameas-links_lang=es.ttl","commons-sameas-links_lang=fr.ttl","commons-sameas-links_lang=ja.ttl",
"commons-sameas-links_lang=nl.ttl","commons-sameas-links_lang=pt.ttl","sameas-all-wikis.ttl","sameas-external.ttl"]
for file in files:
	new_g = Graph()
	count_triples(file, new_g)
	new_g.serialize(destination = f"converted_nt/{file.split('.')[0]}.nt", format="nt11", encoding='utf-8')
