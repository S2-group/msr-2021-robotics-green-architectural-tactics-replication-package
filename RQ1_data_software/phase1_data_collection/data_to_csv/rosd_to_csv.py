import csv
import json
from itertools import zip_longest

with open('../data/ros-discourse_data.json') as f:
    rosd_data = json.load(f)

rosd_url = [item.get('url') for item in rosd_data]
rosd_tcontents = [item.get('thread_contents')
                  for item in rosd_data]
rosd_tdetails = [item.get('thread_details') for item in rosd_data]
rosd_title = [item.get('title') for item in rosd_data]
rosd_id = []
rosd_battery = []
rosd_energy = []
rosd_sustain = []
rosd_power = []
rosd_green = []
rosd_tcontents_new = []
rosd_tdetails_new = []

collection_name = []
raw_contents = []

for i in range(len(rosd_url)):
    y = "ROSD" + str(i)
    rosd_id.append(y)

for i in range(len(rosd_url)):
    collection_name.append("ROSDiscourse")

for contents in rosd_tcontents:
    contents = ''.join(contents)
    rosd_tcontents_new.append(contents)

for details in rosd_tdetails:
    try:
        details = ''.join(details)
        rosd_tdetails_new.append(details)
    except TypeError:
        details = ''
        rosd_tdetails_new.append(details)


# print(len(rosd_url))
# print(len(rosd_title))
# print(len(rosd_tcontents_new))
# print(len(rosd_tdetails_new))

for i in range(2604):
    rcontents = rosd_tcontents_new[i] + '' + rosd_tdetails_new[i]
    raw_contents.append(rcontents)

raw_contents_final = []
for rc in raw_contents:
    other_string = rc[0:90]
    raw_contents_final.append(other_string)

# print(len(raw_contents))

rosd_list = [rosd_id,
             rosd_url,
             collection_name,
             rosd_title,
             raw_contents_final,
             ]

export_data = zip_longest(*rosd_list, fillvalue='')

with open('data/social_discussion.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()
