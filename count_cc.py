import csv
import time
import rocksdb

start = time.time()
class AppendEntity(rocksdb.interfaces.AssociativeMergeOperator):
    def merge(self, key, existing_value, value):
        if existing_value:
            s = existing_value + b' ' + value
            return (True, s)
        return (True, value)

    def name(self):
        return b'AppendEntity'

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
identity_set = rocksdb.DB("compacted_kg_identity_set_rocksdb.db", rocksdb.Options(merge_operator=AppendEntity()))
counter =  rocksdb.DB("count_cc_size_and_occurence.db", opts)
it = identity_set.iteritems()
it.seek_to_first()
for k,v in it:
    len_cc = len(v.decode().split())
    counter.merge(str(len_cc).encode(), b"1")

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
print("Time taken = ", time_formated)