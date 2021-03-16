import csv
import json
from collections import defaultdict

def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return

columns = defaultdict(list)
with open('Repos_all.csv') as f:
	reader = csv.DictReader(no_blank(f))
	for row in reader:
		for (k,v) in row.items(): 
			columns[k].append(v)

while '' in columns['URL']:
    columns['URL'].remove('')
#print(columns['URL'])

with open('data/github-closed-pr-final_data.json') as f:
    d = json.load(f)
    #print(d)
with open('data/github-open-pr_data.json') as f:
    e = json.load(f)

file_url = [item.get('url') for item in d]
new_url = []
for url in file_url:
	url = url.split('/pull')[0]
	new_url.append(url)

file_url1 = [item.get('url') for item in e]
new_url1 = []
for url in file_url1:
    url = url.split('/pull')[0]
    new_url1.append(url)

print(len(set(new_url)))
print(len(set(new_url1)))
print(len(list(set(new_url+new_url1))))
#git_issues = list(set(new_url)) + list(set(new_url1))
#print(len(git_issues))
#output = list(set(columns['URL']) - set(new_url))
#print(len(output))