import csv
import json
from itertools import zip_longest
from collections import defaultdict
import random
import pandas as pd
import fileinput
import itertools

def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return

def select_random_rows(start, end, file_name):
	dataset = pd.read_csv(file_name, encoding='ISO-8859-1')
<<<<<<< HEAD
	a=random.sample(range(start,end), 15)
	data=dataset.loc[a]
	data.to_csv (r'../data/random_sample_wiki.csv', index = False, header=True, encoding='ISO-8859-1')



start = 31
end = 60
select_random_rows(start, end, 'data/wiki_energy.csv')
=======
	a=random.sample(range(start,end), 50)
	data=dataset.loc[a]
	data.to_csv (r'../data/random_sample.csv', index = False, header=True, encoding='ISO-8859-1')



start = 2
end = 73
select_random_rows(start, end, '../data/temp_data.csv')
>>>>>>> 360ea5007f4ab0c6d47e6bdcbb41773e87be1c30
