import pymongo
from pymongo import MongoClient
import ssl
import re
import json

ssl._create_default_https_context = ssl._create_unverified_context

def get_energy_issue(collection):
	collection_key = ['issue_title', 
					  'issue_contents', 
					  'issue_code', 
					  'issue_quotes', 
					  'contents_details', 
					  'contents_details_more'
					 ]
	original_energy_list = []
	counter_list = []
	counter = 0
	# regex_keyword = ['.*batter.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum*.']
	for ck in collection_key:
		energy_query = collection.find({"$or":[ {ck: {'$regex': regex_keyword[0]}},{ck+"."+name: {'$regex': regex_keyword[1]}},
													{ck+"."+name: {'$regex': regex_keyword[2]}},{ck+"."+name: {'$regex': regex_keyword[3]}},
													{ck+"."+name: {'$regex': regex_keyword[4]}}]})
		for document in energy_query:
			original_energy_list.append(document)
			counter = counter + 1
		counter_list.append(counter)

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, counter_list

def get_energy_issue_stats(collection, i):
	collection_key = ['issue_title', 
					  'issue_contents', 
					  'issue_code', 
					  'issue_quotes', 
					  'contents_details', 
					  'contents_details_more'
					 ]
	# regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum*.']
	original_energy_list = []
	counter_list = []
	counter = 0
	for ck in collection_key:
		energy_query = collection.find({"$or":[ {ck: {'$regex': regex_keyword[i]}}]})
		for document in energy_query:
			original_energy_list.append(document)
			counter = counter + 1
		counter_list.append(counter)

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, counter_list


############################
####### MAIN PROGRAM #######
############################
client = MongoClient("mongodb+srv://secretUser:agukalpa1234@cluster0-cem1l.azure.mongodb.net/data_phase1?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.data_phase1
# GET CLOSED/OPEN ISSUE ENERGY DOCUMENTS
c = [db.GitHubOpenIssues]
for collection in c:
	print (collection)
	print('\n')
	for i in range(1):
		duplicate_energy_issue_stat, no_duplicate_energy_issue_stat, issue_document_term_counter_stat = get_energy_issue_stats(collection, i)
		print("duplicate energy issue stats: ", len(duplicate_energy_issue_stat))
		print("energy issue stats: ", len(no_duplicate_energy_issue_stat))

	print('\n')
	print('-------------------------------------')
	print('\n')
	duplicate_energy_issue, no_duplicate_energy_issue, issue_document_term_counter = get_energy_issue(collection)
	print("duplicate energy issue: ", len(duplicate_energy_issue))
	print("energy issue: ", len(no_duplicate_energy_issue))
	print('\n')
	print('-------------------------------------')
	print('\n')

with open('data/consum_new_github-issues_data.json', 'a') as outfile:
	for item in no_duplicate_energy_issue:
		del item['_id']
		outfile.write(json.dumps(item))
		outfile.write(",")
		outfile.write("\n")
	outfile.close()
