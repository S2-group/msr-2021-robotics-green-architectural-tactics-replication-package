import git
import csv
import json
from collections import defaultdict
import os
from pydriller import RepositoryMining

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

def switch_to_dir(dir_name):
    print("Current Working Directory " , os.getcwd())
    try: 
        os.chdir(dir_name)
        print("Directory changed")
    except OSError:
        print("Can't change the Current Working Directory") 
    print("Current Working Directory " , os.getcwd())  


columns = defaultdict(list)
repo_names = []
repo_urls = []

with open('Repos1.csv') as f:
    reader = csv.DictReader(no_blank(f))
    for row in reader:
        for (k,v) in row.items(): 
            columns[k].append(v)

while '' in columns['ID']:
    columns['ID'].remove('')

for id_ in columns['ID']:
    id_ = id_.split('/')[1]
    repo_names.append(id_)

while '' in columns['URL']:
    columns['URL'].remove('')

# for name in repo_names:
#     switch_to_dir('git_other_repos')
#     switch_to_dir(name)



for name in repo_names:
    switch_to_dir('git_repos')
    commit_msgs = []
    commit_hash = []
    commit_date = []
    commit_msg_data = []
    commit_data = {}

    g = git.cmd.Git(name)
    repo = git.Repo(name)
    url = repo.remote("origin").url
    print(url)
    repo_urls.append(url)
    #g.pull()


    for commit in RepositoryMining(name).traverse_commits():
        commit_msgs.append(commit.msg)
        commit_hash.append(commit.hash)
        commit_date.append(commit.committer_date)

    commit_dict = dict(zip(commit_hash, commit_msgs))
    commit_msg_data.append(commit_dict)
    print(len(commit_msg_data))
    commit_data['repo_name'] = name
    commit_data['url'] = url
    #commit_data['url'] = columns['URL'][1]
    commit_data['commit_info'] = commit_msg_data
    json_data = json.dumps(commit_data)

    switch_to_dir('../')
    with open('data/commit_data3.json', 'a') as outfile:
        outfile.write(json_data)
        outfile.write(",")
        outfile.write("\n")
        outfile.close()








