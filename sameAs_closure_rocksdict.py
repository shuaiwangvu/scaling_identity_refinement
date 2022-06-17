import sys
from hdt import HDTDocument
from collections import Counter
import csv
import time
from rocksdict import Rdict, Options

for file in sys.argv[1:]:
    print(f'processing {file}')
    mapping_IS = Rdict(f"{file.split('.')[0]}_mapping_IS.db", Options(create_if_missing=True))
    identity_set = Rdict(f"{file.split('.')[0]}_identity_set.db", Options(create_if_missing=True))
    hdt_metalink = HDTDocument(file)
    start = time.time()
    unique_key = 0

    triples, _ = hdt_metalink.search_triples("", "", "")

    for (x, _, y) in triples:
        x_id = mapping_IS[x]
        y_id = mapping_IS[y]
        if not x_id and not y_id:
            mapping_IS[x] = unique_key
            mapping_IS[y] = unique_key
            identity_set[unique_key] = [x, y]
            unique_key += 1
        elif x_id and not y_id:
            mapping_IS[y] = x_id
            identity_set[x_id] = identity_set[x_id].append(y) # update mapping when creating new identity sets
        elif not x_id and y_id:
            mapping_IS[x] = y_id
            identity_set[y_id] = identity_set[y_id].append(x)
        elif x_id and y_id and x_id != y_id:
            identity_set[x_id] = identity_set[x_id].extend(identity_set[y_id])
            for el in identity_set[y_id]:
                mapping_IS[el] = x_id
            del identity_set[y_id]
    print('identity set:')
    for k, v in identity_set.items():
        print(f"{k} -> {v}")
    print('mapping_IS:')
    for k, v in mapping_IS.items():
        print(f"{k} -> {v}")
    identity_set.close()
    mapping_IS.close()
      
    print(f'finished processing {file}')
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
    print("Time taken = ", time_formated)