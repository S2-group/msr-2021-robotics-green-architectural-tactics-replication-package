import json
import glob
import os
import re
import csv
import sys
import urllib.request, json
from urllib.request import urlopen
import ssl
from collections import defaultdict

ssl._create_default_https_context = ssl._create_unverified_context

######################################
######## CREATE JSON OBJECT ##########
######################################
def create_json(url, pr_title, username, posted_on, pr_contents, pr_comments):
	data = {}
	data['url'] = url
	data['pr_title'] = pr_title
	data['username'] = username
	data['status'] = "Declined"
	data['posted_on'] = posted_on
	data['pr_contents'] = pr_contents
	data['pr_comments'] = pr_comments
	return data
# url to crawl
bitbucket_urls_raw = [
                    'https://bitbucket.org/!api/2.0/repositories/_Luc_/hand_control/pullrequests?pagelen=25&fields=%2Bvalues.participants&q=state%3D"DECLINED"&page=1',
                    'https://bitbucket.org/!api/2.0/repositories/acl-mit/rvo_path_planner/pullrequests?pagelen=25&fields=%2Bvalues.participants&q=state%3D"DECLINED"&page=1',
                    'https://bitbucket.org/!api/2.0/repositories/AndyZe/pid/pullrequests?pagelen=25&fields=%2Bvalues.participants&q=state%3D"DECLINED"&page=1',
                    'https://bitbucket.org/!api/2.0/repositories/traclabs/trac_ik/pullrequests?pagelen=25&fields=%2Bvalues.participants&q=state%3D%22DECLINED%22&page=1',
                    'https://bitbucket.org/!api/2.0/repositories/udg_cirs/cola2_core/pullrequests?pagelen=25&fields=%2Bvalues.participants&q=state%3D"DECLINED"&page=1',
                    'https://bitbucket.org/!api/2.0/repositories/whoidsl/ds_base/pullrequests?pagelen=25&fields=%2Bvalues.participants&q=state%3D"DECLINED"&page=1',
                    'https://bitbucket.org/!api/2.0/repositories/whoidsl/ds_nav/pullrequests?pagelen=25&fields=%2Bvalues.participants&q=state%3D"DECLINED"&page=1',
                    'https://bitbucket.org/!api/2.0/repositories/whoidsl/ds_sensors/pullrequests?pagelen=25&fields=%2Bvalues.participants&q=state%3D"DECLINED"&page=1'
                    ]
bitbucket_urls = [
				'https://bitbucket.org/_Luc_/hand_control',
				'https://bitbucket.org/acl-mit/rvo_path_planner',
				'https://bitbucket.org/AndyZe/pid',
				'https://bitbucket.org/traclabs/trac_ik',
				'https://bitbucket.org/udg_cirs/cola2_core',
				'https://bitbucket.org/whoidsl/ds_base',
				'https://bitbucket.org/whoidsl/ds_nav',
				'https://bitbucket.org/whoidsl/ds_sensors'
				 ]
j = 0
for link in bitbucket_urls_raw:
	pr_contents = []
	pull_request_number = []
	display_name = []
	username = ""
	# start crawling urs
	with urllib.request.urlopen(link) as url:
		data = json.loads(url.read().decode())
	# get PR titles 	
	title = [title['title'] for title in data['values']]
	# get PR description
	description = [description['description'] for description in data['values']]
	# get PR author
	author = [author['author'] for author in data['values']]
	for a in author:
		# if author is "null" (deleted user), rewrite author name
		try:
			if a['display_name']:
				username = a['display_name']
				display_name.append(username)
		except TypeError:
			username = "former author"
			display_name.append(username)
	# get PR post date
	post_date = [post_date['created_on'] for post_date in data['values']]
	# get PR #
	pr_number = [pr_number['links'] for pr_number in data['values']]
	pr_number = [link['decline'] for link in pr_number]
	pr_number = [linkk['href'] for linkk in pr_number]
	for number in pr_number:
		pr_final_number = re.search('pullrequests/(.+?)/decline', number).group(1)
		pull_request_number.append(pr_final_number)
	# get PR comments
	links = [links['links'] for links in data['values']]
	comment_links = [comment_links['comments'] for comment_links in links]
	comment_links_clean = [comment_links_clean['href'] for comment_links_clean in comment_links]
	for linkk in comment_links_clean:
		with urllib.request.urlopen(linkk) as url:
			comments = json.loads(url.read().decode())
		contents = [contents['content'] for contents in comments['values']]
		raw_contents = [raw_contents['raw'] for raw_contents in contents]
		pr_contents.append(raw_contents)

	b = [bitbucket_urls[j]] * len(title)
	print(b)
	for i in range(len(title)):
		json_data = create_json(b[i]+"/pull-requests/"+pull_request_number[i], title[i], display_name[i], post_date[i], description[i], pr_contents[i])
		#print(json_data)
		with open('data/bitbucket_pr_data.json', 'a') as outfile:
			outfile.write(json.dumps(json_data))
			outfile.write(",")
			outfile.write("\n")
			outfile.close()
	j = j + 1