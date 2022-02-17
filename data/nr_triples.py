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

files= [
'identity_links/commons-sameas-links_lang=es.ttl','identity_links/commons-sameas-links_lang=ja.ttl',
'identity_links/commons-sameas-links_lang=pt.ttl','identity_links/commons-sameas-links_lang=nl.ttl',
'identity_links/commons-sameas-links_lang=de.ttl','identity_links/commons-sameas-links_lang=en.ttl',
'identity_links/commons-sameas-links_lang=fr.ttl','identity_links/commons-sameas-links_lang=ja-1.ttl',
'identity_links/commons-sameas-links_lang=es-1.ttl','identity_links/commons-sameas-links_lang=de-1.ttl',
'identity_links/commons-sameas-links_lang=en-1.ttl','identity_links/commons-sameas-links_lang=fr-1.ttl',
'identity_links/commons-sameas-links_lang=pt-1.ttl','identity_links/commons-sameas-links_lang=nl-1.ttl',
]

for file in files:
    count_triples(file, file.split(".")[-1])

new_g.serialize(destination="identity_graph.nt")

g = Graph().parse('identity_graph.nt', format='nt')

count_sameAs = 0
for _,_,_ in g.triples((None, URIRef(sameAs), None)):
    count_sameAs += 1
print('identity_graph.nt has ', len(g), " triples and ", count_sameAs , " amount of sameAs triples")