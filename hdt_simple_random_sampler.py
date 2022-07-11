# Util functions from Lars H. https://github.com/Lars-H/hdt_sampler

# import rocksdb
import sys
from hdt import HDTDocument
import random
from rdf_utils import tuple_to_triple, tuple_to_ntriple
import datetime as dt

def random_sample(file, size):
    (_, cardinality) = file.search_triples("", "", "")
    sample = set()
    entities = set()
    if size > cardinality:
        raise Exception("Sample size exceeds dataset size")
    while len(sample) < size:
        offset = random.randint(0, cardinality - 1)
        triples, _ = file.search_triples("", "", "", limit=1, offset=offset)
        triple = next(triples)
        s,_,o = triple
        if not s in entities or not o in entities:
            sample.add(tuple_to_triple(triple))
            entities.add(s)
            entities.add(o)

    return list(sample)

FILENAME = sys.argv[1]
MAX_ENTITIES = int(sys.argv[2])

sampling_dataset = HDTDocument(FILENAME)
sampling_metadata = random_sample(sampling_dataset, MAX_ENTITIES)

start = dt.datetime.now()
sample_id = str(start.timestamp()).replace(".", "")
sample_fn = "{}".format("sample_{}.nt".format(sample_id))

with open(sample_fn, "w+") as file:
    for triple in sampling_metadata:
         file.write(tuple_to_ntriple(triple))