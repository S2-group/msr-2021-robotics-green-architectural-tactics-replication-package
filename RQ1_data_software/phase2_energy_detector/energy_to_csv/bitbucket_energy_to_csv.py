import csv
import json
from itertools import zip_longest

with open('../energy_detectors/data/bitbucket_pr_data.json') as f:
    bitbucket_data = json.load(f)

bitbucket_url = [item.get('url') for item in bitbucket_data]
bitbucket_contents = [item.get('pr_contents') for item in bitbucket_data]
bitbucket_title = [item.get('pr_title') for item in bitbucket_data]
bitbucket_id = []
bitbucket_battery = []
bitbucket_energy = []
bitbucket_sustain = []
bitbucket_power = []
bitbucket_green = []
bitbucket_contents_new = []
collection_name = []

for i in range(len(bitbucket_url)):
    y = "B" + str(i)
    bitbucket_id.append(y)

for i in range(len(bitbucket_url)):
    collection_name.append("BitBucketPR")

for contents in bitbucket_contents:
    c = contents.rstrip()
    bitbucket_contents_new.append(c)

for battery in bitbucket_contents:
    b = battery.count('batter')
    bitbucket_battery.append(b)

for power in bitbucket_contents:
    p = power.count('power')
    bitbucket_power.append(p)

for energy in bitbucket_contents:
    e = energy.count('energy')
    bitbucket_energy.append(e)

for sustainab in bitbucket_contents:
    s = sustainab.count('sustainab')
    bitbucket_sustain.append(s)

for green in bitbucket_contents:
    g = green.count('green')
    bitbucket_green.append(g)

bitbucket_list = [bitbucket_id,
                  bitbucket_url,
                  collection_name,
                  bitbucket_title,
                  bitbucket_contents,
                  bitbucket_battery,
                  bitbucket_energy,
                  bitbucket_power,
                  bitbucket_sustain,
                  bitbucket_green
                  ]

export_data = zip_longest(*bitbucket_list, fillvalue='')

with open('data/energy_data.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("ID", "URL", "Collection", "Title", "Contents",
                 "Battery", "Energy", "Power", "Sustainab", "Green"))
    wr.writerows(export_data)
myfile.close()
print(bitbucket_id)
print(bitbucket_url)
print(bitbucket_contents_new)
print(bitbucket_title)
print(bitbucket_battery)
