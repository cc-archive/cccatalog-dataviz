'''

The following file is a parser which converts the input data schema from {nodes:[], links:[]} to the distance list format.

'''

import shelve
# For DeepCopy
import copy
# For JSON file output
import json

# INPUT DATA SOURCE FILENAME
INPUT_FILE_NAME = 'fdg_input_file.json'
OUTPUT_FILE_NAME = 'fdg_output_file'
# Maximum distance to be considered
MAX_DISTANCE = 10



'''
Builds schema for an individual node
'''
def buildSchema(distance):
    schema = {}
    for i in range(distance):
        schema[str(i+1)] = []
    return schema

'''
Converts the {'nodes': [], 'links': []} into Adjancency List
'''
def createAdjacencyList(aggregate_data):
    links = aggregate_data['links']
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
    return adjacencyList


'''
Breadth First Search Traversal 
'''
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

'''
Creates a python dictionary and dumps a JSON object
'''
def dumpJSON(output_list):
    json_output_list = {}
    for key in output_list:
        json_output_list[key] = output_list[key]

    open(OUTPUT_FILE_NAME+'.json', 'w').write(json.dumps(json_output_list, indent=2))



# Building schema
schema = buildSchema(MAX_DISTANCE)

# Loading Input File
input_file = open(INPUT_FILE_NAME).read()
aggregate_data = json.loads(input_file)
# Building Adjacency List
adjacencyList = createAdjacencyList(aggregate_data)

# Opening shelve instance
output_list = shelve.open(OUTPUT_FILE_NAME, writeback=True)

# Calling BFS on every node and adding the nodes inside output_list
for node in adjacencyList:
    # calling bfs from node
    distance_list_of_node = bfs(adjacencyList, node)
    # adding to output_list
    output_list[node] = distance_list_of_node


# DEBUG: List to store the nodes which are are completely isolated (Both indegree and outdegree zero)
redundant_nodes = []

nodes = aggregate_data['nodes']
# Adding metadata to all nodes
for node in nodes:
    try:
        # output_list[node['id']]['metadata'] = {key: value for key, value in node.items() if key not in 'id'}
        output_list[node['id']]['metadata'] = node
    except Exception as e:
        # Appending all redundant nodes
        redundant_nodes.append(e.args[0])

# DEBUG: print('REDUNDANT_NODES: ', redundant_nodes, len(redundant_nodes))

output_list.sync()

# Uncomment this to output JSON file too
# dumpJSON(output_list)


output_list.close()


