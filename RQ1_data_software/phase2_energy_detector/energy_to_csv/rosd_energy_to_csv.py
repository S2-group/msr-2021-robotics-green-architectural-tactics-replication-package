import csv
import json
from itertools import zip_longest

with open('../energy_detectors/data/ros-discourse_data.json') as f:
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

for i in range(197):
    rcontents = rosd_tcontents_new[i] + '' + rosd_tdetails_new[i]
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

# print(raw_contents_final[56])


for battery in raw_contents:
    b = battery.count('batter')
    rosd_battery.append(b)

for power in raw_contents:
    p = power.count('power')
    rosd_power.append(p)

for energy in raw_contents:
    e = energy.count('energy')
    rosd_energy.append(e)

for sustainab in raw_contents:
    s = sustainab.count('sustainab')
    rosd_sustain.append(s)

for green in raw_contents:
    g = green.count('green')
    rosd_green.append(g)

rosd_list = [rosd_id,
             rosd_url,
             collection_name,
             rosd_title,
             raw_contents_final,
             rosd_battery,
             rosd_energy,
             rosd_power,
             rosd_sustain,
             rosd_green
             ]

export_data = zip_longest(*rosd_list, fillvalue='')

with open('data/energy_data.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()
