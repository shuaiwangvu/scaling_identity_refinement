from hdt import HDTDocument
"""
install 
https://github.com/RDFLib/rdflib-hdt
https://github.com/RDFLib/rdflib-hdt

"""

sameas = 'http://www.w3.org/2002/07/owl#sameAs'
differentFrom = 'https://www.w3.org/2002/07/owl#differentFrom'
exactMatch = 'http://www.w3.org/2004/02/skos/core#exactMatch'

def count_triples(path):
    hdt_lod = HDTDocument(path)

    triples, cardinality_sameas = hdt_lod.search_triples("", sameas, "")
    triples, cardinality_differentFrom = hdt_lod.search_triples("", differentFrom, "")
    triples, cardinality_exactMatch = hdt_lod.search_triples("", exactMatch, "")
    triples, cardinality_total = hdt_lod.search_triples("", "", "")

    print("count of owl:sameAs triples: \n", cardinality_sameas)
    print("count of owl:differentFrom triples: \n", cardinality_differentFrom)
    print("count of skos:exactMatch triples: \n", cardinality_exactMatch)
    print("count of total triples: \n", cardinality_total)

count_triples("integrated.hdt")

# PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
# count_triples(PATH_LOD)