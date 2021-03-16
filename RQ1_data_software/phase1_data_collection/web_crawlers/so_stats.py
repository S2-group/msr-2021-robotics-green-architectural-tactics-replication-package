import json

def count_user():
	with open('../data/so_stats.json') as f:
		user_data = json.load(f)
		so_user = [item.get('user') for item in user_data]

	user_frequency = {x:so_user.count(x) for x in so_user}
	so_user, frequency = user_frequency.keys(), user_frequency.values()

	print(len(so_user))
	print(len(frequency))

	with open('../data/so_user_frequency.txt', mode='wt', encoding='utf-8') as myfile:
	    for item in frequency:
	        myfile.write(str(item) + '\n')

count_user()