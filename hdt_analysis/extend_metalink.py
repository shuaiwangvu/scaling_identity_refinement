#count the nr of triples with no uniqueID from the file indicated by PATH_META
from hdt import HDTDocument

rdf_subject = "http://www.w3.org/1999/02/22-rdf-syntax-ns#subject"
rdf_object = "http://www.w3.org/1999/02/22-rdf-syntax-ns#object"

count_none = 0
max_id = 0
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
        collect_statement_id_regarding_object.add(str(s))

    inter_section = collect_statement_id_regarding_subject.intersection(collect_statement_id_regarding_object)

    if len(inter_section) == 1:
        return list(inter_section)[0]
    else:
        return None

triples, cardinality = hdt_metalink.search_triples("", "", "")

#first loop check for the maxID, what if there is no triple with a id?
for (s, _, o) in triples:
    id = find_statement_id(s,o)
    if (id > max_id):
        max_id = int(id.split("/")[-1])

#second loop extends the metalink
for (s, _, o) in triples:
    max_id += 1
    id = find_statement_id(s,o)
    if id == None:
        #add new triples here?
        #https://docs.google.com/document/d/1ruA1xGLNn0SG8vORaZaeRcAMFLy55Pa9_EL9rAGi1Lg/edit#
        md5 = 'https://krr.triply.cc/krr/metalink/fileMD5/' + str(max_id) #need to pass the max_id through a md5 generator first?
        #new graph.add(md5, rdf_subject, s) 
        #new graph.add(md5, rdf_object, o)
        #nothing with the predicate? or do we assume everything is sameAs?
        #eventually more meta Data