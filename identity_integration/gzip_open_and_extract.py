"""
parses gzip files and extracts sameAs and exactMatch to a new gzip file (alos counts the amount)
"""
import gzip, sys
# %%
SAMEAS = b'http://www.w3.org/2002/07/owl#sameAs'
EXACTMATCH = b'http://www.w3.org/2004/02/skos/core#exactMatch'

# %%
def convert_to_nt(filename):
    print ('processing file ', filename)

    total_triples = 0
    sameas_triples = 0
    exactmatch_triples = 0

    with gzip.open("extracted_wikidata.nt.gz", 'ab') as new_file:
        with gzip.open(filename) as infile:
            for line in infile: 
                if b'<' in line:
                    total_triples += 1
                    if SAMEAS in line:
                        sameas_triples += 1
                        new_file.write(line)
                    elif EXACTMATCH in line:
                        exactmatch_triples += 1
                        new_file.write(line)
                    if total_triples % 10000000 == 0:
                        print ('\tprocessed ', total_triples, ' lines')
            print(filename + " has " + total_triples + " total triples, " + sameas_triples + " owl:sameAs triples and, " + exactmatch_triples + " skos:exactMatch triples")

# %%
for file in sys.argv[1:]:
    convert_to_nt(file)