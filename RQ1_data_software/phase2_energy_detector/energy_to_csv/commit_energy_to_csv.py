import csv
import json
from itertools import zip_longest
from collections import defaultdict
import re
from collections import Counter

with open('../../phase1_data_collection/git_scraper/data/commit_data_new.json') as f:
    commit_data = json.load(f)

commit_url = [item.get('url') for item in commit_data]
commit_info = [item.get('commit_info') for item in commit_data]
repo_name = [item.get('repo_name') for item in commit_data]
commit_id = []
collection_name = []
new_dicts = []
new_commit_url = []
new_commit_url1 = []
new_repo_name = []
new_repo_name1 = []

for ci in commit_info:
    for i in ci:
        for key in i.keys():
            i[key] = ''.join(i[key])

# power_keyword = 'power'
# battery_keyword = 'batter'
# energy_keyword = 'energy'
# sustain_keyword = 'sustainab'
# green_keyword = 'green'

# for ci in commit_info:
#     for i in ci:
#         for key in i.keys():
#             if(power_keyword in i[key]):
#                 a,b = i[key].split(power_keyword, 1)
#                 a = a[-45:]
#                 b = b[0:45]
#                 power_string = a + power_keyword + b
#                 i[key] = power_string
#             elif(battery_keyword in i[key]):
#                 a,b = i[key].split(battery_keyword, 1)
#                 a = a[-45:]
#                 b = b[0:45]
#                 battery_string = a + battery_keyword + b
#                 i[key] = battery_string
#             elif(energy_keyword in i[key]):
#                 a,b = i[key].split(energy_keyword, 1)
#                 a = a[-45:]
#                 b = b[0:45]
#                 energy_string = a + energy_keyword + b
#                 i[key] = energy_string
#             elif(sustain_keyword in i[key]):
#                 a,b = i[key].split(sustain_keyword, 1)
#                 a = a[-45:]
#                 b = b[0:45]
#                 sustain_string = a + sustain_keyword + b
#                 i[key] = sustain_string
#             elif(green_keyword in i[key]):
#                 a,b = i[key].split(green_keyword, 1)
#                 a = a[-45:]
#                 b = b[0:45]
#                 green_string = a + green_keyword + b
#                 i[key] = green_string
#             else:
#                 other_string = i[key][0:90]
#                 i[key] = other_string



# for ci in commit_info:
#     for i in ci:
#         for k, v in list(i.items()):
#             if (('power' not in v) and ('energy' not in v) and ('batter' not in v) and ('green' not in v)
#                 and ('sustainab' not in v)):
#                 del i[k]

for ci in commit_info:
    for i in ci:
        for k, v in i.items():
            new_commit_info = {}
            new_commit_info[k] = v
            new_dicts.append(new_commit_info)

i = 0
for url in commit_url:
    new_commit_url.append([url] * len(commit_info[i][0]))
    i = i + 1

for url_list in new_commit_url:
    for url in url_list:
        new_commit_url1.append(url)
i = 0
for name in repo_name:
    new_repo_name.append([name] * len(commit_info[i][0]))
    i = i + 1

for name_list in new_repo_name:
    for name in name_list:
        new_repo_name1.append(name)

for i in range(len(new_repo_name1)):
    y = "C" + str(i)
    commit_id.append(y)

for i in range(len(commit_id)):
    collection_name.append("Commits")

# print(len(new_dicts))
# print(len(new_commit_url1))
# print(len(new_repo_name1))
# print(len(collection_name))
# print(len(commit_id))

commit_list = [commit_id,
               new_commit_url1,
               new_repo_name1,
               collection_name,
               new_dicts
              ]

export_data = zip_longest(*commit_list, fillvalue='')

with open('data/energy_commit_data_split_new.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("ID", "URL", "Repo Name", "Collection", "Commit Info"))
    wr.writerows(export_data)
myfile.close()