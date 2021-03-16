import csv
import json
from itertools import zip_longest

with open('../energy_detectors/data/new_github-issues_data.json') as f:
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

for i in range(len(git_issue_url)):
    y = "GitIssue" + str(i)
    git_issue_id.append(y)

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

for i in range(593):
    rcontents = git_issue_contents_new[
        i] + '' + git_issue_code_new[i] + '' + git_issue_quotes_new[i] + '' + git_issue_details_new[i] + '' + git_issue_details_m_new[i]
    raw_contents.append(rcontents)

# print(len(raw_contents))

power_keyword = 'power'
battery_keyword = 'battery'
energy_keyword = 'energy'
sustain_keyword = 'sustainab'
green_keyword = 'green'

raw_contents_final = []
for rc in raw_contents:
    if (power_keyword in rc):
        a, b = rc.split(power_keyword, 1)
        a = a[-45:]
        b = b[0:45]
        power_string = a + power_keyword + b
        raw_contents_final.append(power_string)
    elif (battery_keyword in rc):
        a, b = rc.split(battery_keyword, 1)
        a = a[-45:]
        b = b[0:45]
        battery_string = a + battery_keyword + b
        raw_contents_final.append(battery_string)
    elif (energy_keyword in rc):
        a, b = rc.split(energy_keyword, 1)
        a = a[-45:]
        b = b[0:45]
        energy_string = a + energy_keyword + b
        raw_contents_final.append(energy_string)
    elif (sustain_keyword in rc):
        a, b = rc.split(sustain_keyword, 1)
        a = a[-45:]
        b = b[0:45]
        sustain_string = a + sustain_keyword + b
        raw_contents_final.append(sustain_string)
    elif (green_keyword in rc):
        a, b = rc.split(green_keyword, 1)
        a = a[-45:]
        b = b[0:45]
        green_string = a + green_keyword + b
        raw_contents_final.append(green_string)
    else:
        other_string = rc[0:90]
        raw_contents_final.append(other_string)

# print(raw_contents_final[10])


for battery in raw_contents:
    b = battery.count('batter')
    git_issue_battery.append(b)

for power in raw_contents:
    p = power.count('power')
    git_issue_power.append(p)

for energy in raw_contents:
    e = energy.count('energy')
    git_issue_energy.append(e)

for sustainab in raw_contents:
    s = sustainab.count('sustainab')
    git_issue_sustain.append(s)

for green in raw_contents:
    g = green.count('green')
    git_issue_green.append(g)

git_issue_list = [git_issue_id,
                  git_issue_url,
                  collection_name,
                  git_issue_title,
                  raw_contents_final,
                  git_issue_battery,
                  git_issue_energy,
                  git_issue_power,
                  git_issue_sustain,
                  git_issue_green
                  ]

export_data = zip_longest(*git_issue_list, fillvalue='')

with open('data/new_energy_data.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()
