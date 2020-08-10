import shelve
import json
import datetime

DIST = "D"  # Prefix in every node distance key [eg. D1, D2]
DBNAME = "graph_dB"
INPUT_FILENAME = "fdg_input_file.json"
base_time = datetime.datetime.now()


def main(adjacency_shelf_name=DBNAME, input_filename=INPUT_FILENAME):
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
        f"{datetime.datetime.now() - base_time}"
        f" Saving Adjacency map to shelf DB: {adjacency_shelf_name}"
    )

    with shelve.open(adjacency_shelf_name) as db:
        for k in adjacency_map:
            db[k] = adjacency_map[k]
    print(f"{datetime.datetime.now() - base_time}" f" Adjacency Map saved")


def init_adjacency_map(aggregate_data):
    """
    Converts the {'nodes': [], 'links': []} into Adjancency Map
    """
    print(f"{datetime.datetime.now() - base_time}" f" Creating adjacency map")
    links = aggregate_data["links"]
    adjacency_map = {}
    dist_1_key = f"{DIST}1"

    for link in links:
        adjacency_map.setdefault(link["source"], {dist_1_key: []})[dist_1_key].append(
            {"target": link["target"], "value": link["value"]}
        )
        adjacency_map.setdefault(link["target"], {dist_1_key: []})
    print(
        f"{datetime.datetime.now() - base_time}"
        f" Adjacency map created. Length: {len(adjacency_map)}"
    )
    return adjacency_map


def add_node_metadata(adjacency_map, aggregate_data):
    print(f"{datetime.datetime.now() - base_time}" f" Adding nodes metadata")
    dist_1_key = f"{DIST}1"
    nodes = aggregate_data["nodes"]
    for node in nodes:
        adjacency_map.setdefault(node["id"], {dist_1_key: []})["metadata"] = node

    print(f"{datetime.datetime.now() - base_time}" f" Nodes metadata added.")


if __name__ == "__main__":
    main()
