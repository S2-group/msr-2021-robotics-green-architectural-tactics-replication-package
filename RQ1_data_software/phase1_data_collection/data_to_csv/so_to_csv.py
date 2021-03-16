import csv
import json
from itertools import zip_longest

with open('../data/new_stackoverflow_data.json') as f:
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


for i in range(1880):
    rcontents = stackoverflow_question_new[i] + '' + stackoverflow_question_code_new[
        i] + '' + stackoverflow_answer_new[i] + '' + stackoverflow_answer_code_new[i]
    raw_contents.append(rcontents)

raw_contents_final = []
for rc in raw_contents:
    other_string = rc[0:90]
    raw_contents_final.append(other_string)


stackoverflow_list = [stackoverflow_id,
                      stackoverflow_url,
                      collection_name,
                      stackoverflow_title,
                      raw_contents_final
                      ]

export_data = zip_longest(*stackoverflow_list, fillvalue='')

with open('data/social_discussion.csv', 'a', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(export_data)
myfile.close()
