import shelve
import copy
import json
import datetime

# INPUT DATA SOURCE FILENAME
INPUT_FILE_NAME = 'test.json'
OUTPUT_FILE_NAME = 'fdg_output_file'

# Maximum distance to be considered
MAX_DISTANCE = 10

base_time = datetime.datetime.now()


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


def build_distance_list(adj_list, node, visited, distance_list):
    """
    Traverses the component and builds/update the distance_list
    """
    visited.add(node)
    q = []
    q.append({"node": node, "parent": []})
    while q:
        front = q.pop(0)
        curr_node = front['node']
        parent = front['parent']
        parent.append(curr_node)
        # Keeping only last [MAX_DISTANCE] nodes
        if(len(parent) > MAX_DISTANCE):
            parent.pop(0)

        # For every node directly connected [At distance one] from the curr_node
        for i in adj_list[curr_node]:
            # Updating the parent's distance_list
            for j in enumerate(reversed(parent)):
                if j[1] not in distance_list:
                    distance_list[j[1]] = copy.deepcopy(schema)

                if j[0]==0:
                    # If the distance (j[0]+1) is one from the j[1] node. Pushing the nodeName and the value/weight of the link 
                  distance_list[j[1]]['1'].append(i)
                else:
                    # If the distance is > 1. Pushing only nodeName
                  distance_list[j[1]][str(j[0]+1)].append(i['target'])
            
            # Checking if the node is already travered or not
            if not i['target'] in visited:
                q.append({'node': i['target'], 'parent': copy.deepcopy(parent)})
                visited.add(i['target'])

    return distance_list

def dump_json(output_list):
    """
    Creates a python dictionary and dumps a JSON object
    """
    json_output_list = {}
    for key in output_list:
        json_output_list[key] = output_list[key]

    open(OUTPUT_FILE_NAME+'.json', 'w').write(json.dumps(json_output_list, indent=2))


def display_time(message):
    curr_time = datetime.datetime.now()
    print(message + " : ", curr_time - base_time)

# Building schema
schema = build_schema(MAX_DISTANCE)

# Loading Input File
input_file = open(INPUT_FILE_NAME).read()
aggregate_data = json.loads(input_file)
curr_time = datetime.datetime.now()
display_time("Data Loaded")

# Building Adjacency List
adjacency_list = create_adjacency_list(aggregate_data)
curr_time = datetime.datetime.now()
display_time("Adjacency List Successfully Built")

temp_output_list = {}

# Set to store the visited nodes
visited = set()

# Calling build_distance_list on every node which is not yet traversed
for node in adjacency_list:
    if node not in visited:
        # calling build_distance_list from node
        build_distance_list(adjacency_list, node, visited, temp_output_list)

display_time("Distance List Successfully Built")


# Opening shelve instance
output_list = shelve.open(OUTPUT_FILE_NAME)

# DEBUG: List to store the nodes which are are completely isolated (Both indegree and outdegree zero)
zero_indeg_nodes = []

nodes = aggregate_data['nodes']
# Adding metadata to all nodes
for node in nodes:
    if node['id'] not in temp_output_list:
        temp_output_list[node['id']] = copy.deepcopy(schema)
        zero_indeg_nodes.append(node['id'])
    temp_output_list[node['id']]['metadata'] = node
    # output_list[node['id']] = temp_output_list[node['id']]


output_list.update(temp_output_list)

# DEBUG: 
# print('zero_indeg_nodes: ', len(zero_indeg_nodes))

display_time("Nodes Metadata Successfully Added")

# Uncomment this to output JSON file [Only to visualize the data]
# dump_json(temp_output_list)

output_list.close()
display_time("Operation Successful")