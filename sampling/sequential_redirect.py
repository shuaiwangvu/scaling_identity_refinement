# this script is for testing only and is not being maintained anymore 
import time
import networkx as nx
import sys
import csv
import requests
from requests.exceptions import Timeout

sameas = 'http://www.w3.org/2002/07/owl#sameAs'
my_redirect = "https://krr.triply.cc/krr/metalink/def/redirectedTo" # a relation

NOTFOUND = 1
FOUNDWITHOUTREDIRECT = 2
ERROR = 3
TIMEOUT = 4
REDIRECT = 5

standard_timeout =  (0.01, 0.05)
retry_timeout = (0.5, 2.5)
final_try_timeout = (1, 5)

def find_redirects (iri, timeout = standard_timeout):
	try:
		collect_urls = []
		response = requests.get(iri, timeout= timeout, allow_redirects=True)

		if response.status_code == 404:
			return NOTFOUND, None

		if response.history:
			if response.url == iri: # instead of this we do: encodingequivalent
				return FOUNDWITHOUTREDIRECT, None
			else: # return graph that distinguishing encoding equivalent and redirect
				# print("Request was redirected")
				for resp in response.history:
					# print(resp.status_code, resp.url)
					collect_urls.append(resp.url) # TODO save in sep file(kvstore?)
				# print("Final destination:")
				# print(response.status_code, response.url)

				collect_urls.append(response.url)
				return REDIRECT, collect_urls # also return the ee_url
		else:
			# print("Request was not redirected")
			return FOUNDWITHOUTREDIRECT, None
	except Timeout:
		# print('The request timed out', iri)
		return TIMEOUT, None
	except:
		#print (f'error: ', iri)
		return ERROR, None

def load_entities(graph_id):
	entities = set()
	with open(graph_id, encoding='utf-8') as in_file:
		for line in in_file:
			#print(line)
			entities.add(line)
	return entities

def export_redirect_graph_edges(file_name, graph):
	# count_line = 0
	with open(file_name, 'w') as output:
		for (l,r) in graph.edges():
			line = '<' + l + '> '
			line += '<' + my_redirect + '> '
			if r[0] == '"':
				if "^^" in r:
					line += '' + r + ' .\n'
					# edited = splited[-2][1:-1] # keep that original one
					# example "http://xmlns.com/foaf/0.1/"^^<http://www.w3.org/2001/XMLSchema#anyURI>
				else: # else, add the following
					line += '' + r + "^^<http://www.w3.org/2001/XMLSchema#string>" + ' .\n'
					# edited = splited[-2][1:-1] + "^^<http://www.w3.org/2001/XMLSchema#string>"
			else:
				line +=  '<' + r +'>. \n'
			output.write(str(line))
			# count_line += 1
	# print ('count line = ', count_line)

def export_redirect_graph_nodes(file_name, graph):
	file =  open(file_name, 'w', newline='')
	writer = csv.writer(file,  delimiter='\t')
	writer.writerow([ "Entity", "Remark"])
	for n in graph.nodes:
		if graph.nodes[n]['remark'] == 'not_found':
			writer.writerow([n, 'NotFound'])
		elif graph.nodes[n]['remark'] == 'found_without_redirect':
			writer.writerow([n, 'NotRedirect'])
		elif graph.nodes[n]['remark'] == 'error':
			writer.writerow([n, 'Error'])
		elif graph.nodes[n]['remark'] == 'timeout':
			writer.writerow([n, 'Timeout'])
		elif graph.nodes[n]['remark'] == 'redirected':
			writer.writerow([n, 'Redirected'])
		elif graph.nodes[n]['remark'] == 'redirect_until_timeout':
			writer.writerow([n, 'RedirectedUntilTimeout'])
		elif graph.nodes[n]['remark'] == 'redirect_until_error':
			writer.writerow([n, 'RedirectedUntilError'])
		elif graph.nodes[n]['remark'] == 'redirect_until_found':
			writer.writerow([n, 'RedirectedUntilLanded'])
		elif graph.nodes[n]['remark'] == 'redirect_until_not_found':
			writer.writerow([n, 'RedirectedUntilNotFound'])
		else:
			print ('Error: ', graph.nodes[n]['remark'])

def create_redi_graph(graph_id):
	start = time.time()
	redi_graph = nx.DiGraph()

	entities_to_test = load_entities(graph_id)
	print ('there are ', len (entities_to_test), ' entities in the graph ')

	for entity in entities_to_test:
		redi_graph.add_node(entity, remark='unknown')

	for timeout_parameters in [standard_timeout, retry_timeout, final_try_timeout]:
		timeout_entities = set()
		end_of_redirect_entities = set()
		for e in redi_graph.nodes():
			if redi_graph.nodes[e]['remark'] == 'unknown':
				entities_to_test.add(e)
		for e in entities_to_test:
			result, via_entities = find_redirects(e, timeout = timeout_parameters )
			if result == NOTFOUND:
				redi_graph.nodes[e]['remark'] = 'not_found'
			elif result == FOUNDWITHOUTREDIRECT:
				redi_graph.nodes[e]['remark'] = 'found_without_redirect'
			elif result == ERROR:
				redi_graph.nodes[e]['remark'] = 'error'
			elif result == TIMEOUT:
				timeout_entities.add(e)
				redi_graph.nodes[e]['remark'] = 'timeout'
			elif result == REDIRECT:
				redi_graph.nodes[e]['remark'] = 'redirected'
				if via_entities[0] != e:
					# the resolved IRI is in a different encoding
					# print ('working on ', e)
					# print ('error at the first! ')
					# print ('via_entities', via_entities)
					# redi_graph.add_node(t, remark = 'unknown')
					# redi_graph.add_edge(e, via_entities[0])
					via_entities = [e] + via_entities
				if len (via_entities) > 1:
					for i, s in enumerate(via_entities[:-1]):
						t = via_entities[i+1]
						if s not in redi_graph.nodes():
							redi_graph.add_node(s, remark = 'redirected')
						else:
							redi_graph.nodes[s]['remark'] = 'redirected'

						# if t not in redi_graph.nodes():
						redi_graph.add_node(t, remark = 'unknown')

						redi_graph.add_edge(s, t)

					# if via_entities[-1] not in end_of_redirect_entities and via_entities[-1] not in timeout_entities:
					end_of_redirect_entities.add(via_entities[-1])
				else:
					print ('error: ', via_entities)

				# print ('\n')
				# for v in via_entities:
				# 	print ('after update ',v,' with mark ', redi_graph.nodes[v]['remark'], ' with outdegree', redi_graph.out_degree(v))
			else:
				print ('error')
		
		print ('TIMEOUT: there are ', len (timeout_entities), ' timeout entities')
		print ('End Of Redirect: there are ', len (end_of_redirect_entities), ' end of redirect entities')
		entities_to_test = timeout_entities.union(end_of_redirect_entities)

		for e in redi_graph.nodes():

			if redi_graph.nodes[e]['remark'] == 'redirected' and redi_graph.out_degree(e) == 0:
				print ('ERROR:')
				print (e, ' was redirected but has out-degree 0')
				print (e, ' was redirected is with in-degree ', redi_graph.in_degree(e))
				# if e in graph.nodes():
				# 	print ('it is in the original graph!')


	for m in end_of_redirect_entities:
		redi_graph.add_node(m, remark = 'timeout')

	update_against = set()
	for n in redi_graph.nodes():
		if redi_graph.nodes[n]['remark'] != 'redirected':
			update_against.add(n)

	# count_redirect_until_timeout = 0

	for n in redi_graph.nodes():

		if redi_graph.nodes[n]['remark'] == 'redirected':
			# print ('updating node : ', n)
			for m in update_against:
				if nx.has_path(redi_graph, n, m):
					if redi_graph.nodes[m]['remark'] == 'timeout' or redi_graph.nodes[m]['remark'] == 'redirect_until_timeout':
						redi_graph.nodes[n]['remark'] = 'redirect_until_timeout'
						# print ('\tupdating against m = ', redi_graph.nodes[m]['remark'])
					elif redi_graph.nodes[m]['remark'] == 'not_found'  or redi_graph.nodes[m]['remark'] == 'redirect_until_not_found':
						redi_graph.nodes[n]['remark'] = 'redirect_until_not_found'
						# print ('\tupdating against m = ', redi_graph.nodes[m]['remark'])
					elif redi_graph.nodes[m]['remark'] == 'error' or redi_graph.nodes[m]['remark'] == 'redirect_until_error':
						redi_graph.nodes[n]['remark'] = 'redirect_until_error'
						# print ('\tupdating against m = ', redi_graph.nodes[m]['remark'])
					elif redi_graph.nodes[m]['remark'] == 'found_without_redirect' or redi_graph.nodes[m]['remark'] == 'redirect_until_found':
						redi_graph.nodes[n]['remark'] = 'redirect_until_found'
						# print ('\tupdating against m = ', redi_graph.nodes[m]['remark'])
					else:
						# pass
						print('Error? reaching m = ', redi_graph.nodes[m]['remark'])

			if redi_graph.nodes[n]['remark'] == 'redirected': # redirected until redirected

				print ('\n\nredirected but not to anywhere?')
				print ('entitiy: ', n)
				print ('outdegree: ', redi_graph.out_degree(n))
				print ('indegree: ', redi_graph.in_degree(n))
				result, via_entities = find_redirects(n, timeout = timeout_parameters )
				print ('result ', result)
				print ('via_entities = ', via_entities)
				redi_graph.nodes[n]['remark'] = 'redirect_until_timeout'


	count_not_found = 0
	count_found_without_redirect = 0
	count_error = 0
	count_timeout = 0
	count_redirected = 0
	count_redirect_until_timeout = 0
	count_redirect_until_not_found = 0
	count_redirect_until_error = 0
	count_redirect_until_found = 0
	count_other = 0

	for n in redi_graph.nodes():
		if redi_graph.nodes[n]['remark'] == 'not_found':
			count_not_found += 1
		elif redi_graph.nodes[n]['remark'] == 'found_without_redirect':
			count_found_without_redirect += 1
		elif redi_graph.nodes[n]['remark'] == 'error':
			count_error += 1
		elif redi_graph.nodes[n]['remark'] == 'timeout':
			count_timeout += 1
		elif redi_graph.nodes[n]['remark'] == 'redirect_until_timeout':
			count_redirect_until_timeout += 1
		elif redi_graph.nodes[n]['remark'] == 'redirect_until_not_found':
			count_redirect_until_not_found += 1
		elif redi_graph.nodes[n]['remark'] == 'redirect_until_error':
			count_redirect_until_error += 1
		elif redi_graph.nodes[n]['remark'] == 'redirect_until_found':
			count_redirect_until_found += 1
		else:
			print ('strange : ', redi_graph.nodes[n]['remark'])
			count_other += 1

	count_redirected = count_redirect_until_timeout + count_redirect_until_not_found + count_redirect_until_error + count_redirect_until_found

	print ('Regarding the original graph:')
	print ('\tcount not found: ', count_not_found)
	print ('\tcount found (not redirected): ', count_found_without_redirect)
	print ('\tcount error: ', count_error)
	print ('\tcount timeout: ', count_timeout)
	print ('*****')
	print ('\tcount redirect until timeout: ', count_redirect_until_timeout)
	print ('\tcount redirect until not found: ', count_redirect_until_not_found)
	print ('\tcount redirect until error: ', count_redirect_until_error)
	print ('\tcount redirect until found: ', count_redirect_until_found)
	print ('\tTOTAL REDIRECTED: ', count_redirected)
	print ('\tcount other (mistake): ', count_other)

	# Validate
	count = 0
	for n in redi_graph.nodes():
		if redi_graph.nodes[n]['remark'] == 'unknown':
			print  ('unknown exists (but should not)!')
			print (n)
			count += 1

		if  redi_graph.nodes[n]['remark'] == 'end_of_redirect' :
			print ('end of redirect exists (but should not)!')
			print (n)

	# print('count unknown = ', count)
	print ('total num edges in the new redirect graph = ', len(redi_graph.edges()))

	end = time.time()
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)

	time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
	print("Time taken = ", time_formated)

	return redi_graph

graph_ids = sys.argv[1:]
for graph_id in graph_ids:
	print ('\n\n\nprocessing file = ', graph_id)
	redi_graph = create_redi_graph(graph_id)
	export_redirect_graph_edges(f"{graph_id.split('.')[0]}_redirect_edges.nt", redi_graph)
	export_redirect_graph_nodes(f"{graph_id.split('.')[0]}_redirect_nodes.tsv", redi_graph)
	# # count_notfound = 0
	# # count_no_redirect = 0
	# # count_error = 0
	# # count_timeout = 0
	# # count_redirect = 0
	# original_entities = entities_to_test.copy()
	# redirect_result = {}
	# for e in entities_to_test:
	# 	redirect_result[e] = None

	# while len(entities_to_test) != 0:
	# 	collect_new_entities_to_test = set()
	# 	for e in entities_to_test:
	# 		# find_redirects
	# 		result, via_entities = find_redirects(e)
	# 		# print ('testing ',e)
	# 		if result == NOTFOUND:
	# 			redirect_result[e] = NOTFOUND
	# 		elif result == FOUNDWITHOUTREDIRECT:
	# 			redirect_result[e] = FOUNDWITHOUTREDIRECT
	# 		elif result == ERROR:
	# 			redirect_result[e] = ERROR
	# 		elif result == TIMEOUT:
	# 			redirect_result[e] = TIMEOUT
	# 			timeout_entities.add(e)
	# 		elif result == REDIRECT:
	# 			redirect_result[e] = REDIRECT
	# 			if len (via_entities) > 1:
	# 				for i, s in enumerate(via_entities[:-1]):
	# 					t = via_entities[i+1]
	# 					redi_graph.add_edge(s, t)

	# 				if via_entities[-1] not in entities_to_test:
	# 					collect_new_entities_to_test.add(via_entities[-1])
	# 			else:
	# 				print ('error: ', via_entities)
	# 		else:
	# 			print ('error')

	# 	print ('TIMEOUT: there are ', len (timeout_entities), ' timeout entities')

	# 	count_timeout = 0
	# 	remain_timeout_entities = set()
	# 	for e in timeout_entities:
	# 		# find_redirects
	# 		result, via_entities = find_redirects(e, timeout = retry_timeout)
	# 		# print ('testing ',e)
	# 		if result == NOTFOUND:
	# 			redirect_result[e] = NOTFOUND
	# 		elif result == FOUNDWITHOUTREDIRECT:
	# 			redirect_result[e] = FOUNDWITHOUTREDIRECT
	# 		elif result == ERROR:
	# 			redirect_result[e] = ERROR
	# 		elif result == TIMEOUT:
	# 			count_timeout += 1
	# 			remain_timeout_entities.add(e)
	# 		elif result == REDIRECT:
	# 			redirect_result[e] = REDIRECT
	# 			if len (via_entities) > 1:
	# 				# count_redirect += 1
	# 				for i, s in enumerate(via_entities[:-1]):
	# 					t = via_entities[i+1]
	# 					redi_graph.add_edge(s, t)

	# 				if via_entities[-1] not in entities_to_test:
	# 					collect_new_entities_to_test.add(via_entities[-1])
	# 			else:
	# 				print ('too short? error: ',via_entities)
	# 		else:
	# 			print ('error')
	# 	print ('TIMEOUT: still timeout ', count_timeout)

	# 	count_timeout = 0
	# 	for e in remain_timeout_entities:
	# 		# find_redirects
	# 		result, via_entities = find_redirects(e, timeout = final_try_timeout)
	# 		# print ('testing ',e)
	# 		if result == NOTFOUND:
	# 			redirect_result[e] = NOTFOUND
	# 		elif result == FOUNDWITHOUTREDIRECT:
	# 			redirect_result[e] = FOUNDWITHOUTREDIRECT
	# 		elif result == ERROR:
	# 			redirect_result[e] = ERROR
	# 		elif result == TIMEOUT:
	# 			count_timeout += 1
	# 			# timeout_entities.add(e)
	# 			# print (e)
	# 		elif result == REDIRECT:
	# 			redirect_result[e] = REDIRECT
	# 			if len (via_entities) > 1:
	# 				# count_redirect += 1
	# 				for i, s in enumerate(via_entities[:-1]):
	# 					t = via_entities[i+1]
	# 					redi_graph.add_edge(s, t)

	# 				if via_entities[-1] not in entities_to_test:
	# 					collect_new_entities_to_test.add(via_entities[-1])
	# 			else:
	# 				print ('too short? error: ',via_entities)
	# 		else:
	# 			print ('error')
	# 	print ('TIMEOUT: still timeout after final try', 55555555555555555555555555555555555555)

	# 	timeout_entities = set()
	# 	entities_to_test = collect_new_entities_to_test

	# redirect_result_filtered = { your_key: redirect_result[your_key] for your_key in original_entities }

	# print ('there are in total ', sum(value == NOTFOUND for value in redirect_result_filtered.values()), ' not found')
	# print ('there are in total ', sum(value == FOUNDWITHOUTREDIRECT for value in redirect_result_filtered.values()), ' no redirect')
	# print ('there are in total ', sum(value == TIMEOUT for value in redirect_result_filtered.values()), ' timeout')
	# print ('there are in total ', sum(value == ERROR for value in redirect_result_filtered.values()), ' error')
	# print ('there are in total ', sum(value == REDIRECT for value in redirect_result_filtered.values()), 'redirected')

	# print ('total num edges in the new redirect graph = ', len(redi_graph.edges()))

	# end = time.time()
	# hours, rem = divmod(end-start, 3600)
	# minutes, seconds = divmod(rem, 60)

	# time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
	# print("Time taken = ", time_formated)

	# print ('Exporting')
	# file = open( str(graph_id) + "_redirect.nt", 'w')
	# redirect_file_writer = csv.writer(file, delimiter=' ')
	# for (s,t) in redi_graph.edges():
	# 	# log_file_writer.writerow([s,t])
	# 	if t[0] != '"':
	# 		redirect_file_writer.writerow(['<'+s+'>', '<'+my_redirect+'>', '<'+t+'>', '.'])
	# 	else:
	# 		redirect_file_writer.writerow(['<'+s+'>', '<'+my_redirect+'>', t+'^^<http://www.w3.org/2001/XMLSchema#string>', '.'])