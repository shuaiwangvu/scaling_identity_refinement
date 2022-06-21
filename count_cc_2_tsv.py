from ast import Assert
import csv
import time
import rocksdb

start = time.time()
class AssocCounter(rocksdb.interfaces.AssociativeMergeOperator):
    def merge(self, key, existing_value, value):
        if existing_value:
            s = int(existing_value) + int(value)
            return (True, str(s).encode())
        return (True, value)

    def name(self):
        return b'AssocCounter'

opts = rocksdb.Options()
opts.merge_operator = AssocCounter()
identity_set =  rocksdb.DB("count_cc_size_and_occurence.db", opts)
it = identity_set.iteritems()
it.seek_to_first()
with open('size_cc_2_number_of_occurences.tsv', 'w') as out:
    tsv = csv.writer(out, delimiter="\t")
    for k,v in it:
        tsv.writerow([k.decode(),v.decode()])