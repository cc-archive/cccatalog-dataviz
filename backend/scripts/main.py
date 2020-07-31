import shelve
import json
import datetime

MAX_DISTANCE = 2
DIST = 'D' # Prefix in every node distance key [eg. D1, D2]
DBNAME = "graph_DB_new_mod"
INPUT_FILENAME = 'fdg_input_file.json'
base_time = datetime.datetime.now()


def main(
        max_distance=MAX_DISTANCE,
        adjacency_shelf_name=DBNAME,
        input_filename=INPUT_FILENAME
):
    with open(input_filename) as f:
        data = json.loads(f.read())

    init_adjacency_shelf(adjacency_shelf_name, data)
    # Adding nodes at distance [2, MAX_DISTANCE]
    for d in range(2, MAX_DISTANCE+1):
        add_dx_list_to_adjacency_shelf(adjacency_shelf_name, d=d)


def init_adjacency_shelf(adjacency_shelf_name, aggregate_data):
    """
    Stores adjacency Map or distance 1 list into shelve dB
    """
    adjacency_map = init_adjacency_map(aggregate_data)
    print(
        f'{datetime.datetime.now() - base_time}'
        f' Saving Adjacency map to shelf DB: {adjacency_shelf_name}'
    )
    with shelve.open(adjacency_shelf_name) as db:
        for k in adjacency_map:
            db[k] = adjacency_map[k]
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
    dist_1_key = f'{DIST}1'

    for link in links:
        adjacency_map.setdefault(
            link['source'], {dist_1_key: set()}
        )[dist_1_key].add(link['target'])
        adjacency_map.setdefault(link['target'], {dist_1_key: set()})
    print(
        f'{datetime.datetime.now() - base_time}'
        f' Adjacency map created. Length: {len(adjacency_map)}'
    )
    return adjacency_map


def add_dx_list_to_adjacency_shelf(adjacency_shelf_name, d=2, dist_stub=DIST):
    """
    Finds set of nodes at distance [d] for every node in adjacency list
    """
    d_minus_1_key = f'{dist_stub}{d - 1}'
    d1_key = f'{dist_stub}1'
    count = 0
    print(
        f'{datetime.datetime.now() - base_time}'
        f' Adding {dist_stub}{d} set to {adjacency_shelf_name}'
    )
    with shelve.open(adjacency_shelf_name) as db:
        for key in db:
            node_adj_info = db[key]
            dx_set = {
                target
                for node in node_adj_info[d1_key]
                for target in db[node][d_minus_1_key]
            }
            for i in range(1, d):
                dx_set.difference_update(node_adj_info[f'{dist_stub}{i}'])
            node_adj_info[f'{dist_stub}{d}'] = dx_set
            db[key] = node_adj_info
            count += 1
            
            # Dumping the Batch into the shelve dB
            if count % 1000 == 0:
                print(f'{datetime.datetime.now() - base_time} Saved {count}')


if __name__ == '__main__':
    main()