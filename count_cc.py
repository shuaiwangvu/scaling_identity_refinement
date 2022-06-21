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
opts.create_if_missing = True
opts.merge_operator = AssocCounter()
identity_set = rocksdb.DB("compacted_kg_identity_set_rocksdb.db", rocksdb.Options())
counter =  rocksdb.DB("count_cc_size_and_occurence.db", opts)
it = identity_set.iteritems()
it.seek_to_first()
for k,v in it:
    len_cc = len(v.decode().split())
    counter.merge(len_cc, b"1")

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
print("Time taken = ", time_formated)