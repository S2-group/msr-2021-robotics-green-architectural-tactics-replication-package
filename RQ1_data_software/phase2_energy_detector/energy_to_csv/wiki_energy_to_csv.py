import csv
import json
from itertools import zip_longest

with open('../../phase1_data_collection/data/wiki_data.json') as f:
    wiki_data = json.load(f)

wiki_url = [item.get('url') for item in wiki_data]
wiki_package = [item.get('package')
                          for item in wiki_data]
wiki_summary = [item.get('package_summary') for item in wiki_data]
wiki_details = [item.get('package_details')
                       for item in wiki_data]
wiki_tt = [item.get('package_tt') for item in wiki_data]
wiki_code = [item.get('package_code') for item in wiki_data]
wiki_id = []
wiki_battery = []
wiki_energy = []
wiki_sustain = []
wiki_power = []
wiki_green = []
wiki_summary_new = []
wiki_details_new = []
wiki_tt_new = []
wiki_code_new = []
collection_name = []
raw_contents = []

for i in range(len(wiki_url)):
    y = "W" + str(i)
    wiki_id.append(y)

for i in range(len(wiki_url)):
    collection_name.append("Wiki")

for summary in wiki_summary:
    summary = ''.join(summary)
    wiki_summary_new.append(summary)

for details in wiki_details:
    try:
        details = ''.join(details)
        wiki_details_new.append(details)
    except TypeError:
        details = ''
        wiki_details_new.append(details)

for tt in wiki_tt:
    try:
        tt = ''.join(tt)
        wiki_tt_new.append(tt)
    except TypeError:
        tt = ''
        wiki_tt_new.append(tt)

for code in wiki_code:
    try:
        code = ''.join(code)
        wiki_code_new.append(code)
    except TypeError:
        code = ''
        wiki_code_new.append(code)

# print(len(wiki_question_new))
# print(len(wiki_answer_new))
# print(len(wiki_question_code_new))
# print(len(wiki_answer_code_new))

for i in range(60):
    rcontents = wiki_summary_new[i] + '' + wiki_details_new[
        i] + '' + wiki_tt_new[i] + '' + wiki_code_new[i]
    raw_contents.append(rcontents)

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


for battery in raw_contents:
    b = battery.count('batter')
    wiki_battery.append(b)

for power in raw_contents:
    p = power.count('power')
    wiki_power.append(p)

for energy in raw_contents:
    e = energy.count('energy')
    wiki_energy.append(e)

for sustainab in raw_contents:
    s = sustainab.count('sustainab')
    wiki_sustain.append(s)

for green in raw_contents:
    g = green.count('green')
    wiki_green.append(g)

wiki_list = [wiki_id,
                      wiki_url,
                      collection_name,
                      wiki_package,
                      raw_contents_final,
                      wiki_battery,
                      wiki_energy,
                      wiki_power,
                      wiki_sustain,
                      wiki_green
                      ]

export_data = zip_longest(*wiki_list, fillvalue='')

with open('data/all_wiki_data.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()
