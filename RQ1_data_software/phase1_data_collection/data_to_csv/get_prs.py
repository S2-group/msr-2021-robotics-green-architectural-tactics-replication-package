import pymongo
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://secretUser:agukalpa1234@cluster0-cem1l.azure.mongodb.net/data_phase1?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.data_phase1

collection = db.GitHubClosedPRs

document_list = []
query = collection.find()
for document in query:
	document_list.append(document)

print(len(document_list))
with open('../git_scraper/data/github-closed-prs-final_data.json', 'a') as outfile:
	for item in document_list:
		del item['_id']
		outfile.write(json.dumps(item))
		outfile.write(",")
		outfile.write("\n")
	outfile.close()