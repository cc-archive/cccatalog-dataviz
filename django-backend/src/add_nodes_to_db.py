"""Use the following script in Django Shell"""

import json
from dataviz_api.models import Node
import shelve
import datetime

DB_PATH = "./dataviz_api/data/graph_dB"
base_time = datetime.datetime.now()

with shelve.open(DB_PATH) as db:
    count=0
    for node in db:
        if node['provider_domain'] == "Domain not available":
            index = node['id']
        else:
            index = node['provider_domain']

        instance = Node(id = db[node]['metadata']['id'], index=index)
        instance.save()
        count+=1
        if count%1000:
            print(f"Added ${count}, Time Elapsed: ${datetime.datetime.now() - base_time}")

    print("Number of Nodes Added: ", count)