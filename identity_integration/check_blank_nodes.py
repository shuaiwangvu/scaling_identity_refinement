# this Python script checks the blank nodes and if there are formating errors in the files.

import os

#files I skipped: 'identity_links/yago-wd-sameAs.nt', 'identity_links/sameas-external.ttl',
files = ['identity_links/yago-wd-sameAs.nt', 'identity_links/sameas-external.ttl', 'identity_links/sameas-all-wikis.ttl']

def test_blank_nodes(filename):
	print ('processing file ', filename)
	file1 = open(filename, 'r')
	lines = file1.readlines()

	count = 0
	# Strips the newline character
	for line in lines:
		count += 1
		# check if there are blank nodes in these files
		if "<_:" in line:
			print("Blank node in line{}: {}".format(count, line.strip()))
		# check if there are lines with \t included in the .nt files
		if '.nt' in filename:
			if len(line.split('\t')) != 4:
				print("Tab in line{}: {}".format(count, line.strip()))
		# check if there are lines with space included in the .ttl files 
		elif '.ttl' in filename:
			if len(line.split(' ')) != 4:
				print("Space in line{}: {}".format(count, line.strip()))
		if count % 10000000 ==0:
			print ('\tprocessed ', count, ' lines')


for file in files:
	if 'finn' in os.getcwd():
		file = '/home/nasim/data/' + file
	test_blank_nodes(file)
