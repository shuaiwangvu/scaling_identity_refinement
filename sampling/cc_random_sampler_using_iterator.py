import random
import csv
import argparse
import rocksdb
# open a csv file without loading it all in memory
# sample n lines of the csv file without duplicates and writes them to a new csv file
# uses commandline arguments for input file and output file

parser = argparse.ArgumentParser()

parser.add_argument("input_file", help="input file")

parser.add_argument("output_file", help="output file")

parser.add_argument("n", help="number of lines to sample")

parser.add_argument("identity_set", help="identity set rocksdb")

parser.add_argument("mapping_is", help="mapping identity set rocksdb")

args = parser.parse_args()

identity_set = rocksdb.DB(args.identity_set, rocksdb.Options(create_if_missing=False))
mapping_IS = rocksdb.DB(args.mapping_is, rocksdb.Options(create_if_missing=False))

def check_cc_size(l):
    mapping_index = mapping_IS.get(l[0].encode())
    len_cc = len(identity_set.get(mapping_index).decode().split())
    return len_cc

# randomly replace an element in a list with a new elemnt


def replace_random_element(l, e):
    index = random.randint(0, len(l) - 1)
    l[index] = e
    return l

# sample large csv file without loading the entire file into memory
def sample_large_csv(input_file, output_file, n):
    with open(input_file, "r") as f:
        results_2 = []
        results_3_9 = []
        results_10 = []
        reader = csv.reader(f)
        for _ in range(n):
            entity = next(reader)
            CC = check_cc_size(entity)
            if CC == 2:
                if len(results_2) == n:
                    results_2 = replace_random_element(results_2, entity)
                else:
                    results_2.append(entity)
            if CC > 2 and CC <= 10:
                if len(results_3_9) == n:
                    results_3_9 = replace_random_element(results_3_9, entity)
                else:
                    results_3_9.append(entity)
            if CC > 10:
                if len(results_10) == n:
                    results_10 = replace_random_element(results_10, entity)
                else:
                    results_10.append(entity)

        random.shuffle(results_2)
        random.shuffle(results_3_9)
        random.shuffle(results_10)
        
        reader = csv.reader(f)
        for i, v in enumerate(reader, n):
            r = random.randint(0, i)
            if r < n:
                CC = check_cc_size(v)
                if CC == 2:
                    if len(results_2) == n:
                        results_2 = replace_random_element(results_2, v)
                    else:
                        results_2.append(v)
                if CC > 2 and CC <= 10:
                    if len(results_3_9) == n:
                        results_3_9 = replace_random_element(results_3_9, v)
                    else:
                        results_3_9.append(v)
                if CC > 10:
                    if len(results_10) == n:
                        results_10 = replace_random_element(results_10, v)
                    else:
                        results_10.append(v)
        
        with open(f"output_file_2", "w") as f2:
            writer = csv.writer(f2)
            writer.writerows(results_2)
        with open(f"output_file_3_9", "w") as f2:
            writer = csv.writer(f2)
            writer.writerows(results_3_9)
        with open(f"output_file_10", "w") as f2:
            writer = csv.writer(f2)
            writer.writerows(results_10)


sample_large_csv(args.input_file, args.output_file, int(args.n))
