import csv
import json
import itertools
from collections import defaultdict
from itertools import zip_longest

def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return

with open('../data/repos_split.json') as f:
    repo_split_data = json.load(f)
with open('../data/consum_repos_split.json') as f:
    consum_repo_split_data = json.load(f)

# r = list(itertools.filterfalse(lambda x: x in repo_split_data, consum_repo_split_data)) + list(itertools.filterfalse(lambda x: x in consum_repo_split_data, repo_split_data))
# print(len(r))
#print(consum_repo_split_data)
# for c in consum_repo_split_data:
# 	for r in repo_split_data:
# 		shared_items = {k: c[k] for k in c if k in r and c[k] == r[k]}
# 	print(shared_items)

for r in consum_repo_split_data:
    if r in repo_split_data:
        print(r)