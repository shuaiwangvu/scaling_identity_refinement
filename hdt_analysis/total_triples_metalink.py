from hdt import HDTDocument

# Load an HDT file.
# Missing indexes are generated automatically, add False as the second argument to disable them
PATH_META = "/home/jraad/ssd/data/identity/metalink/metalink.hdt"
#PATH_META = "integrated.hdt"
document = HDTDocument(PATH_META)

# Display some metadata about the HDT document itself
print("nb triples: %i" % document.total_triples)
print("nb subjects: %i" % document.nb_subjects)
print("nb predicates: %i" % document.nb_predicates)
print("nb objects: %i" % document.nb_objects)
print("nb shared subject-object: %i" % document.nb_shared)

triples, cardinality = document.search_triples("", "", "")

print("nb triples (through search_triples): ", cardinality)