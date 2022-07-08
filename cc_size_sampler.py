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
    (_, CARD) = file.search_triples("", "", "")
    cardinality = CARD
    sample = set()
    if size > CARD:
        raise Exception("Sample size exceeds dataset size")
    while 1:
        offset = random.randint(0, cardinality - 1)
        (triples, res_card) = file.search_triples("", "", "", limit=1, offset=offset)
        spo = next(triples)
        s,_,_ = spo
        idx = mapping_IS.get(s.encode())
        len_cc = len(identity_set.get(idx).decode().split())
        if len_cc == 2 and count_cc_two < size:
            count_cc_two += 2
            sample.add(tuple_to_triple(spo))
        elif len_cc > 2 and len_cc <= 10 and count_cc_Between_3_and_10 < size:
            count_cc_Between_3_and_10 += 2
            sample.add(tuple_to_triple(spo))
        elif len_cc > 10 and count_cc_larger_than_ten < size:
            count_cc_larger_than_ten += 2
            sample.add(tuple_to_triple(spo))
        
        if count_cc_two == count_cc_Between_3_and_10 == count_cc_larger_than_ten == size:
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