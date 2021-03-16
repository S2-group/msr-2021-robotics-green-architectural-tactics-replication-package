import git
import csv
from collections import defaultdict

####################################
#### REMOVE BLANK LINES FROM CSV ###
####################################
def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return

columns = defaultdict(list)
with open('Repos1.csv') as f:
	reader = csv.DictReader(no_blank(f))
	for row in reader:
		for (k,v) in row.items(): 
			columns[k].append(v)

while '' in columns['URL']:
    columns['URL'].remove('')
print(columns['URL'])

for url in columns['URL']:
	git.Git("git_repos").clone(url)