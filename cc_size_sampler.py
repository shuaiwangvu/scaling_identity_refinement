# Util functions from Lars H. https://github.com/Lars-H/hdt_sampler

import rocksdb
import sys
from hdt import HDTDocument
import random
from rdf_utils import tuple_to_triple, tuple_to_ntriple
import datetime as dt

class AppendEntity(rocksdb.interfaces.AssociativeMergeOperator):
    def merge(self, key, existing_value, value):
        if existing_value:
            s = existing_value + b' ' + value
            return (True, s)
        return (True, value)

    def name(self):
        return b'AppendEntity'

def random_sample(file, size):
    count_cc_two = 0
    count_cc_Between_3_and_10 = 0
    count_cc_larger_than_ten = 0
    identity_set = rocksdb.DB("compacted_kg_identity_set_rocksdb.db", rocksdb.Options(merge_operator=AppendEntity()))
    mapping_IS = rocksdb.DB("compacted_kg_mapping_IS_rocksdb.db", rocksdb.Options(create_if_missing=False))

    (_, cardinality) = file.search_triples("", "", "")
    sample_two = set()
    sample_Between_3_and_10 = set()
    sample_larger_than_ten = set()
    
    entities = set()

    if size > cardinality:
        raise Exception("Sample size exceeds dataset size")
    while True:
        offset = random.randint(0, cardinality - 1)
        (triples, _) = file.search_triples("", "", "", limit=1, offset=offset)
        triple = next(triples)
        s,_,o = triple

        if not s in entities or not o in entities:
            idx = mapping_IS.get(s.encode())
            len_cc = len(identity_set.get(idx).decode().split())

            if len_cc == 2 and count_cc_two < size:
                count_cc_two += 1
                sample_two.add(tuple_to_triple(triple))
            elif len_cc > 2 and len_cc <= 10 and count_cc_Between_3_and_10 < size:
                count_cc_Between_3_and_10 += 1
                sample_Between_3_and_10.add(tuple_to_triple(triple))
            elif len_cc > 10 and count_cc_larger_than_ten < size:
                count_cc_larger_than_ten += 1
                sample_larger_than_ten.add(tuple_to_triple(triple))
            
            if count_cc_two == count_cc_Between_3_and_10 == count_cc_larger_than_ten == size:
                return list(sample_two), list(sample_Between_3_and_10), list(sample_larger_than_ten)
    

FILENAME = sys.argv[1]
MAX_ENTITIES = int(sys.argv[2])

sampling_dataset = HDTDocument(FILENAME)
sampling_metadata_two, sampling_metadata_Between_3_and_10, sampling_metadata_larger_than_ten = random_sample(sampling_dataset, MAX_ENTITIES)

start = dt.datetime.now()
sample_id = str(start.timestamp()).replace(".", "")

sample_fn = "{}".format("sample_{}_two.nt".format(sample_id))
with open(sample_fn, "w+") as file:
    for triple in sampling_metadata_two:
         file.write(tuple_to_ntriple(triple))

sample_fn = "{}".format("sample_{}_Between_3_and_10.nt".format(sample_id))
with open(sample_fn, "w+") as file:
    for triple in sampling_metadata_Between_3_and_10:
         file.write(tuple_to_ntriple(triple))

sample_fn = "{}".format("sample_{}_larger_than_ten.nt".format(sample_id))
with open(sample_fn, "w+") as file:
    for triple in sampling_metadata_larger_than_ten:
         file.write(tuple_to_ntriple(triple))