import sys
from hdt import HDTDocument
from collections import Counter
import csv
import time
import dbm

for file in sys.argv[1:]:
    print(f'processing {file}')
    mapping_IS = dbm.open(f"{file.split('.')[0]}_mapping_IS.db", 'c')
    identity_set = dbm.open(f"{file.split('.')[0]}_identity_set.db", 'c')
    hdt_metalink = HDTDocument(file)
    start = time.time()
    unique_key = 0

    triples, _ = hdt_metalink.search_triples("", "", "")

    for (x, _, y) in triples:
        str_unique_key = str(unique_key)
        x_id = mapping_IS.get(x)
        y_id = mapping_IS.get(y)
        if not x_id and not y_id:
            mapping_IS[x] = str_unique_key
            mapping_IS[y] = str_unique_key
            identity_set[str_unique_key] = " ".join([x, y])
            unique_key += 1
        elif x_id and not y_id:
            mapping_IS[y] = x_id
            identity_set[x_id] = " ".join([identity_set[x_id].decode(), y])
        elif not x_id and y_id:
            mapping_IS[x] = y_id
            identity_set[y_id] = " ".join([identity_set[y_id].decode(), x])
        elif x_id and y_id and x_id != y_id:
            identity_set[x_id] = " ".join([identity_set[x_id].decode(), identity_set[y_id].decode()])
            for el in identity_set[y_id].split():
                mapping_IS[el] = x_id
            del identity_set[y_id]
    identity_set.close()
    mapping_IS.close()
      
    print(f'finished processing {file}')
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
    print("Time taken = ", time_formated)