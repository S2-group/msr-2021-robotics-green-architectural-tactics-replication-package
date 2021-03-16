import csv
import json
from itertools import zip_longest

with open('../git_scraper/data/github-open-pr_data.json') as f:
    git_pr_data = json.load(f)

git_pr_url = [item.get('url') for item in git_pr_data]
git_pr_contents = [item.get('pr_contents')
                   for item in git_pr_data]
git_pr_comments = [item.get('pr_comments')
                   for item in git_pr_data]
git_pr_code = [item.get('pr_code') for item in git_pr_data]
git_pr_quotes = [item.get('pr_quotes') for item in git_pr_data]
git_pr_details = [item.get('pr_details') for item in git_pr_data]
git_pr_details_m = [item.get('pr_details_more') for item in git_pr_data]
git_pr_title = [item.get('pr_title') for item in git_pr_data]
git_pr_id = []
git_pr_battery = []
git_pr_energy = []
git_pr_sustain = []
git_pr_power = []
git_pr_green = []
git_pr_contents_new = []
git_pr_comments_new = []
git_pr_code_new = []
git_pr_quotes_new = []
git_pr_details_new = []
git_pr_details_m_new = []

collection_name = []
raw_contents = []

z = 28995
for i in range(len(git_pr_url)):
    y = "GitPR" + str(z)
    git_pr_id.append(y)
    z = z + 1

for i in range(len(git_pr_url)):
    collection_name.append("GitHubPRs")

for contents in git_pr_contents:
    try:
        contents = ''.join(contents)
        git_pr_contents_new.append(contents)
    except TypeError:
        contents = ''
        git_pr_contents_new.append(contents)

for comments in git_pr_comments:
    try:
        comments = ''.join(comments)
        git_pr_comments_new.append(comments)
    except TypeError:
        comments = ''
        git_pr_comments_new.append(comments)

for code in git_pr_code:
    try:
        code = ''.join(code)
        git_pr_code_new.append(code)
    except TypeError:
        code = ''
        git_pr_code_new.append(code)

for quotes in git_pr_quotes:
    try:
        quotes = ''.join(quotes)
        git_pr_quotes_new.append(quotes)
    except TypeError:
        quotes = ''
        git_pr_quotes_new.append(quotes)

for details in git_pr_details:
    try:
        details = ''.join(details)
        git_pr_details_new.append(details)
    except TypeError:
        details = ''
        git_pr_details_new.append(details)

for details_m in git_pr_details_m:
    try:
        details_m = ''.join(details_m)
        git_pr_details_m_new.append(details_m)
    except TypeError:
        details_m = ''
        git_pr_details_m_new.append(details_m)


# print(len(git_pr_url))
# print(len(git_pr_title))
# print(len(git_pr_contents_new))
# print(len(git_pr_answer_new))
# print(len(git_pr_qdetails_new))
# print(len(git_pr_adetails_new))

for i in range(1031):
    rcontents = git_pr_contents_new[
        i] + '' + git_pr_code_new[i] + '' + git_pr_comments_new[i] + '' + git_pr_quotes_new[i] + '' + git_pr_details_new[i] + '' + git_pr_details_m_new[i]
    raw_contents.append(rcontents)

# print(len(raw_contents))

raw_contents_final = []
for rc in raw_contents:
    other_string = rc[0:90]
    raw_contents_final.append(other_string)

git_pr_list = [git_pr_id,
               git_pr_url,
               collection_name,
               git_pr_title,
               raw_contents_final
               ]

export_data = zip_longest(*git_pr_list, fillvalue='')

with open('data/energy_data.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()
