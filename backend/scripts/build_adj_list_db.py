import json
import datetime
import pymongo
import os

DIST = 'D' # Prefix in every node distance key [eg. D1, D2]
REV_DIST = 'RD'
DBNAME = "graph_dB"
INPUT_FILENAME = 'fdg_input_file.json'
base_time = datetime.datetime.now()

USERNAME=os.environ.get('MONGO_INITDB_ROOT_USERNAME')
PASSWORD=os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
MONGO_DB_NAME=os.environ.get('MONGO_DB_NAME')
MONGO_COLLECTION_NAME=os.environ.get('MONGO_COLLECTION_NAME')


def main(
    adjacency_shelf_name=DBNAME,
    input_filename=INPUT_FILENAME
):
    with open(input_filename) as f:
        data = json.loads(f.read())

    init_adjacency_shelf(adjacency_shelf_name, data)



def init_adjacency_shelf(adjacency_shelf_name, aggregate_data):
    """
    Stores adjacency Map or distance 1 list with nodes metadata into shelve dB
    """
    adjacency_map = init_adjacency_map(aggregate_data)
    add_node_metadata(adjacency_map, aggregate_data)
    print(
        f'{datetime.datetime.now() - base_time}'
        f' Saving Adjacency map to shelf DB: {adjacency_shelf_name}'
    )
    client = pymongo.MongoClient(f'mongodb://{USERNAME}:{PASSWORD}@localhost:27017')
    db = client.get_database(name=MONGO_DB_NAME)
    node_collection = db.get_collection(name=MONGO_COLLECTION_NAME)
    count=0
    curr_batch=[]
    for k in adjacency_map:
        curr_batch.append({"_id": k, **adjacency_map[k]})
        count+=1
        if(count%1000==0):
            node_collection.insert_many(curr_batch)
            curr_batch.clear()
            print(
                f'{datetime.datetime.now()-base_time}',
                f'Added {count} nodes'
            )

    # Adding elems which are left
    node_collection.insert_many(curr_batch)
    print(
        f'{datetime.datetime.now()-base_time}',
        f'Added {count} nodes'
    )
    print(
        f'{datetime.datetime.now() - base_time}'
        f' Adjacency Map saved'
    )


def init_adjacency_map(aggregate_data):
    """
    Converts the {'nodes': [], 'links': []} into Adjancency Map
    """
    print(
        f'{datetime.datetime.now() - base_time}'
        f' Creating adjacency map'
    )
    links = aggregate_data['links']
    adjacency_map = {}
    dist_1_out_key = f'{DIST}1'
    dist_1_in_key = f'{REV_DIST}1'

    for link in links:
        adjacency_map.setdefault(
            link['source'], {dist_1_out_key: [], dist_1_in_key:[]}
        )[dist_1_out_key].append({"target": link['target'], "value": link['value']})

        adjacency_map.setdefault(
            link['target'], {dist_1_out_key: [], dist_1_in_key:[]}
        )[dist_1_in_key].append({"source": link['source'], "value": link['value']})
    print(
        f'{datetime.datetime.now() - base_time}'
        f' Adjacency map created. Length: {len(adjacency_map)}'
    )
    return adjacency_map


def add_node_metadata(adjacency_map, aggregate_data):
    print(
        f'{datetime.datetime.now() - base_time}'
        f' Adding nodes metadata'
    )
    dist_1_out_key = f'{DIST}1'
    dist_1_in_key = f'{REV_DIST}1'
    
    nodes = aggregate_data['nodes']
    for node in nodes:
        curr_node = node
        if(curr_node['cc_licenses']):
            curr_node['cc_licenses']=json.dumps(curr_node['cc_licenses'])

        adjacency_map.setdefault(
            node['id'], {dist_1_out_key: [], dist_1_in_key:[]}
        )['metadata'] = curr_node

    print(
        f'{datetime.datetime.now() - base_time}'
        f' Nodes metadata added.'
    )


if __name__ == '__main__':
    main()