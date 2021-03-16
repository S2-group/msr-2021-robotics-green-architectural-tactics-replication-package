import csv
import json
from itertools import zip_longest

with open('../energy_detectors/data/new_stackoverflow_data.json') as f:
    stackoverflow_data = json.load(f)

stackoverflow_url = [item.get('url') for item in stackoverflow_data]
stackoverflow_question = [item.get('post_content')
                          for item in stackoverflow_data]
stackoverflow_answer = [item.get('answer') for item in stackoverflow_data]
stackoverflow_qcode = [item.get('question_code')
                       for item in stackoverflow_data]
stackoverflow_acode = [item.get('answer_code') for item in stackoverflow_data]
stackoverflow_title = [item.get('title') for item in stackoverflow_data]
stackoverflow_id = []
stackoverflow_battery = []
stackoverflow_energy = []
stackoverflow_sustain = []
stackoverflow_power = []
stackoverflow_green = []
stackoverflow_question_new = []
stackoverflow_answer_new = []
stackoverflow_question_code_new = []
stackoverflow_answer_code_new = []
collection_name = []
raw_contents = []

for i in range(len(stackoverflow_url)):
    y = "SO" + str(i)
    stackoverflow_id.append(y)

for i in range(len(stackoverflow_url)):
    collection_name.append("StackOverflow")

for questions in stackoverflow_question:
    questions = ''.join(questions)
    stackoverflow_question_new.append(questions)

for answers in stackoverflow_answer:
    answers = ''.join(answers)
    stackoverflow_answer_new.append(answers)

for qcode in stackoverflow_qcode:
    try:
        qcode = ''.join(qcode)
        stackoverflow_question_code_new.append(qcode)
    except TypeError:
        qcode = ''
        stackoverflow_question_code_new.append(qcode)

for acode in stackoverflow_acode:
    try:
        acode = ''.join(acode)
        stackoverflow_answer_code_new.append(acode)
    except TypeError:
        acode = ''
        stackoverflow_answer_code_new.append(acode)

# print(len(stackoverflow_question_new))
# print(len(stackoverflow_answer_new))
# print(len(stackoverflow_question_code_new))
# print(len(stackoverflow_answer_code_new))

for i in range(32):
    rcontents = stackoverflow_question_new[i] + '' + stackoverflow_question_code_new[
        i] + '' + stackoverflow_answer_new[i] + '' + stackoverflow_answer_code_new[i]
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
    stackoverflow_battery.append(b)

for power in raw_contents:
    p = power.count('power')
    stackoverflow_power.append(p)

for energy in raw_contents:
    e = energy.count('energy')
    stackoverflow_energy.append(e)

for sustainab in raw_contents:
    s = sustainab.count('sustainab')
    stackoverflow_sustain.append(s)

for green in raw_contents:
    g = green.count('green')
    stackoverflow_green.append(g)

stackoverflow_list = [stackoverflow_id,
                      stackoverflow_url,
                      collection_name,
                      stackoverflow_title,
                      raw_contents_final,
                      stackoverflow_battery,
                      stackoverflow_energy,
                      stackoverflow_power,
                      stackoverflow_sustain,
                      stackoverflow_green
                      ]

export_data = zip_longest(*stackoverflow_list, fillvalue='')

with open('data/energy_data_new.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()
