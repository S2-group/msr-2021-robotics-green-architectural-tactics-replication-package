import json

def count_user():
	with open('../data/wiki_stats.json') as f:
		user_data = json.load(f)
		wiki_user = [item.get('user') for item in user_data]

	user_frequency = {x:wiki_user.count(x) for x in wiki_user}
	wiki_user, frequency = user_frequency.keys(), user_frequency.values()

	print(len(wiki_user))
	print(len(frequency))

	with open('../data/wiki_user_frequency.txt', mode='wt', encoding='utf-8') as myfile:
	    for item in frequency:
	        myfile.write(str(item) + '\n')

count_user()