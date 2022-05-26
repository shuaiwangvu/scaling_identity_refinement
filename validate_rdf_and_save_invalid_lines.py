"""
uses rdflib parser to validate rdf triples
argument 1 is the format specified by rdflib e.g., 'nt11'
argument 2+ are the files you wish to validate
makes three files
filename_extracted.nt for all extracted sameAs and exactMatch triples (adds %20 if there is an unicode whitespace)
filename_fixed_triples.tsv depicts all old triples and the triples that replaced it
filename_invalid_lines.nt all invalid lines that can't be solved by replacing whitespace with %20
"""
import sys
from rdflib import Graph
import rdflib
import re
import csv

SAMEAS = 'http://www.w3.org/2002/07/owl#sameAs'
EXACTMATCH = 'http://www.w3.org/2004/02/skos/core#exactMatch'

def fix_invalid_line(invalid_line):
    invalid_spo = re.findall(r"(?<=\<)(.*?)(?=\>)", invalid_line)
    # check for unicode escape char in string and replace with %20
    s,p,o = [re.sub(r"\u2005|\u0020|\u00A0|\u1680|\u2000|\u2001|\u2002|\u2003|\u2004|\u2005|\u2006|\u2007|\u2008|\u2009|\u200A|\u202F|\u205f|\u3000", "%20", i) for i in invalid_spo]
    fixed_line = f"<{s}> <{p}> <{o}> ."
    # save correct IRI and invalid IRI to a tsv
    with open(f"{file.split('.')[0]}_fixed_triples.tsv", 'a') as out:
        tsv = csv.writer(out, delimiter='\t')
        tsv.writerow([invalid_line, fixed_line])
    # return valid IRI
    return fixed_line

def validate_file(file):
    total_triples = 0
    sameas_triples = 0
    exactmatch_triples = 0
    invalid_lines = 0

    with open(f"{file.split('.')[0]}_fixed_triples.tsv", 'a') as out:
        tsv = csv.writer(out, delimiter='\t')
        tsv.writerow(['old triple', 'new triple'])

    with open(f"{file.split('.')[0]}_extracted.nt", 'a') as extracted_file:
        with open(f"{file.split('.')[0]}_invalid_lines.nt", 'a') as error_file:
            with open(file, 'r') as infile:
                for line in infile:
                    if '<' in line:
                        total_triples += 1
                        try:
                            if SAMEAS in line:
                                sameas_triples += 1
                                Graph().parse(data=line, format=FORMAT)
                                extracted_file.write(line)
                            elif EXACTMATCH in line:
                                exactmatch_triples += 1
                                Graph().parse(data=line, format=FORMAT) 
                                extracted_file.write(line)                  
                        except rdflib.plugins.parsers.ntriples.ParseError as e:
                            fixed_line = fix_invalid_line(line)
                            try:
                                Graph().parse(data=fixed_line, format=FORMAT)
                                extracted_file.write(fixed_line)
                            except:
                                print(e, fixed_line)
                                error_file.write(line)
    
    print(f"{file} has {total_triples} total triples, {sameas_triples} owl:sameAs triples and, {exactmatch_triples} skos:exactMatch triples, and {invalid_lines} invalid lines.")

FORMAT = sys.argv[1]

for file in sys.argv[2:]:
    validate_file(file)