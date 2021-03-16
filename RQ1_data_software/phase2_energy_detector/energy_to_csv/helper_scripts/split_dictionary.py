import json
import csv
from itertools import zip_longest
from collections import defaultdict

data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
dicts = []
for k, v in data.items():
	new_data = {}
	new_data[k] = v
	dicts.append(new_data)

print(dicts)