import gzip, sys
# %%
SAMEAS = b'http://www.w3.org/2002/07/owl#sameAs'
EXACTMATCH = b'http://www.w3.org/2004/02/skos/core#exactMatch'
SAMEAS_LITERAL = b'http://schema.org/sameAs'
# %%
def convert_to_nt(filename):
    print ('processing file ', filename)

    total_triples = 0
    sameas_triples = 0
    exactmatch_triples = 0
    sameas_literal_triples = 0

    with gzip.open("extracted_wikidata_doublechecked.nt.gz", 'ab') as new_file:
        with gzip.open(filename) as infile:
            for line in infile: 
                if b'<' in line:
                    total_triples += 1
                    
                    if SAMEAS in line:
                        sameas_triples += 1
                        new_file.write(line)
                    elif SAMEAS_LITERAL in line:
                        sameas_literal_triples += 1
                        new_file.write(line)
                        with gzip.open("extracted_wikidata_literals.nt.gz", 'ab') as literal_file:
                            literal_file.write(line)
                    elif EXACTMATCH in line:
                        exactmatch_triples += 1
                        new_file.write(line)
                    if total_triples % 10000000 == 0:
                        print ('\tprocessed ', total_triples, ' lines')
                        
            print(f"{filename} has {total_triples} total triples, {sameas_triples} owl:sameAs triples and, {exactmatch_triples} skos:exactMatch triples and, {sameas_literal_triples} schema sameAs triples")

# %%
for file in sys.argv[1:]:
    convert_to_nt(file)

