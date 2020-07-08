import shelve
import copy
import json

# INPUT DATA SOURCE FILENAME
INPUT_FILE_NAME = 'fdg_input_file.json'
OUTPUT_FILE_NAME = 'fdg_output_file'
# Maximum distance to be considered
MAX_DISTANCE = 10



def build_schema(distance):
    """
    Builds schema for an individual node
    """
    schema = {}
    for i in range(distance):
        schema[str(i+1)] = []
    return schema

def create_adjacency_list(aggregate_data):
    """
    Converts the {'nodes': [], 'links': []} into Adjancency List
    """
    links = aggregate_data['links']
    adjacency_list = {}

    for link in links:
        key = link['source']
        if not key in adjacency_list:
            adjacency_list[key] = []
        if not link['target'] in adjacency_list:
            adjacency_list[link['target']] = []

        adjacency_list[key].append({
            "target": link['target'],
            "value": link['value']
        })
    return adjacency_list


def bfs(adj_list, node):
    """
    Breadth First Search Traversal 
    """
    visited = []
    visited.append(node)
    distance_list = copy.deepcopy(schema)
    q = []
    q.append({"node": node, "level": 0})
    while q:
        front = q.pop(0)
        currNode = front['node']
        currLevel = front['level']
        if(int(currLevel) >= MAX_DISTANCE):
            continue
        for i in adj_list[currNode]:
            if not i in visited:
                q.append({'node': i['target'], 'level': currLevel+1})
                distance_list[str(currLevel+1)].append(i)
                visited.append(i)

    return distance_list

def dump_json(output_list):
    """
    Creates a python dictionary and dumps a JSON object
    """
    json_output_list = {}
    for key in output_list:
        json_output_list[key] = output_list[key]

    open(OUTPUT_FILE_NAME+'.json', 'w').write(json.dumps(json_output_list, indent=2))



# Building schema
schema = build_schema(MAX_DISTANCE)

# Loading Input File
input_file = open(INPUT_FILE_NAME).read()
aggregate_data = json.loads(input_file)
# Building Adjacency List
adjacency_list = create_adjacency_list(aggregate_data)

# Opening shelve instance
output_list = shelve.open(OUTPUT_FILE_NAME, writeback=True)

# Calling BFS on every node and adding the nodes inside output_list
for node in adjacency_list:
    # calling bfs from node
    distance_list_of_node = bfs(adjacency_list, node)
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

# DEBUG: 
# print('REDUNDANT_NODES: ', redundant_nodes, len(redundant_nodes))

output_list.sync()

# Uncomment this to output JSON file [Only to visualize the data]
# dump_json(output_list)


output_list.close()