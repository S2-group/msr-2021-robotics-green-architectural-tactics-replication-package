import json

def count_user():
	with open('../data/rosa_stats.json') as f:
		user_data = json.load(f)
		rosa_user = [item.get('user') for item in user_data]

	user_frequency = {x:rosa_user.count(x) for x in rosa_user}
	rosa_user, frequency = user_frequency.keys(), user_frequency.values()

	print(len(rosa_user))
	print(len(frequency))

	with open('../data/rosa_user_frequency.txt', mode='wt', encoding='utf-8') as myfile:
	    for item in frequency:
	        myfile.write(str(item) + '\n')

count_user()