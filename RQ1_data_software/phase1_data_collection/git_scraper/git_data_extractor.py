import json
import glob
import os
import re
import csv
from collections import defaultdict

######################################
##### GET NAMES OF DESIRED FILES #####
######################################
def get_file_names(rootdir):
	comments_file_names = []
	#or file.endswith(".h")
	md_file_names = []
	for root, dirs, files in os.walk(rootdir):
		for file in files:
			if (file.endswith(".cpp") or file.endswith(".py")):
				comments_file_names.append(file)
			if (file.endswith(".md")):
				md_file_names.append(file)
	return comments_file_names, md_file_names

######################################
########### GET FILE PATHS ###########
######################################
def get_file_path(rootdir):
	for subdir, dirs, files in os.walk(rootdir):
	    for file in files:
	        #print os.path.join(subdir, file)
	        #or filepath.endswith(".h")
	        filepath = subdir + os.sep + file

	        if (filepath.endswith(".cpp") 
	        	or filepath.endswith(".py")):
	            comments_file_location.append(filepath)
	        if (filepath.endswith(".md")):
	        	md_location.append(filepath)
	return comments_file_location, md_location

######################################
##### GET CONTENTS OF .MD FILES ######
######################################
def extract_md_contents(md_location):
	contents = ""
	data = {}
	for location in md_location:
		md_contents = []
		with open(location, "r") as f:
			contents = f.readlines()
			file_name = location.split('/')[-1]
			md_contents.append(contents)
			data[location]=md_contents
	return data

######################################
### GET CONTENTS OF C++ SRC FILES ####
######################################
def extract_source_code_comments_c(comments_file_location):
	data = {}
	# iterate through .cpp files only
	comments_file_location = [s for s in comments_file_location if ".cpp" in s]
	for location in comments_file_location:
		comments_c = []
		try:
			with open(location, "r") as f:
				contents = f.readlines()
				file_name = location.split('/')[-1]
				for line in contents:
					# if (re.search(r'//', line) or re.search(r'#', line) 
					# and not re.search(r'#include', line) and not re.search(r'#ifndef', line)
					# and not re.search(r'#endif', line) and not re.search(r'#define', line)):
					#line = str(line)
					comment_search_c = re.search('//(.*)\n', line, re.IGNORECASE)
					comment_search_c1 = re.search("/\*(.*)\*", line, re.IGNORECASE)
					if comment_search_c:
						comment = comment_search_c.group(1)
						comments_c.append(comment)
						data[file_name]=comments_c
					elif comment_search_c1:
						comment = comment_search_c1.group(1)
						comments_c.append(comment)
						data[file_name]=comments_c
		except UnicodeDecodeError:
			pass # Found non-text data
	return data

######################################
### GET CONTENTS OF PYTHON SRC FILES #
######################################
def extract_source_code_comments_p(comments_file_location):
	data = {}
	# iterate through .py files only
	comments_file_location = [s for s in comments_file_location if ".py" in s]
	for location in comments_file_location:
		comments_p = []
		try:
			with open(location, "r") as f:
				contents = f.readlines() 
				file_name = location.split('/')[-1]
				for line in contents:
					#line = str(line)
					comment_search_p = re.search('#(.*)\n', line, re.IGNORECASE)
					comment_search_p1 = re.search('#ifndef(.*)\n', line, re.IGNORECASE)
					comment_search_p2 = re.search('#define(.*)\n', line, re.IGNORECASE)
					comment_search_p3 = re.search('#include(.*)\n', line, re.IGNORECASE)
					comment_search_p4 = re.search('#endif(.*)\n', line, re.IGNORECASE)
					comment_search_p5 = re.search('#ifdef(.*)\n', line, re.IGNORECASE)
					if (comment_search_p and not comment_search_p1 and not comment_search_p2
						and not comment_search_p3 and not comment_search_p4 and not comment_search_p5):
						comment = comment_search_p.group(1)
						comments_p.append(comment)
						data[file_name]=comments_p
		except UnicodeDecodeError:
			pass # Found non-text data
	return data

######################################
######## CREATE JSON OBJECT ##########
######################################
def create_json(md_file_contents, source_comments_c, source_comments_p, comments_file_names, 
	md_file_names, git_repo):
	data['git_repo_name'] = git_repo
	#data['url'] = url
	data['code_comments_file_names'] = comments_file_names
	data['md_file_names'] = md_file_names
	data['md_contents'] = md_file_contents
	data['code_comments_c++'] = source_comments_c
	data['code_comments_python'] = source_comments_p
	json_data = json.dumps(data)
	#print(data)
	return data

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
def sort_key(s):
	s = s.split('/')[-1]
	print(s)
	return s

############################
####### MAIN PROGRAM #######
############################
git_repos_names = [dI for dI in os.listdir('git_repos') if os.path.isdir(os.path.join('git_repos',dI))]

for git_repo in git_repos_names:
	data = {}
	feeds = []
	comments_file_location  = []
	md_location = []
	rootdir = 'git_repos/'+git_repo
	#print(rootdir)
	#get the file names 
	comments_file_names, md_file_names = get_file_names(rootdir)
	# get the location of desired files
	comments_file_location, md_location = get_file_path(rootdir)
	#print(md_file_names)
	#print(md_location)
	#print(comments_file_location)
	# get the contents of .md files
	extracted_md_contents = extract_md_contents(md_location)
	#print(extracted_md_contents)
	# get the comments from the c++ source code files
	extracted_comments_c = extract_source_code_comments_c(comments_file_location)
	# #extract_source_code_comments_c(comments_file_location)
	# #extracted_comments_c = []
	# #print(extracted_comments_c)
	extracted_comments_p = extract_source_code_comments_p(comments_file_location)
	final_data = create_json(extracted_md_contents, extracted_comments_c, 
	 	extracted_comments_p, comments_file_names, md_file_names, git_repo)
	# print(final_data)
	with open('data/git_repos1_data.json', 'a') as outfile:
		outfile.write(json.dumps(final_data))
		outfile.write(",")
		outfile.write("\n")
		outfile.close()

