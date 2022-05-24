"""
convert file from ttl to nt, will not check if triple is valid nt triple
"""
import sys
# %%
SAMEAS = 'http://www.w3.org/2002/07/owl#sameAs'
EXACTMATCH = 'http://www.w3.org/2004/02/skos/core#exactMatch'
files = ['wikidata-20220502-all-BETA.nt.gz']

# %%
def convert_to_nt(filename):
    print ('processing file ', filename)
    total_triples = 0
    sameas_triples = 0
    exactmatch_triples = 0
    new_file = open(f"converted_nt/{filename.split('.')[0]}.nt", 'a')
    with open(filename, 'r') as infile:
        for line in infile: 
            if '<' in line:
                total_triples += 1
                if SAMEAS in line:
                    sameas_triples += 1
                    new_file.write(line)
                elif EXACTMATCH in line:
                    exactmatch_triples += 1
                    new_file.write(line)
                if total_triples % 10000000 == 0:
                    print ('\tprocessed ', total_triples, ' lines')
        print(f"{filename} has {total_triples} total triples, {sameas_triples} owl:sameAs triples and, {exactmatch_triples} skos:exactMatch triples")
        new_file.close()

# %%
for file in sys.argv[1:]:
    convert_to_nt(file)