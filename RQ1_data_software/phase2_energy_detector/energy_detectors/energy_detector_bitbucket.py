import pymongo
from pymongo import MongoClient
import ssl
import re
import json

ssl._create_default_https_context = ssl._create_unverified_context

def get_energy_pr(collection):
	collection_key = ['pr_title', 
					  'pr_contents', 
					  'pr_comments', 
					 ]
	regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	#regex_keyword = ['.*consum.*']
	original_energy_list = []
	counter_list = []
	counter = 0
	for ck in collection_key:
		energy_query = collection.find({"$or":[ {ck: {'$regex': regex_keyword[0]}},{ck: {'$regex': regex_keyword[1]}},
												{ck: {'$regex': regex_keyword[2]}},{ck: {'$regex': regex_keyword[3]}},
												{ck: {'$regex': regex_keyword[4]}}]})
		for document in energy_query:
			original_energy_list.append(document)
			counter = counter + 1
		counter_list.append(counter)

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, counter_list

def get_energy_pr_stats(collection, i):
	collection_key = ['pr_title', 
					  'pr_contents', 
					  'pr_comments', 
					 ]
	regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	#regex_keyword = ['.*consum.*']
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
# GET CLOSED/OPEN PR ENERGY DOCUMENTS
c = [db.BitBucketPR]
for collection in c:
	print (collection)
	print('\n')
	for i in range(1):
		duplicate_energy_pr_stat, no_duplicate_energy_pr_stat, pr_document_term_counter_stat = get_energy_pr_stats(collection, i)
		print("duplicate energy pr stats: ", len(duplicate_energy_pr_stat))
		print("energy pr stats: ", len(no_duplicate_energy_pr_stat))

	print('\n')
	print('-------------------------------------')
	print('\n')
	duplicate_energy_pr, no_duplicate_energy_pr, pr_document_term_counter = get_energy_pr(collection)
	print("duplicate energy pr: ", len(duplicate_energy_pr))
	print("energy pr: ", len(no_duplicate_energy_pr))
	print('\n')
	print('-------------------------------------')
	print('\n')
print(no_duplicate_energy_pr)

with open('data/consum_bitbucket_pr_data.json', 'a') as outfile:
	for item in no_duplicate_energy_pr:
		del item['_id']
		outfile.write(json.dumps(item))