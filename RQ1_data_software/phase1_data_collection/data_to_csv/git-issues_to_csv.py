import csv
import json
from itertools import zip_longest

with open('../git_scraper/data/github-closed-issues_data.json') as f:
    git_issue_data = json.load(f)

git_issue_url = [item.get('url') for item in git_issue_data]
git_issue_contents = [item.get('issue_contents') for item in git_issue_data]
git_issue_code = [item.get('issue_code') for item in git_issue_data]
git_issue_quotes = [item.get('issue_quotes') for item in git_issue_data]
git_issue_details = [item.get('contents_details') for item in git_issue_data]
git_issue_details_m = [item.get('contents_details_more')
                       for item in git_issue_data]
git_issue_title = [item.get('issue_title') for item in git_issue_data]
git_issue_id = []
git_issue_battery = []
git_issue_energy = []
git_issue_sustain = []
git_issue_power = []
git_issue_green = []
git_issue_contents_new = []
git_issue_code_new = []
git_issue_quotes_new = []
git_issue_details_new = []
git_issue_details_m_new = []

collection_name = []
raw_contents = []

z = 5721
for i in range(len(git_issue_url)):
    y = "GitIssue" + str(z)
    git_issue_id.append(y)
    z = z + 1

for i in range(len(git_issue_url)):
    collection_name.append("GitHubIssues")

for contents in git_issue_contents:
    try:
        contents = ''.join(contents)
        git_issue_contents_new.append(contents)
    except TypeError:
        contents = ''
        git_issue_contents_new.append(contents)

for code in git_issue_code:
    try:
        code = ''.join(code)
        git_issue_code_new.append(code)
    except TypeError:
        code = ''
        git_issue_code_new.append(code)

for quotes in git_issue_quotes:
    try:
        quotes = ''.join(quotes)
        git_issue_quotes_new.append(quotes)
    except TypeError:
        quotes = ''
        git_issue_quotes_new.append(quotes)

for details in git_issue_details:
    try:
        details = ''.join(details)
        git_issue_details_new.append(details)
    except TypeError:
        details = ''
        git_issue_details_new.append(details)

for details_m in git_issue_details_m:
    try:
        details_m = ''.join(details_m)
        git_issue_details_m_new.append(details_m)
    except TypeError:
        details_m = ''
        git_issue_details_m_new.append(details_m)


# print(len(git_issue_url))
# print(len(git_issue_title))
# print(len(git_issue_contents_new))
# print(len(git_issue_answer_new))
# print(len(git_issue_qdetails_new))
# print(len(git_issue_adetails_new))

for i in range(17493):
    rcontents = git_issue_contents_new[
        i] + '' + git_issue_code_new[i] + '' + git_issue_quotes_new[i] + '' + git_issue_details_new[i] + '' + git_issue_details_m_new[i]
    raw_contents.append(rcontents)

# print(len(raw_contents))
raw_contents_final = []
for rc in raw_contents:
    other_string = rc[0:90]
    raw_contents_final.append(other_string)



git_issue_list = [git_issue_id,
                  git_issue_url,
                  collection_name,
                  git_issue_title,
                  raw_contents_final,
                  ]

export_data = zip_longest(*git_issue_list, fillvalue='')

with open('data/pr_issue1.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()
