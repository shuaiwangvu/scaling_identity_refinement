import csv
import argparse
import rocksdb
import time

# open two rocksdb files and check how many keys overlap
# write the overlapped lines to a new csv file
# use argparse for the input and output files
def main():
    # start timer
    start = time.time()
    parser = argparse.ArgumentParser(
        description='Finds overlaps between two rocksdb files')
    parser.add_argument('db1', help='first rocksdb file')
    parser.add_argument('db2', help='second rocksdb file')
    parser.add_argument('out', help='output file')
    args = parser.parse_args()

    db1 = rocksdb.DB(args.db1, rocksdb.Options(create_if_missing=False))
    db2 = rocksdb.DB(args.db2, rocksdb.Options(create_if_missing=False))

    count_overlap = 0
    with open(args.out, 'w', encoding='utf-8') as out:
        writer = csv.writer(out)
        it = db1.iteritems()
        it.seek_to_first()
        for key, _ in it:
            if db2.get(key):
                count_overlap += 1
                writer.writerow([key.decode()])
        
    print(f"{count_overlap} entities")
    # print how long the program took to run in hours minutes and seconds
    print(f'finished processing')
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
    print("Time taken = ", time_formated)

main()
