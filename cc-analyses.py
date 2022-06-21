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

opts = rocksdb.Options()
opts.merge_operator = AppendEntity()
with rocksdb.DB("compacted_kg_identity_set_rocksdb.db", opts) as identity_set:
    it = identity_set.iteritems()
    it.seek_to_first()
    with open('id2terms.tsv', 'w') as out:
        tsv = csv.writer(out, delimiter="\t")
        for k,v in it:
            tsv.writerow([k.decode(),v.decode()])
        
with rocksdb.DB("compacted_kg_mapping_IS_rocksdb.db", rocksdb.Options()) as mapping_IS:
    it = mapping_IS.iteritems()
    it.seek_to_first()
    with open('terms2id.tsv', 'w') as out:
        tsv = csv.writer(out, delimiter="\t")
        for k,v in it:
            tsv.writerow([k.decode(),v.decode()])

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
print("Time taken = ", time_formated)