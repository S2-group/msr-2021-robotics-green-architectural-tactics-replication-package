import json
from iteration_utilities import unique_everseen

with open('web_crawlers/WikiCrawler/WikiCrawler/spiders/data.json') as f:
    wiki_data = json.load(f)


print(len(wiki_data))
new_wiki_data = list(unique_everseen(wiki_data))
print(len(new_wiki_data))

with open('data/wiki_data.json', 'a') as outfile:
	for item in new_wiki_data:
		outfile.write(json.dumps(item))
		outfile.write(",")
		outfile.write("\n")
	outfile.close()