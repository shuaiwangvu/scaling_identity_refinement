#count the nr of triples with no uniqueID from the file indicated by PATH_META
from hdt import HDTDocument

rdf_subject = "http://www.w3.org/1999/02/22-rdf-syntax-ns#subject"
rdf_object = "http://www.w3.org/1999/02/22-rdf-syntax-ns#object"

count_none = 0
PATH_META = "/home/jraad/ssd/data/identity/metalink/metalink.hdt"
hdt_metalink = HDTDocument(PATH_META)

def find_statement_id(subject, object):
    triples_statement_id_regarding_subject, cardinality_statement_id_regarding_subject = hdt_metalink.search_triples("", rdf_subject, subject)
    collect_statement_id_regarding_subject = set()

    for (s,_,o) in triples_statement_id_regarding_subject:
        collect_statement_id_regarding_subject.add(str(s))
    
    triples_statement_id_regarding_object, cardinality_statement_id_regarding_object = hdt_metalink.search_triples("", rdf_object, object)
    collect_statement_id_regarding_object = set()

    for (s,_,o) in triples_statement_id_regarding_object:
        collect_statement_id_regarding_object.add(str(o))

    inter_section = collect_statement_id_regarding_subject.intersection(collect_statement_id_regarding_object)

    if len(inter_section) == 1:
        return inter_section
    else:
        return None

triples, cardinality = hdt_metalink.search_triples("", "", "")

for (s, _, o) in triples:
    id = find_statement_id(s,o)
    if id == None:
        count_none += 1
    else:
        pass

print("nr of triples without an id", count_none)