# iterate through a rocksDB term2id file and write to a csv file

import argparse
import rocksdb
import csv

def get_options():
    parser = argparse.ArgumentParser(description="rocksDB_keys2csv: iterates through all keys in a database, and writes them to a csv file")
    parser.add_argument("-f", "--file",
                        help="input file (required)", required=True)
    parser.add_argument("-o", "--output-file",
                        help="output file (required)", required=True)
    args = parser.parse_args()
    return args

options = get_options()

db = rocksdb.DB(options.file, rocksdb.Options(create_if_missing=False))
it = db.iterkeys()
it.seek_to_first()

with open(options.output_file, 'w') as output_file:
    writer = csv.writer(output_file)
    for key in it:
        writer.writerow(key)
