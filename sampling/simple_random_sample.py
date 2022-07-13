import argparse
import random
import pandas
import time

def get_options():
    parser = argparse.ArgumentParser(description="rocksDB_keys2csv: iterates through all keys in a database, and writes them to a csv file")
    parser.add_argument("-f", "--file",
                        help="input file (required)", required=True)
    parser.add_argument("-o", "--output-file",
                        help="output file (required)", required=True)
    parser.add_argument("-n", "--number-of-samples",
                        type=int, default=100000, help="number of samples to write (default=100000)")
    parser.add_argument("-m", "--max-size",
                        help="number of records in file (required)", required=True)                   
    args = parser.parse_args()
    return args

options = get_options()

start = time.time()

n = options.max_size #number of records in file
s = options.number_of_samples #desired sample size
filename = options.file
skip = sorted(random.sample(range(n),n-s))
df = pandas.read_csv(filename, skiprows=skip)

df.to_csv(options.output_file, index=False)

print(f'finished processing')
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
print("Time taken = ", time_formated)
