'''
The following file converts the graph data schema, to distance list format.
'''
import json
import copy
import shelve

INPUT_FILE_NAME = 'fdg_input_file.json'
OUTPUT_FILE_NAME = 'fdg_output_file'
MAX_DISTANCE = 10


schema = {}

for i in range(MAX_DISTANCE):
    schema[str(i+1)] = []


input_file = open(INPUT_FILE_NAME).read()

aggregate_data = json.loads(input_file)
links = aggregate_data['links']
nodes = aggregate_data['nodes']

adjacencyList = {}

for link in links:
    key = link['source']
    if not key in adjacencyList:
        adjacencyList[key] = []
    if not link['target'] in adjacencyList:
        adjacencyList[link['target']] = []

    adjacencyList[key].append({
        "target": link['target'],
        "value": link['value']
    })



def bfs(adjList, node):
    visited = []
    visited.append(node)
    distanceList = copy.deepcopy(schema)
    q = []
    q.append({"node": node, "level": 0})
    while q:
        front = q.pop(0)
        currNode = front['node']
        currLevel = front['level']
        if(int(currLevel) >= MAX_DISTANCE):
            continue
        for i in adjList[currNode]:
            if not i in visited:
                q.append({'node': i['target'], 'level': currLevel+1})
                distanceList[str(currLevel+1)].append(i)
                visited.append(i)

    return distanceList


output_list = shelve.open(OUTPUT_FILE_NAME, writeback=True)

for node in adjacencyList:
    # calling bfs from node
    distance_list_of_node = bfs(adjacencyList, node)
    # adding to output_list
    output_list[node] = distance_list_of_node


redundant_nodes = []

# Adding metadata
for node in nodes:
    try:
        # output_list[node['id']]['metadata'] = {key: value for key, value in node.items() if key not in 'id'}
        output_list[node['id']]['metadata'] = node
    except Exception as e:
        redundant_nodes.append(e.args[0])

print('REDUNDANT_NODES: ', redundant_nodes, len(redundant_nodes))

output_list.sync()

# Output JSON file
json_output_list = {}
for key in output_list:
    json_output_list[key] = output_list[key]

# open(OUTPUT_FILE_NAME+'.json', 'w').write(json.dumps(json_output_list, indent=2))

output_list.close()


