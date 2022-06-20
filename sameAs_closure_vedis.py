import sys
from hdt import HDTDocument
from collections import Counter
import csv
import time
from vedis import Vedis

for file in sys.argv[1:]:
    print(f'processing {file}')
    hdt_metalink = HDTDocument(file)
    start = time.time()
    unique_key = 0

    triples, _ = hdt_metalink.search_triples("", "", "")
    with Vedis(f"{file.split('.')[0]}_mapping_IS_vedis.db", "c") as mapping_IS:
        with Vedis(f"{file.split('.')[0]}_identity_set_vedis.db", "c") as identity_set:
            for (x, _, y) in triples:
                x_id, y_id = mapping_IS.mget([x,y])

                if not x_id and not y_id:
                    mapping_IS[x] = str(unique_key)
                    mapping_IS[y] = str(unique_key)
                    identity_set[str(unique_key)] = " ".join([x,y])
                    unique_key += 1
                elif x_id and not y_id:
                    mapping_IS[y] = x_id
                    identity_set.append(x_id, " " + y)
                elif not x_id and y_id:
                    mapping_IS[x] = y_id
                    identity_set.append(y_id, " " + x)
                elif x_id and y_id and x_id != y_id:
                    identity_set.append(x_id, " " + identity_set[y_id])
                    for el in identity_set[y_id]:
                        del mapping_IS[el]
                        mapping_IS[el] = x_id
                    del identity_set[y_id]
    print('identity set:')
    for k, v in identity_set.items():
        print(f"{k} -> {v}")
    print('mapping_IS:')
    for k, v in mapping_IS.items():
        print(f"{k} -> {v}")
      
    print(f'finished processing {file}')
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
    print("Time taken = ", time_formated)