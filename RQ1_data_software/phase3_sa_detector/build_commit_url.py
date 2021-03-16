import csv
import json
from itertools import zip_longest
from collections import defaultdict
import ast

def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return

columns = defaultdict(list)
commit_info_dicts = []
commit_hashes = []
new_commit_url = []

with open('energy_commits.csv') as f:
    reader = csv.DictReader(no_blank(f))
    for row in reader:
        for (k,v) in row.items(): 
            columns[k].append(v)

while '' in columns['URL']:
    columns['URL'].remove('')

while '' in columns['Commit Info']:
    columns['Commit Info'].remove('')

commit_url = columns['URL']
commit_info = columns['Commit Info']

for commit in commit_info:
	commit = ast.literal_eval(commit)
	commit_info_dicts.append(commit)
#print(commit_info_dicts)

for commits in commit_info_dicts:
	for k, v in commits.items():
		commit_hashes.append(k)

for url in commit_url:
	url = url+'/commit'
	new_commit_url.append(url)

final_url_list = ['/'.join(z) for z in zip(new_commit_url, commit_hashes)]

list_ = [final_url_list]

export_data = zip_longest(*list_, fillvalue='')

with open('commit_urls.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("URL"))
    wr.writerows(export_data)
myfile.close()
