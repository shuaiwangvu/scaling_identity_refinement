import sys
from hdt import HDTDocument
from collections import Counter
import csv
import time
import rocksdb
from rocksdb.merge_operators import StringAppendOperator

for file in sys.argv[1:]:
    print(f'processing {file}')

    opts = rocksdb.Options()
    opts.create_if_missing = True
    opts.merge_operator = StringAppendOperator()
    identity_set = rocksdb.DB(f"{file.split('.')[0]}_identity_set_rocksdb.db", opts)
    mapping_IS = rocksdb.DB(f"{file.split('.')[0]}_mapping_IS_rocksdb.db", rocksdb.Options(create_if_missing=True))

    hdt_metalink = HDTDocument(file)
    start = time.time()
    unique_key = 0

    triples, _ = hdt_metalink.search_triples("", "", "")

    for (s, _, o) in triples:
        x = s.encode()
        y = o.encode()
        x_id = mapping_IS.get(x)
        y_id = mapping_IS.get(y)
        if not x_id and not y_id:
            mapping_IS.put(x, str(unique_key).encode())
            mapping_IS.put(y, str(unique_key).encode())
            identity_set.put(str(unique_key).encode(), x + b" " + y)
            unique_key += 1
        elif x_id and not y_id:
            mapping_IS.put(y, x_id)
            identity_set.merge(x_id, b" "+ y)
        elif not x_id and y_id:
            mapping_IS.put(x, y_id)
            identity_set.merge(y_id, b" " + x)
        elif x_id and y_id and x_id != y_id:
            IS_of_y = identity_set.get(y_id)
            identity_set.delete(y_id)
            identity_set.merge(x_id, b" " + IS_of_y)
            for mapping_key in IS_of_y.split():
                # mapping_IS.delete(mapping_key)
                mapping_IS.put(mapping_key, x_id)
    print("identity set:")
    it = identity_set.iteritems()
    it.seek_to_first()
    for k,v in it:
        print(f"{k} => {v}")
    print("mapping IS:")
    it = mapping_IS.iteritems()
    it.seek_to_first()
    for k,v in it:
        print(f"{k} => {v}")

    print(f'finished processing {file}')
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
    print("Time taken = ", time_formated)