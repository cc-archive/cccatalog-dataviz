"""Use the following script in Django Shell"""

import json
from dataviz_api.models import Node
import shelve
import datetime

DB_PATH = "./dataviz_api/data/graph_dB"
base_time = datetime.datetime.now()
BATCH_SIZE = 10000

with shelve.open(DB_PATH) as db:
    count = 0
    nodes_list = []
    for node_id in db:
        node = db[node_id]["metadata"]
        if node["provider_domain"] == "Domain not available":
            index = node["id"]
        else:
            index = node["provider_domain"]

        instance = {"id": node["id"], "index": index}
        nodes_list.append(Node(**instance))
        count += 1
        if count % BATCH_SIZE == 0:
            # break
            Node.objects.bulk_create(nodes_list)
            nodes_list.clear()
            print(
                f"Added ${count}, Time Elapsed: ${datetime.datetime.now() - base_time}"
            )


print("Number of Nodes Added: ", count)
