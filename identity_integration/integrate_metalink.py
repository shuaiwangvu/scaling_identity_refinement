# %%
from rdflib import Graph, URIRef

# %%
rdf_subject = "http://www.w3.org/1999/02/22-rdf-syntax-ns#subject"
rdf_object = "http://www.w3.org/1999/02/22-rdf-syntax-ns#object"
max_id = 0
new_graph = Graph()
FILES = ["commons-sameas-links_lang=en.ttl"]
DESTINATION = "extending_metalink.ttl"
# %%
def find_statement_id(subject, object, g):
    collect_statement_id_regarding_subject = set()
    for s,_,_ in g.triples((None, URIRef(rdf_subject), subject)):
        collect_statement_id_regarding_subject.add(str(s))

    collect_statement_id_regarding_object = set()
    for s,_,_ in g.triples((None, URIRef(rdf_object), object)):
        collect_statement_id_regarding_object.add(str(s))
    
    inter_section = collect_statement_id_regarding_subject.intersection(collect_statement_id_regarding_object)

    if len(inter_section) == 1:
        return list(inter_section)[0]
    else:
        return None

# Iterates through all triples
# checks if there already is a statement id 
# otherwise, all two triples <max_id> rdf_subject <subject> and <max_id> rdf_object <object>
# max_id += 1
# %%
def create_metalink_data(path, format):
    global max_id

    try:
        g = Graph().parse(path, format=format)
    except:
        print('error on file: ', path)
        exit(-1)

    for s,_,o in g:
        id = find_statement_id(s, o, g)
        if id != None: 
            print(str(s) + " " + str(o) + " already in metalink form")
            continue

        new_id = URIRef("metalink/extended/id/" + str(max_id))
        new_graph.add((new_id, URIRef(rdf_subject), s))
        new_graph.add((new_id, URIRef(rdf_object), o))
        max_id += 1
        if (max_id == 999): break

# %%
for file in FILES:
    print("extending metalink for file " + file)
    create_metalink_data(file, file.split(".")[-1])

# %%
print("done, serializing graph to " + DESTINATION)
new_graph.serialize(destination=DESTINATION)


