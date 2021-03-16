import csv
import json
from itertools import zip_longest
from collections import defaultdict
import re
from collections import Counter
def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return

def return_longest_list(list1, list2, list3):
    if (len(list1) > len(list2) and len(list1) > len(list3)):
        return list1
    elif (len(list2) > len(list1) and len(list2) > len(list3)):
        return list2
    elif (len(list3) > len(list1) and len(list3) > len(list2)):
        return list3
    # else:
    #     return list1
    else:
        if (len(list1) != 0):
            return list1
        elif (len(list2) != 0):
            return list2
        elif (len(list3) != 0):
            return list3

columns = defaultdict(list)
with open('data/Repos_all.csv') as f:
    reader = csv.DictReader(no_blank(f))
    for row in reader:
        for (k,v) in row.items(): 
            columns[k].append(v)

while '' in columns['URL']:
    columns['URL'].remove('')

with open('../../phase1_data_collection/git_scraper/data/git_repos_data.json') as f:
    repo_data = json.load(f)

repo_url = []
repo_name = [item.get('git_repo_name') for item in repo_data]
repo_name_new = []
repo_md_contents = [item.get('md_contents') for item in repo_data]
repo_md_file = [item.get('md_file_names') for item in repo_data]
repo_code_c = [item.get('code_comments_c++') for item in repo_data]
repo_code_p = [item.get('code_comments_python') for item in repo_data]
repo_id = []
collection_name = []
new_dicts_md = []
new_dicts_p = []
new_dicts_c = []
new_repo_url = []
new_repo_url1 = []
new_repo_name = []
new_repo_name1 = []

for name in repo_name:
    for url in columns['URL']:
        if url.endswith(name):
            print(name+": ",url)
            repo_url.append(url)
            repo_name_new.append(name)
print(len(repo_url))
print(len(repo_name_new))
print(len(repo_name))

repo_name = repo_name_new
#print(len(repo_name))
# print(len(set(repo_name)))
d =  Counter(repo_name)
res = [k for k, v in d.items() if v > 1]
#print(res)

for mcontents in repo_md_contents:
    for key in mcontents.keys():
        mcontents[key] = ''.join(mcontents[key])

for cpp in repo_code_c:
    for key in cpp.keys():
        cpp[key] = ''.join(cpp[key])

for py in repo_code_p:
    for key in py.keys():
        py[key] = ''.join(py[key])

# # consum_keyword = 'consum'
power_keyword = 'power'
battery_keyword = 'battery'
energy_keyword = 'energy'
sustain_keyword = 'sustainab'
green_keyword = 'green'

combo = [repo_md_contents, repo_code_c, repo_code_p]

for c in combo:
    for mcontents in c:
        for key in mcontents.keys():
            # if(consum_keyword in mcontents[key]):
            #     print('consum')
            #     a,b = mcontents[key].split(consum_keyword, 1)
            #     a = a[-45:]
            #     b = b[0:45]
            #     consum_string = a + consum_keyword + b
            #     mcontents[key] = consum_string
            if(power_keyword in mcontents[key]):
                a,b = mcontents[key].split(power_keyword, 1)
                a = a[-45:]
                b = b[0:45]
                power_string = a + power_keyword + b
                mcontents[key] = power_string
            elif(battery_keyword in mcontents[key]):
                a,b = mcontents[key].split(battery_keyword, 1)
                a = a[-45:]
                b = b[0:45]
                battery_string = a + battery_keyword + b
                mcontents[key] = battery_string
            elif(energy_keyword in mcontents[key]):
                a,b = mcontents[key].split(energy_keyword, 1)
                a = a[-45:]
                b = b[0:45]
                energy_string = a + energy_keyword + b
                mcontents[key] = energy_string
            elif(sustain_keyword in mcontents[key]):
                a,b = mcontents[key].split(sustain_keyword, 1)
                a = a[-45:]
                b = b[0:45]
                sustain_string = a + sustain_keyword + b
                mcontents[key] = sustain_string
            elif(green_keyword in mcontents[key]):
                a,b = mcontents[key].split(green_keyword, 1)
                a = a[-45:]
                b = b[0:45]
                green_string = a + green_keyword + b
                mcontents[key] = green_string
            else:
                other_string = mcontents[key][0:90]
                mcontents[key] = other_string



for cpp in repo_code_c:
    for k, v in list(cpp.items()):
        if (('power' not in v) and ('energy' not in v) and ('battery' not in v) and ('green' not in v)
            and ('sustainab' not in v)):
            del cpp[k]
# # for cpp in repo_code_c:
# #     for k, v in list(cpp.items()):
# #         if ('consum' not in v):
# #             del cpp[k]
for py in repo_code_p:
    for k, v in list(py.items()):
        if (('power' not in v) and ('energy' not in v) and ('battery' not in v) and ('green' not in v)
            and ('sustainab' not in v)):
            del py[k]
# # for py in repo_code_p:
# #     for k, v in list(py.items()):
# #         if ('consum' not in v):
# #             del py[k]

for md in repo_md_contents:
    for k, v in list(md.items()):
        if (('power' not in v) and ('energy' not in v) and ('battery' not in v) and ('green' not in v)
            and ('sustainab' not in v)):
            del md[k]
# for md in repo_md_contents:
#     for k, v in list(md.items()):
#         if ('consum' not in v):
#             del md[k]

# # print(len(repo_md_contents))
# # print(len(repo_code_c))
# # print(len(repo_code_p))

for c in repo_code_c:
    if (len(c.keys()) == 0):
        c['message'] = 'no data'
    for k, v in c.items():
        new_code_c = {}
        new_code_c[k] = v
        new_dicts_c.append(new_code_c)

#print(new_dicts_c)

for p in repo_code_p:
    if (len(p.keys()) == 0):
        p['message'] = 'no data'
    for k, v in p.items():
        new_code_p = {}
        new_code_p[k] = v
        new_dicts_p.append(new_code_p)
#print(len(new_dicts_p))

for m in repo_md_contents:
    if (len(m.keys()) == 0):
        m['message'] = 'no data'
    for k, v in m.items():
        new_md = {}
        new_md[k] = v
        new_dicts_md.append(new_md)
#print(new_dicts_md)


i = 0
for url in repo_url:
    longest_list = return_longest_list(repo_code_p[i], repo_md_contents[i], repo_code_c[i])
    new_repo_url.append([url] * len(repo_code_p[i]))
    i = i + 1

for url_list in new_repo_url:
    for url in url_list:
        new_repo_url1.append(url)

i = 0
for name in repo_name:
    longest_list = return_longest_list(repo_code_p[i], repo_md_contents[i], repo_code_c[i])
    new_repo_name.append([name] * len(repo_code_p[i]))
    i = i + 1

for name_list in new_repo_name:
    for name in name_list:
        new_repo_name1.append(name)

for i in range(len(new_repo_name1)):
    y = "REPO_P" + str(i)
    repo_id.append(y)

for i in range(len(new_repo_name1)):
    collection_name.append("Repositories")

print(len(repo_id))
print(len(new_repo_url1))
print(len(new_repo_name1))
print(len(collection_name))
print(len(new_dicts_md))
print(len(new_dicts_p))
print(len(new_dicts_c))





repo_list = [repo_id,
             new_repo_url1,
             new_repo_name1,
             collection_name,
             new_dicts_p
             ]

export_data = zip_longest(*repo_list, fillvalue='')

with open('data/repo_split_p.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("ID", "URL", "Repo Name", "Collection", "Contents"))
    # wr.writerow(("ID", "URL", "Repo Name", "Collection", "MD Contents"))
    wr.writerows(export_data)
myfile.close()
