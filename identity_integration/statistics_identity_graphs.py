from rdflib import Graph, URIRef

sameAs = 'http://www.w3.org/2002/07/owl#sameAs'
seeAlso= 'https://www.w3.org/TR/rdf-schema/#ch_seealso'

def count_triples(path, format):
    g = Graph().parse(path, format=format)

    count_sameAs = 0
    count_seeAlso = 0 #test commit

    for _,_,_ in g.triples((None, URIRef(sameAs), None)):
        count_sameAs += 1
    for _,_,_ in g.triples((None, URIRef(seeAlso), None)):
        count_seeAlso += 1

    print(path, " has ", len(g), " triples and ", count_sameAs , " amount of sameAs triples and ", count_seeAlso, " rdf seeAlso triples.")

files= ['commons-sameas-links_lang=nl.ttl']

for file in files:
    count_triples(file, file.split(".")[-1])