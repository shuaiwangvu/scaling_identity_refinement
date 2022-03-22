from rdflib import Graph, URIRef
import os
sameas = 'http://www.w3.org/2002/07/owl#sameAs'


file_info = {"commons-sameas-links_lang=en.ttl.bz2": "dbpedia/databus/2021.12.01/commons-sameas-links_lang=en.ttl.bz2"}



new_g = Graph()
def count_triples(path, format):
	g = Graph()

	try:
		g.parse(path, format=format)
	except Exception as e:
		print('error on file: ', file)
		print ('Exception  = ', e)
		return

	count = 0
	for s,p,o in g.triples((None, URIRef(sameas), None)):
		if p.toPython() == sameas:
			count = count + 1
			new_g.add((s,p,o))
	print(path, " has ", len(g), " triples and ", count , " amount of sameAs triples")

# files= [
# 'identity_links/commons-sameas-links_lang=es.ttl','identity_links/commons-sameas-links_lang=ja.ttl',
# 'identity_links/commons-sameas-links_lang=pt.ttl','identity_links/commons-sameas-links_lang=nl.ttl',
# 'identity_links/commons-sameas-links_lang=de.ttl','identity_links/commons-sameas-links_lang=en.ttl',
# 'identity_links/commons-sameas-links_lang=fr.ttl','identity_links/commons-sameas-links_lang=ja-1.ttl',
# 'identity_links/commons-sameas-links_lang=es-1.ttl','identity_links/commons-sameas-links_lang=de-1.ttl',
# 'identity_links/commons-sameas-links_lang=en-1.ttl','identity_links/commons-sameas-links_lang=fr-1.ttl',
# 'identity_links/commons-sameas-links_lang=pt-1.ttl','identity_links/commons-sameas-links_lang=nl-1.ttl',
# ]

#files I skipped: 'identity_links/yago-wd-sameAs.nt',
files = ['identity_links/sameas-external.ttl', 'identity_links/sameas-all-wikis.ttl', 'mappingbased-objects-uncleaned.ttl']

for file in files:
	if 'finn' in os.getcwd():
		file = '/home/nasim/data/' + file
	count_triples(file, file.split(".")[-1])

new_g.serialize(destination="identity_graph.ttl")
