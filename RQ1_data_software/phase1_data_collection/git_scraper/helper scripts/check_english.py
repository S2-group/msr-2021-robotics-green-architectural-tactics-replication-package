import json
from collections import defaultdict
import pycld2 as cld2

def isEnglish(s):
	try:
		s.encode(encoding='utf-8').decode('ascii')
	except UnicodeDecodeError:
		return False
	else:
		return True


with open('/Users/agukalpa/Desktop/thesis/green_tactics_ROS/phase1_data_collection/git_scraper/data/github-closed-pr_data.json') as f:
	e = json.load(f)
pr_contents = [item.get('pr_contents') for item in e]

text = []
print(len(e))
seen = set()
e = [i for n, i in enumerate(e) if i not in e[n + 1:]]
print(len(e))

with open('data/github-closed-pr-final_data.json', 'a') as outfile:
	outfile.write(json.dumps(e))
	outfile.close()

# for contents in pr_contents:
# 	try:
# 		text.append(contents)
# 	except TypeError:
# 		pass
# #print(text)
# for t in text:
# 	print(next(item for item in e if item["pr_contents"] == t))
	# list(filter(lambda content: content['pr_contents'] == t, e))
# for contents in pr_contents:
# 	try:
# 		for text in contents:
# 			isReliable, textBytesFound, details = cld2.detect(text)
# 			#print(isReliable)
# 			if isEnglish(text) is False:
# 				#print(text)
# 				list(filter(lambda content: content['pr_contents'] == text, e))
# 	except TypeError:
# 		pass
		#isReliable, textBytesFound, details = cld2.detect(contents)


# for title in pr_titles:
# 	isReliable, textBytesFound, details = cld2.detect(title)

# 	#print(isReliable)
# 	#print(details[0])
# 	if isReliable is False:
# 		print(title)
