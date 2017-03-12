import pandas as pd
import json

l=pd.read_json('yelp_academic_dataset_business.json',encoding='utf-8')

data = json.loads('yelp_academic_dataset_business.json',encoding='utf-8')

import pandas as pd

# read the entire file into a python array
with open('yelp_academic_dataset_business.json', 'rb') as f:
    data = f.readlines()

# remove the trailing "\n" from each line
data = map(lambda x: x.rstrip(), data)


data_json_str = "[" + ','.join(data) + "]"

# now, load it into pandas
data_df = pd.read_json(data)



with open('yelp_academic_dataset_business.json', 'rb') as f:
    for line in f:
          print(json.loads(line))
    
    
    
    data = f.readlines()
    
    
    
json_lines = [json.loads( l.strip() ) for l in open('yelp_academic_dataset_business.json',encoding='utf-8').readlines() ]