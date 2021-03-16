import csv
import json

csvfile = open('../../phase1_data_collection/git_scraper/data/git_repos_data.json', 'r')
jsonfile = open('data/repo_split_md.csv', 'w')

fieldnames = ("ID", "URL", "Repo Name", "Collection", "MD Contents", "C/C++ Contents", "Python Contents")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write(",")
    jsonfile.write("\n")