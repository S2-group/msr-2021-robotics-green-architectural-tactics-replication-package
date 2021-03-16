import csv
import json
from itertools import zip_longest

commit_battery = []
commit_energy = []
commit_power = []
commit_green = []
commit_sus = []


with open('data/commits_split.json') as f:
    commit_data = json.load(f)

commit_info = [item.get('Commit Info') for item in commit_data]

### BATTERY COUNT
for battery in commit_info:
    b = battery.count('batter')
    commit_battery.append(b)
print(len(commit_battery))

### ENERGY COUNT
for energy in commit_info:
    e = energy.count('energy')
    commit_energy.append(e)
print(len(commit_energy))

### POWER COUNT
for power in commit_info:
    p = power.count('power')
    commit_power.append(p)
print(len(commit_power))

### GREEN COUNT
for green in commit_info:
    g = green.count('green')
    commit_green.append(g)
print(len(commit_green))

### SUSTAINAB COUNT
for sus in commit_info:
    s = sus.count('sustainab')
    commit_sus.append(s)
print(len(commit_sus))

keyword_list = [
                commit_battery,
                commit_energy,
                commit_power,
                commit_sus,
                commit_green
               ]

export_data = zip_longest(*keyword_list, fillvalue='')

with open('data/commit_keyword_data.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()