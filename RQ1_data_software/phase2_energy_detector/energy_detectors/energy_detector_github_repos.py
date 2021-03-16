import pymongo
from pymongo import MongoClient
import ssl
import re
import json

ssl._create_default_https_context = ssl._create_unverified_context

def get_energy_python(collection):
	collection_key = [
					  'code_comments_python'
					 ]
	#regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum*.']
	original_energy_list = []
	counter_list = []
	python_file_names = []
	counter = 0

	with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/git_repos_data.json') as f:
		d = json.load(f)

	code_comments_python = [item.get('code_comments_python') for item in d]
	for dictionary in code_comments_python:
		for file_name in dictionary:
			python_file_names.append(file_name)

	for ck in collection_key:
		for name in python_file_names:
			energy_query = collection.find({"$or":[ {ck+"."+name: {'$regex': regex_keyword[0]}},{ck+"."+name: {'$regex': regex_keyword[1]}},
													{ck+"."+name: {'$regex': regex_keyword[2]}},{ck+"."+name: {'$regex': regex_keyword[3]}},
													{ck+"."+name: {'$regex': regex_keyword[4]}}]})
			for document in energy_query:
				original_energy_list.append(document)
				counter = counter + 1
			counter_list.append(counter)
			#print(len(original_energy_list))

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, counter_list

def get_energy_cpp(collection):
	collection_key = [ 
					  'code_comments_c++'
					 ]
	#regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum*.']
	original_energy_list = []
	counter_list = []
	cpp_file_names = []
	counter = 0

	with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/git_repos_data.json') as f:
		d = json.load(f)

	code_comments_cpp = [item.get('code_comments_c++') for item in d]
	for dictionary in code_comments_cpp:
		for file_name in dictionary:
			cpp_file_names.append(file_name)

	for ck in collection_key:
		for name in cpp_file_names:
			energy_query = collection.find({"$or":[ {ck+"."+name: {'$regex': regex_keyword[0]}},{ck+"."+name: {'$regex': regex_keyword[1]}},
													{ck+"."+name: {'$regex': regex_keyword[2]}},{ck+"."+name: {'$regex': regex_keyword[3]}},
													{ck+"."+name: {'$regex': regex_keyword[4]}}]})
			for document in energy_query:
				original_energy_list.append(document)
				counter = counter + 1
			counter_list.append(counter)
			#print(len(original_energy_list))

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, counter_list

def get_energy_md(collection):
	# {'md_contents.git_repospocketsphinxREADME':{"$elemMatch":{"$elemMatch":{$in: [/ros/]}}}}
	collection_key = [ 
					  'md_contents'
					 ]
	#regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum.*']
	original_energy_list = []
	counter_list = []
	md_file_names = []
	counter = 0

	with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/git_repos_data.json') as f:
		d = json.load(f)

	code_comments_md = [item.get('md_contents') for item in d]
	for dictionary in code_comments_md:
		for file_name in dictionary:
			md_file_names.append(file_name)

	for ck in collection_key:
		for name in md_file_names:
			energy_query = collection.find({"$or":[ {ck+"."+name: {'$regex': regex_keyword[0]}},{ck+"."+name: {'$regex': regex_keyword[1]}},
													{ck+"."+name: {'$regex': regex_keyword[2]}},{ck+"."+name: {'$regex': regex_keyword[3]}},
													{ck+"."+name: {'$regex': regex_keyword[4]}}]})
			for document in energy_query:
				original_energy_list.append(document)
				counter = counter + 1
			counter_list.append(counter)
			#print(len(original_energy_list))

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, counter_list

def get_energy_stats_python(collection, i):
	collection_key = [
					  'code_comments_python'
					 ]
	#regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum.*']
	original_energy_list = []
	counter_list = []
	python_file_names = []
	counter = 0
	with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/git_repos_data.json') as f:
		d = json.load(f)

	code_comments_python = [item.get('code_comments_python') for item in d]
	for dictionary in code_comments_python:
		for file_name in dictionary:
			python_file_names.append(file_name)

	for ck in collection_key:
		for name in python_file_names:
			energy_query = collection.find({"$or":[ {ck+"."+name: {'$regex': regex_keyword[i]}}]})
			for document in energy_query:
				original_energy_list.append(document)
				counter = counter + 1
			counter_list.append(counter)

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, counter_list, regex_keyword[i]

def get_energy_stats_cpp(collection, i):
	collection_key = [
					  'code_comments_c++'
					 ]
	#regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum.*']
	original_energy_list = []
	counter_list = []
	cpp_file_names = []
	counter = 0
	with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/git_repos_data.json') as f:
		d = json.load(f)

	code_comments_cpp = [item.get('code_comments_c++') for item in d]
	for dictionary in code_comments_cpp:
		for file_name in dictionary:
			cpp_file_names.append(file_name)

	for ck in collection_key:
		for name in cpp_file_names:
			energy_query = collection.find({"$or":[ {ck+"."+name: {'$regex': regex_keyword[i]}}]})
			for document in energy_query:
				original_energy_list.append(document)
				counter = counter + 1
			counter_list.append(counter)

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, counter_list, regex_keyword[i]

def get_energy_stats_md(collection, i):
	collection_key = [
					  'md_contents'
					 ]
	#regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum.*']
	original_energy_list = []
	counter_list = []
	md_file_names = []
	counter = 0
	with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/git_repos_data.json') as f:
		d = json.load(f)

	code_comments_md = [item.get('md_contents') for item in d]
	for dictionary in code_comments_md:
		for file_name in dictionary:
			md_file_names.append(file_name)

	for ck in collection_key:
		for name in md_file_names:
			energy_query = collection.find({"$or":[ {ck+"."+name: {'$regex': regex_keyword[i]}}]})
			for document in energy_query:
				original_energy_list.append(document)
				counter = counter + 1
			counter_list.append(counter)

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, counter_list, regex_keyword[i]


############################
####### MAIN PROGRAM #######
############################
client = MongoClient("mongodb+srv://secretUser:agukalpa1234@cluster0-cem1l.azure.mongodb.net/data_phase1?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.data_phase1
# GET CLOSED/OPEN PR ENERGY DOCUMENTS
c = [db.GitHubRepos]
for collection in c:
	print (collection)
	print('\n')
	for i in range(1):
		duplicate_energy_stat_p, no_duplicate_energy_stat_p, document_term_counter_stat_p, keyword = get_energy_stats_python(collection, i)
		print(keyword, ": duplicate energy stats python: ", len(duplicate_energy_stat_p))
		print(keyword, "energy stats python: ", len(no_duplicate_energy_stat_p))
		print('\n')
		duplicate_energy_stat_cpp, no_duplicate_energy_stat_cpp, document_term_counter_stat_cpp, keyword = get_energy_stats_cpp(collection, i)
		print(keyword, ": duplicate energy stats cpp: ", len(duplicate_energy_stat_cpp))
		print(keyword, "energy stats cpp: ", len(no_duplicate_energy_stat_cpp))
		print('\n')
		duplicate_energy_stat_md, no_duplicate_energy_stat_md, document_term_counter_stat_md, keyword = get_energy_stats_md(collection, i)
		print(keyword, ": duplicate energy stats md: ", len(duplicate_energy_stat_md))
		print(keyword, "energy stats md: ", len(no_duplicate_energy_stat_md))
		print('\n')

		total_docs_stats = no_duplicate_energy_stat_p + no_duplicate_energy_stat_cpp + no_duplicate_energy_stat_md
		total_docs_stats = [i for n, i in enumerate(total_docs_stats) if i not in total_docs_stats[n + 1:]]
		print(keyword, "energy stats: ", len(total_docs_stats))


	print('\n')
	print('-------------------------------------')
	print('\n')
	duplicate_energy_python, no_duplicate_energy_python, document_term_counter_p = get_energy_python(collection)
	print("duplicate energy python: ", len(duplicate_energy_python))
	print("energy python: ", len(no_duplicate_energy_python))
	print('\n')
	print('-------------------------------------')
	print('\n')

	print('\n')
	print('-------------------------------------')
	print('\n')
	duplicate_energy_cpp, no_duplicate_energy_cpp, document_term_counter_c = get_energy_cpp(collection)
	print("duplicate energy c++: ", len(duplicate_energy_cpp))
	print("energy c++: ", len(no_duplicate_energy_cpp))
	print('\n')
	print('-------------------------------------')
	print('\n')

	print('\n')
	print('-------------------------------------')
	print('\n')
	duplicate_energy_md, no_duplicate_energy_md, document_term_counter_md = get_energy_md(collection)
	print("duplicate energy md: ", len(duplicate_energy_md))
	print("energy md: ", len(no_duplicate_energy_md))
	print('\n')
	print('-------------------------------------')
	print('\n')

	total_docs = no_duplicate_energy_python + no_duplicate_energy_cpp + no_duplicate_energy_md
	total_docs = [i for n, i in enumerate(total_docs) if i not in total_docs[n + 1:]]
	print(len(total_docs))

with open('data/consum_repositories_data.json', 'a') as outfile:
	for item in total_docs:
		del item['_id']
		outfile.write(json.dumps(item))
		outfile.write(",")
		outfile.write("\n")
	outfile.close()
