# kg        433443217       433,443,217
# old kg    179739567       179,739,567

import argparse
import random
import rocksdb
import pandas
import datetime as dt

def get_options():
    parser = argparse.ArgumentParser(description="samples CC(2), CC(3-10), CC(>10) for N samples each. requires term2id and id2terms first.")
    parser.add_argument("-f", "--file",
                        help="input file (required)", required=True)
    parser.add_argument("-o", "--output-file",
                        help="output file (required)", required=True)
    parser.add_argument("-i", "--identity-set",
                        help="filepath to the rocksdb identity set (required)", required=True)
    parser.add_argument("-m", "--mapping-is",
                        help="filepath to the mapping to the identity set (required)", required=True)
    parser.add_argument("-n", "--number-of-samples",
                        type=int, default=100000, help="number of samples to write (default=100000)")
    parser.add_argument("-d", "--dataset-size",
                        type=int, help="number of records in file (required)", required=True)                   
    args = parser.parse_args()
    return args

def random_sample(input_file, sample_size, max_lines_file, identity_set, mapping_is):
    sample_two = set()
    sample_Between_3_and_10 = set()
    sample_larger_than_ten = set()
    
    identity_set = rocksdb.DB(identity_set, rocksdb.Options(create_if_missing=False))
    mapping_IS = rocksdb.DB(mapping_is, rocksdb.Options(create_if_missing=False))

    if sample_size > max_lines_file:
        raise Exception("Sample nr exceeds maxsize")
    
    while not(len(sample_two) == len(sample_Between_3_and_10) == len(sample_larger_than_ten) == sample_size):
        skip = sorted(random.sample(range(max_lines_file), max_lines_file-(sample_size*3)))
        df = pandas.read_csv(input_file, skiprows=skip)

        for _, row in df.iterrows():
            mapping_index = mapping_IS.get(row[0].encode())
            len_cc = len(identity_set.get(mapping_index).decode().split())

            if len_cc == 2 and len(sample_two) < sample_size:
                sample_two.add(row[0])
            elif len_cc > 2 and len_cc <= 10 and len(sample_Between_3_and_10) < sample_size:
                sample_Between_3_and_10.add(row[0])
            elif len_cc > 10 and len(sample_larger_than_ten) < sample_size:
                sample_larger_than_ten.add(row[0])

    return list(sample_two), list(sample_Between_3_and_10), list(sample_larger_than_ten)

options = get_options()
input_file = options.file
out_file = options.output_file
max_lines_file = options.dataset_size
sample_size = options.number_of_samples
identity_set = options.identity_set
mapping_is = options.mapping_is

sampling_metadata_two, sampling_metadata_Between_3_and_10, sampling_metadata_larger_than_ten = random_sample(input_file, sample_size, max_lines_file, identity_set, mapping_is)

start = dt.datetime.now()
sample_id = str(start.timestamp()).replace(".", "")

sample_fn = "{}".format("sample_{}_two.nt".format(sample_id))
with open(sample_fn, "w+") as file:
    for entity in sampling_metadata_two:
         file.write(entity+'\n')

sample_fn = "{}".format("sample_{}_Between_3_and_10.nt".format(sample_id))
with open(sample_fn, "w+") as file:
    for entity in sampling_metadata_Between_3_and_10:
         file.write(entity+'\n')

sample_fn = "{}".format("sample_{}_larger_than_ten.nt".format(sample_id))
with open(sample_fn, "w+") as file:
    for entity in sampling_metadata_larger_than_ten:
         file.write(entity+'\n')
