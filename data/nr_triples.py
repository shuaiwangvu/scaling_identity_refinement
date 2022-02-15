from rdflib import Graph, URIRef

sameas = 'http://www.w3.org/2002/07/owl#sameAs'
def count_triples(path):
    g = Graph()
    g.parse(path, format="ttl")
    
    count = 0
    for _,p,_ in g.triples((None, URIRef(sameas), None)):
        if p.toPython() == sameas:
            count = count + 1
    print(path, " has ", len(g), " triples and ", count , " amount of sameAs triples")

path = 'sameas-external.ttl'
count_triples(path)