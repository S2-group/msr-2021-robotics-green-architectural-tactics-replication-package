import csv
import json
from collections import defaultdict
from itertools import zip_longest

def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return

def get_column(file_name):
    columns = defaultdict(list)
    with open(file_name) as f:
        reader = csv.DictReader(no_blank(f))
        for row in reader:
            for (k,v) in row.items(): 
                columns[k].append(v)
    return columns

def random_name_to_url():

    columns_url = get_column('data/energy_commit_data_new.csv')
    urls = []

    while '' in columns_url['URL']:
        columns_url['URL'].remove('')


    columns_repo_name = get_column('data/repo_name.csv')

    for name in columns_repo_name['\ufeffRepoName']:
        print(name)
        for url in columns_url['URL']:
            if url.endswith(name):
                urls.append(url)

    urls_list = [urls]
    export_data = zip_longest(*urls_list, fillvalue='')

    with open('random_url_commit_data.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("URL"))
        wr.writerows(export_data)
    myfile.close()

def remove_bad_so():
    with open('../../phase1_data_collection/data/stackoverflow_data.json') as f:
        so_data = json.load(f)

    new_so_data = [item for item in so_data if item['url'].startswith('https://stackoverflow.com')]
    so_url = [item.get('url') for item in new_so_data]
    print(so_url)
    with open('../../phase1_data_collection/data/new_stackoverflow_data.json', 'a') as outfile:
        for item in new_so_data:
        outfile.write(json.dumps(item))
        outfile.write(",")
        outfile.write("\n")
    outfile.close()

##############################
######## MAIN PROGRAM ########
##############################

#random_name_to_url()
#remove_bad_so()

