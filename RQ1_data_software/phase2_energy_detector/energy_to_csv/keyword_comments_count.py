import csv
import json
from itertools import zip_longest

repo_battery_md = []
repo_battery_c = []
repo_battery_p = []

repo_energy_md = []
repo_energy_c = []
repo_energy_p = []

repo_power_md = []
repo_power_c = []
repo_power_p = []

repo_green_md = []
repo_green_c = []
repo_green_p = []

repo_sus_md = []
repo_sus_c = []
repo_sus_p = []

with open('data/repos_split.json') as f:
    repo_data = json.load(f)

md_contents = [item.get('MD Contents') for item in repo_data]
#print(md_contents)

py_contents = [item.get('Python Contents') for item in repo_data]
#print(py_contents)

c_contents = [item.get('C++/C Contents') for item in repo_data]
#print(c_contents)

### BATTERY COUNT
for battery in md_contents:
    b = battery.count('batter')
    repo_battery_md.append(b)
#print(repo_battery_md)

for battery in py_contents:
    b = battery.count('batter')
    repo_battery_p.append(b)
#print(repo_battery_p)

for battery in c_contents:
    b = battery.count('battery')
    repo_battery_c.append(b)
print(len(repo_battery_c))

### ENERGY COUNT
for energy in md_contents:
    e = energy.count('energy')
    repo_energy_md.append(e)
#print(repo_battery_md)

for energy in py_contents:
    e = energy.count('energy')
    repo_energy_p.append(e)
#print(repo_battery_p)

for energy in c_contents:
    e = energy.count('energy')
    repo_energy_c.append(e)
print(len(repo_energy_c))

### POWER COUNT
for power in md_contents:
    p = power.count('power')
    repo_power_md.append(p)
#print(repo_battery_md)

for power in py_contents:
    p = power.count('power')
    repo_power_p.append(p)
#print(repo_battery_p)

for power in c_contents:
    p = power.count('power')
    repo_power_c.append(p)
print(len(repo_power_c))

### GREEN COUNT
for green in md_contents:
    g = green.count('green')
    repo_green_md.append(g)
#print(repo_battery_md)

for green in py_contents:
    g = green.count('green')
    repo_green_p.append(g)
#print(repo_battery_p)

for green in c_contents:
    g = green.count('green')
    repo_green_c.append(g)
print(len(repo_green_c))

### SUSTAINAB COUNT
for sus in md_contents:
    s = sus.count('sustainab')
    repo_sus_md.append(s)
#print(repo_battery_md)

for sus in py_contents:
    s = sus.count('sustainab')
    repo_sus_p.append(s)
#print(repo_battery_p)

for sus in c_contents:
    s = sus.count('sustainab')
    repo_sus_c.append(s)
print(len(repo_sus_c))

keyword_list = [
                repo_battery_md,
                repo_battery_c,
                repo_battery_p,
                repo_energy_md,
                repo_energy_c,
                repo_energy_p,
                repo_power_md,
                repo_power_c,
                repo_power_p,
                repo_sus_md,
                repo_sus_c,
                repo_sus_p,
                repo_green_md,
                repo_green_c,
                repo_green_p
               ]

export_data = zip_longest(*keyword_list, fillvalue='')

with open('data/repo_keyword_data.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()