"""Use the following script in Django Shell"""

import json
from dataviz_api.models import Node

FILE_PATH = "./dataviz_api/data/fdg_output_file.json"

data = open(FILE_PATH).read()
json_data = json.loads(data)
nodes = json_data['nodes']

count=0
for i in nodes:
    instance = Node(id = i['id'], provider_domain=i['provider_domain'])
    instance.save()
    count+=1

print("Number of Nodes Added: ", count)