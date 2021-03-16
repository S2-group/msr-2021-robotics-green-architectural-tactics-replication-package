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
	a=random.sample(range(start,end), 25)
	data=dataset.loc[a]
	data.to_csv (r'data/random_data.csv', index = False, header=True, encoding='ISO-8859-1')



start = 2
end = 210
select_random_rows(start, end, 'commit_data.csv')