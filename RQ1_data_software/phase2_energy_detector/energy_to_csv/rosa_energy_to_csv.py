import csv
import json
from itertools import zip_longest

with open('../energy_detectors/data/ros-answers_data.json') as f:
    rosa_data = json.load(f)

rosa_url = [item.get('url') for item in rosa_data]
rosa_contents = [item.get('post_content')
                 for item in rosa_data]
rosa_answer = [item.get('answer') for item in rosa_data]
rosa_qdetails = [item.get('question_details') for item in rosa_data]
rosa_adetails = [item.get('answer_details') for item in rosa_data]
rosa_qcode = [item.get('question_code') for item in rosa_data]
rosa_acode = [item.get('answer_code') for item in rosa_data]
rosa_title = [item.get('title') for item in rosa_data]
rosa_id = []
rosa_battery = []
rosa_energy = []
rosa_sustain = []
rosa_power = []
rosa_green = []
rosa_contents_new = []
rosa_answer_new = []
rosa_qdetails_new = []
rosa_adetails_new = []
rosa_qcode_new = []
rosa_acode_new = []

collection_name = []
raw_contents = []

for i in range(len(rosa_url)):
    y = "ROSA" + str(i)
    rosa_id.append(y)

for i in range(len(rosa_url)):
    collection_name.append("ROSAnswers")

for contents in rosa_contents:
    try:
        contents = ''.join(contents)
        rosa_contents_new.append(contents)
    except TypeError:
        contents = ''
        rosa_contents_new.append(contents)

for answer in rosa_answer:
    try:
        answer = ''.join(answer)
        rosa_answer_new.append(answer)
    except TypeError:
        answer = ''
        rosa_answer_new.append(answer)

for qdetails in rosa_qdetails:
    try:
        qdetails = ''.join(qdetails)
        rosa_qdetails_new.append(qetails)
    except TypeError:
        qetails = ''
        rosa_qdetails_new.append(qetails)

for adetails in rosa_adetails:
    try:
        adetails = ''.join(adetails)
        rosa_adetails_new.append(aetails)
    except TypeError:
        aetails = ''
        rosa_adetails_new.append(aetails)

for acode in rosa_acode:
    try:
        acode = ''.join(acode)
        rosa_acode_new.append(acode)
    except TypeError:
        acode = ''
        rosa_acode_new.append(acode)

for qcode in rosa_qcode:
    try:
        qcode = ''.join(qcode)
        rosa_qcode_new.append(qcode)
    except TypeError:
        qcode = ''
        rosa_qcode_new.append(qcode)


# print(len(rosa_url))
# print(len(rosa_title))
# print(len(rosa_contents_new))
# print(len(rosa_answer_new))
# print(len(rosa_qdetails_new))
# print(len(rosa_adetails_new))

for i in range(1227):
    rcontents = rosa_contents_new[
        i] + '' + rosa_qdetails_new[i] + '' + rosa_qcode_new[i] + '' + rosa_answer_new[i] + '' + rosa_adetails_new[i] + '' + rosa_acode_new[i]
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

# print(raw_contents_final[4])


for battery in raw_contents:
    b = battery.count('batter')
    rosa_battery.append(b)

for power in raw_contents:
    p = power.count('power')
    rosa_power.append(p)

for energy in raw_contents:
    e = energy.count('energy')
    rosa_energy.append(e)

for sustainab in raw_contents:
    s = sustainab.count('sustainab')
    rosa_sustain.append(s)

for green in raw_contents:
    g = green.count('green')
    rosa_green.append(g)

rosa_list = [rosa_id,
             rosa_url,
             collection_name,
             rosa_title,
             raw_contents_final,
             rosa_battery,
             rosa_energy,
             rosa_power,
             rosa_sustain,
             rosa_green
             ]

export_data = zip_longest(*rosa_list, fillvalue='')

with open('data/energy_data.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()
