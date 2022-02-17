from rdflib import Graph, URIRef

sameas = 'http://www.w3.org/2002/07/owl#sameAs'

new_g = Graph()
def count_triples(path, format):
    g = Graph()

    try:
        g.parse(path, format=format)
    except:
        print('error on file: ', file)
        return

    count = 0
    for s,p,o in g.triples((None, URIRef(sameas), None)):
        if p.toPython() == sameas:
            count = count + 1
            new_g.add((s,p,o))
    print(path, " has ", len(g), " triples and ", count , " amount of sameAs triples")

files= ['yago-wd-sameAs.nt','sameas-external.ttl','commons-sameas-links_lang=es.ttl',
'commons-sameas-links_lang=ja.ttl','commons-sameas-links_lang=pt.ttl',
'commons-sameas-links_lang=nl.ttl','commons-sameas-links_lang=de.ttl',
'commons-sameas-links_lang=en.ttl','commons-sameas-links_lang=fr.ttl',
'sameas-all-wikis.ttl','commons-sameas-links_lang=ja-1.ttl',
'commons-sameas-links_lang=es-1.ttl','commons-sameas-links_lang=de-1.ttl',
'commons-sameas-links_lang=en-1.ttl','commons-sameas-links_lang=fr-1.ttl',
'commons-sameas-links_lang=pt-1.ttl','commons-sameas-links_lang=nl-1.ttl',
'sameas-external-1.ttl']

for file in files:
    count_triples(file, file.split(".")[-1])

new_g.serialize(destination="total_identity_links.ttl")