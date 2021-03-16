import json
import glob
import os
import re
import csv
import git
from collections import defaultdict
from pydriller import RepositoryMining
import requests
import urllib.request, json
import urllib3
from urllib.request import urlopen
import time
import github3
import subprocess
import certifi
import sys

github_limit = 2000

def form_github_request(url):
        time.sleep(3600/github_limit)
        http = urllib3.PoolManager(ca_certs=certifi.where())
        return http.request('GET',
                                url,
                                headers=urllib3.util.make_headers(basic_auth="XXXX" + ":" + "XXXXXX",
                                                                user_agent="XXXXX"))

def form_bitbucket_request(url):
        http = urllib3.PoolManager(ca_certs=certifi.where())
        return http.request('GET', url)


def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return 

def switch_to_dir(dir_name):
    #print("Current Working Directory " , os.getcwd())
    try: 
        os.chdir(dir_name)
        #print("Directory changed")
    except OSError:
        print("Can't change the Current Working Directory") 
    #print("Current Working Directory " , os.getcwd())

def get_file_count(rootdir):
    cpp_file_count = []
    py_file_count = []
    md_file_count = []

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if (file.endswith(".cpp")):
                cpp_file_count.append(file)
            if(file.endswith(".py")):
                py_file_count.append(file)
            if (file.endswith(".md")):
                md_file_count.append(file)
    return len(cpp_file_count), len(py_file_count), len(md_file_count)

def get_commit_count():
    switch_to_dir('git_repos')
    commit_hash = []
    commit_date = []
    commit_msg_data = []
    commit_data = {}

    g = git.cmd.Git(name)
    repo = git.Repo(name)
    url = repo.remote("origin").url
    #print(url)
    #g.pull()
    num_of_commits = len(list(repo.iter_commits()))
    switch_to_dir('../')
    return num_of_commits, url

def get_contributors(repo_name):
    contributors = int(subprocess.check_output("cd " + "git_repos/"+ repo_name + ";git shortlog -s HEAD | wc -l", shell=True))
    return contributors

def get_git_prs(repo_name):
    # get PR count
    response = form_github_request("https://api.github.com/search/issues?q=repo:"+repo_name+"%20is:pr&per_page=1")
    data = response.data
    prs = json.loads(data.decode(sys.stdout.encoding))
    #print(prs)
    try:
        num_pr = prs['total_count']
        return num_pr
    except Exception as e:
        print("wrong repo: "+repo_name)
        return repo_name


def get_git_issues(repo_name):

    # get issue count
    response = form_github_request("https://api.github.com/search/issues?q=repo:"+repo_name+"%20is:issue&per_page=1")
    data = response.data
    issues = json.loads(data.decode(sys.stdout.encoding))
    try:
        num_issues = issues['total_count']
        return num_issues
    except Exception as e:
        print("wrong repo: "+repo_name)
        return repo_name



def get_bitb_prs(repo_name):
    # get MERGED prs
    response = form_bitbucket_request("https://api.bitbucket.org/2.0/repositories/"+repo_name+"/pullrequests?state=MERGED")
    data = response.data
    m_prs = json.loads(data.decode(sys.stdout.encoding))
    num_pr_m = m_prs['values']

    # get OPEN prs
    response = form_bitbucket_request("https://api.bitbucket.org/2.0/repositories/"+repo_name+"/pullrequests?state=OPEN")
    data = response.data
    o_prs = json.loads(data.decode(sys.stdout.encoding))
    num_pr_o = o_prs['values']

    # get DECLINED prs
    response = form_bitbucket_request("https://api.bitbucket.org/2.0/repositories/"+repo_name+"/pullrequests?state=DECLINED")
    data = response.data
    d_prs = json.loads(data.decode(sys.stdout.encoding))
    num_pr_d = d_prs['values']

    return (len(num_pr_m)+len(num_pr_o)+len(num_pr_d))


############################
####### MAIN PROGRAM #######
############################
columns = defaultdict(list)
repo_names = []
repo_urls = []
#git_repos_names = [dI for dI in os.listdir('git_repos') if os.path.isdir(os.path.join('git_repos',dI))]

with open('Repos_all.csv') as f:
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


for name in repo_names:
    rootdir = 'git_repos/'+name
    commit_data = {}

    cpp_file_count, py_file_count, md_file_count = get_file_count(rootdir)
    commits_num, url = get_commit_count()

    commit_data['url'] = url
    commit_data['commits'] = commits_num

    contributors = get_contributors(name)

    if "bitbucket" in url:
        r_name = url[url.index("bitbucket.org/") + len("bitbucket.org/"):]
        prs = get_bitb_prs(r_name)
    else:
        r_name = url[url.index("github.com/") + len("github.com/"):]
        if 'autowarefoundation/autoware' in r_name:
            r_name = 'autowarefoundation/autoware.ai'
        elif 'bluesat/owr_software' in r_name:
            r_name = 'Offworld-Robotics/numbat_software'
        elif 'CopterExpress/clever' in r_name:
            r_name = 'CopterExpress/clover'
        elif 'enesdemirag/point-cloud-filters' in r_name:
            r_name = 'enesdemirag/simpcl'
        elif 'googlecartographer/cartographer_ros' in r_name:
            r_name = 'cartographer-project/cartographer_ros'
        elif 'JHS-ARCC-Club/jetson_car' in r_name:
            r_name = 'ARCC-RACE/jetson_car'
        elif 'osu-uwrt/riptide_software' in r_name:
            r_name = 'osu-uwrt/riptide_setup'
        # print(r_name)
        prs = get_git_prs(r_name)
        issues = get_git_issues(r_name)

        commit_data['issues'] = issues

    commit_data['prs'] = prs
    commit_data['contributors'] = contributors

    commit_data['cpp'] = cpp_file_count
    commit_data['py'] = py_file_count
    commit_data['md'] = md_file_count
    json_data = json.dumps(commit_data)

    with open('data/repo_stats1.json', 'a') as outfile:
        outfile.write(json_data)
        outfile.write(",")
        outfile.write("\n")
        outfile.close()
