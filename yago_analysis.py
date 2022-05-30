import sys
from rdflib import Graph
import csv
from urllib.parse import urlparse
from rdflib.plugins.parsers.ntriples import ParseError
import re

SAMEAS = 'http://www.w3.org/2002/07/owl#sameAs'
SAMEAS_LITERAL = 'http://schema.org/sameAs'
EXACTMATCH = 'http://www.w3.org/2004/02/skos/core#exactMatch'

def validate_file(file):
    total_triples = 0
    sameas_triples = 0
    sameas_invalid = 0
    sameas_literal = 0
    sameas_literal_encoded = 0
    sameas_literal_invalid = 0

    with open(f"analysis_yago/{file.split('.')[0]}_fixed_triples.tsv", 'a') as out:
        tsv = csv.writer(out, delimiter='\t')
        tsv.writerow(['old triple', 'new triple'])

    with open(f"analysis_yago/{file.split('.')[0]}_extracted.nt", 'a') as extracted_file:
        with open(f"analysis_yago/{file.split('.')[0]}_invalid_lines.nt", 'a') as error_file:
            with open(file, 'r') as infile:
                for line in infile:
                    if '<' in line:
                        total_triples += 1
                        if SAMEAS in line:
                            try:
                                Graph().parse(data=line, format=FORMAT)
                                sameas_triples += 1
                                extracted_file.write(line)
                            except:
                                sameas_invalid += 1
                                error_file.write(line)
                        elif SAMEAS_LITERAL in line:
                            try:
                                Graph().parse(data=line, format=FORMAT)
                                sameas_literal += 1
                                extracted_file.write(line)
                            except ParseError:
                                fixed_line = re.search(r"<.*?>", line)
                                fixed_line = fixed_line.group(0)[1:-1]
                                fixed_line = urlparse(line).geturl()
                                try:
                                    Graph().parse(data=fixed_line, format=FORMAT)
                                    extracted_file.write(fixed_line)
                                    sameas_literal_encoded += 1
                                    with open(f"analysis_yago/{file.split('.')[0]}_fixed_triples.tsv", 'a') as out:
                                        tsv = csv.writer(out, delimiter='\t')
                                        tsv.writerow([line, fixed_line])
                                except ParseError:
                                    sameas_literal_invalid += 1
                                    error_file.write(line)
    print(f"{file} has {total_triples} total triples, {sameas_triples} http://www.w3.org/2002/07/owl#sameAs triples and, {sameas_invalid} of those triples are invalid and not added, and {sameas_literal} http://schema.org/sameAs triples, with an additional {sameas_literal_encoded} encoded triples. {sameas_literal_invalid} could not be encoded and not added")

FORMAT = sys.argv[1]

for file in sys.argv[2:]:
    validate_file(file)