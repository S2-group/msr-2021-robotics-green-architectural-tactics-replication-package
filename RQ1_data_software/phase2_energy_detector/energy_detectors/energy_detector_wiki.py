import pymongo
from pymongo import MongoClient
import ssl
import re
import json

ssl._create_default_https_context = ssl._create_unverified_context

def get_energy(collection):
	collection_key = ['package', 
					  'pakcage_summary', 
					  'package_code',
					  'package_tt',
					  'package_details'
					 ]
	regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
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

def get_energy_stats(collection, i):
	collection_key = ['package', 
					  'pakcage_summary', 
					  'package_code',
					  'package_tt',
					  'package_details'
					 ]
	regex_keyword = ['.*battery.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
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

	return original_energy_list, new_energy_list, counter_list, regex_keyword[i]


############################
####### MAIN PROGRAM #######
############################
client = MongoClient("mongodb+srv://secretUser:agukalpa1234@cluster0-cem1l.azure.mongodb.net/data_phase1?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.data_phase1
# GET Wiki ENERGY DOCUMENTS
c = [db.Wiki]
for collection in c:
	print (collection)
	print('\n')
	for i in range(5):
		duplicate_energy_stat, no_duplicate_energy_stat, document_term_counter_stat, keyword = get_energy_stats(collection, i)
		print(keyword, ": duplicate energy stats: ", len(duplicate_energy_stat))
		print(keyword, "energy stats: ", len(no_duplicate_energy_stat))

	print('\n')
	print('-------------------------------------')
	print('\n')
	duplicate_energy, no_duplicate_energy, document_term_counter = get_energy(collection)
	print("duplicate energy: ", len(duplicate_energy))
	print("energy: ", len(no_duplicate_energy))
	print('\n')
	print('-------------------------------------')
	print('\n')

with open('data/wiki_energy_data.json', 'a') as outfile:
	for item in no_duplicate_energy:
		del item['_id']
		outfile.write(json.dumps(item))
		outfile.write(",")
		outfile.write("\n")
	outfile.close()
