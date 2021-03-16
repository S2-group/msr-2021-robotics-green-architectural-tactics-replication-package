import pymongo
from pymongo import MongoClient
import ssl
import re
import json

ssl._create_default_https_context = ssl._create_unverified_context

def get_energy_commit(collection):
	collection_key = [
					  'commit_info'
					 ]
	#regex_keyword = ['.*batter.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum.*']
	original_energy_list = []
	commit_hash = []

	with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/commit_data_new.json') as f:
		d = json.load(f)

	commits = [item.get('commit_info') for item in d]
	for arr in commits:
		for dictionary in arr:
			for k, v in dictionary.items():
				commit_hash.append(k)

	for ck in collection_key:
		for hash_ in commit_hash:
			energy_query = collection.find({"$or":[ {ck+"."+hash_: {'$regex': regex_keyword[0]}}]})

			for document in energy_query:
				print(document)
				original_energy_list.append(document)


	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list



def get_energy_stats_commit(collection, i):
	collection_key = [
					  'commit_info'
					 ]
	#regex_keyword = ['.*batter.*', '.*energy.*', '.*power.*', '.*sustainab.*', '.*green.*']
	regex_keyword = ['.*consum.*']
	original_energy_list = []
	commit_hash = []

	with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/commit_data_new.json') as f:
		d = json.load(f)

	commits = [item.get('commit_info') for item in d]
	for arr in commits:
		for dictionary in arr:
			for k, v in dictionary.items():
				commit_hash.append(k)

	for ck in collection_key:
		for hash_ in commit_hash:
			energy_query = collection.find({"$or":[ {ck+"."+hash_: {'$regex': regex_keyword[i]}}]})
			for document in energy_query:
				original_energy_list.append(document)

	new_energy_list = [i for n, i in enumerate(original_energy_list) if i not in original_energy_list[n + 1:]]

	return original_energy_list, new_energy_list, regex_keyword[i]

############################
####### MAIN PROGRAM #######
############################
client = MongoClient("mongodb+srv://secretUser:agukalpa1234@cluster0-cem1l.azure.mongodb.net/data_phase1?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.data_phase1
# GET CLOSED/OPEN PR ENERGY DOCUMENTS
c = [db.Commits]
for collection in c:
	print (collection)
	print('\n')
	#duplicate_energy_commit, no_duplicate_energy_commit = get_energy_commit(collection)
	#total_docs = no_duplicate_energy_commit


	for i in range(1):
		duplicate_energy_commit_stat, no_duplicate_energy_commit_stat, keyword = get_energy_stats_commit(collection, i)
		print(keyword, ": duplicate energy stats: ", len(duplicate_energy_commit_stat))
		print(keyword, "energy stats: ", len(no_duplicate_energy_commit_stat))
		print('\n')

		total_docs_stats = no_duplicate_energy_commit_stat
		total_docs_stats = [i for n, i in enumerate(total_docs_stats) if i not in total_docs_stats[n + 1:]]
		print(keyword, "energy stats: ", len(total_docs_stats))


with open('data/consum_commit_data_new.json', 'a') as outfile:
	for item in total_docs:
		del item['_id']
		outfile.write(json.dumps(item))
		outfile.write(",")
		outfile.write("\n")
	outfile.close()
