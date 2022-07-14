import argparse
import random
import pandas
import time

def get_options():
    parser = argparse.ArgumentParser(description="samples N lines from a file")
    parser.add_argument("-f", "--file",
                        help="input file (required)", required=True)
    parser.add_argument("-o", "--output-file",
                        help="output file (required)", required=True)
    parser.add_argument("-n", "--number-of-samples",
                        type=int, default=100000, help="number of samples to write (default=100000)")
    parser.add_argument("-d", "--dataset-size",
                        type=int, help="number of records in file (required)", required=True)                   
    args = parser.parse_args()
    return args

start = time.time()

options = get_options()
in_file = options.file
out_file = options.output_file
max_lines = options.dataset_size
sample_size = options.number_of_samples

if sample_size > max_lines:
    raise Exception("Sample nr exceeds maxsize")

sample = set()

while len(sample) < sample_size:
    skip = sorted(random.sample(range(max_lines), max_lines-sample_size))
    df = pandas.read_csv(in_file, skiprows=skip)
    for _, row in df.iterrows():
        sample.add(row[0])

with open(out_file, "w+") as file:
    for entity in sample:
         file.write(entity+'\n')

print(f'finished processing')
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
print("Time taken = ", time_formated)
