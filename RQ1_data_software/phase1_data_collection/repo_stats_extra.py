import json

with open('data/repo_stats.json') as f:
    repo_data = json.load(f)

python_repos = []
cpp_repos = []
both_repos = []
for r in repo_data:
	if (r['cpp'] is 0 and r['py'] is 0):
		print('both are 0')
	if (r['cpp'] is 0 and r['py'] is not 0):
		python_repos.append(r)
	if (r['cpp'] is not 0 and r['py'] is 0):
		cpp_repos.append(r)
	if (r['cpp'] is not 0 and r['py'] is not 0):
		both_repos.append(r)

print(len(python_repos))
print(len(cpp_repos))
print(len(both_repos))

python_json_data = json.dumps(python_repos)
cpp_json_data = json.dumps(cpp_repos)
both_json_data = json.dumps(both_repos)

with open('data/python_repo_stats.json', 'a') as outfile:
    outfile.write(python_json_data)
    outfile.write(",")
    outfile.write("\n")
    outfile.close()

with open('data/cpp_repo_stats.json', 'a') as outfile:
    outfile.write(cpp_json_data)
    outfile.write(",")
    outfile.write("\n")
    outfile.close()

with open('data/both_repo_stats.json', 'a') as outfile:
    outfile.write(both_json_data)
    outfile.write(",")
    outfile.write("\n")
    outfile.close()

