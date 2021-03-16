import urllib
import requests
import json
import time
from bs4 import BeautifulSoup

def get_stats():
	stat_dict = {}
	with open('../data/rosd_data.json') as f:
		url_data = json.load(f)
		rosd_url = [item.get('url') for item in url_data]
	url = rosd_url
	#url = ['https://discourse.ros.org/t/dns-change-for-build-ros2-org/9202']

	for u in url:
		page = requests.get(u,timeout=None)

		soup = BeautifulSoup(page.text, 'html.parser')
		try:
			time = soup.find('time')
			if time.has_attr('datetime'):
				post_time = time['datetime']
			user = ''
			li = soup.find('span', {'class': 'creator'})
			children = li.findChildren("a" , recursive=False)
			for child in children:
			    user = child.text
		except  AttributeError:
			post_time = 'no_date'
			user = 'no_user'

		# print(post_time)
		# print(user)
		# print(u)

		stat_dict['url'] = u
		stat_dict['post_time'] = post_time
		stat_dict['user'] = user
		print(stat_dict)
		if stat_dict['user'] is 'no_user' and stat_dict['post_time'] is 'no_date':
			pass
		else:
			with open('../data/rosd_stats.json', 'a') as outfile:
				outfile.write(json.dumps(stat_dict))
				outfile.write(",")
				outfile.write("\n")
			outfile.close()

def count_user():
	with open('../data/rosd_stats.json') as f:
		user_data = json.load(f)
		rosd_user = [item.get('user') for item in user_data]

	user_frequency = {x:rosd_user.count(x) for x in rosd_user}
	rosd_user, frequency = user_frequency.keys(), user_frequency.values()

	print(len(rosd_user))
	print(len(frequency))

	with open('../data/rosd_user_frequency.txt', mode='wt', encoding='utf-8') as myfile:
	    for item in frequency:
	        myfile.write(str(item) + '\n')

count_user()