import json
import datetime
import pymongo
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH=os.path.join(BASE_DIR, '..', '.env')

# Loading env variables
load_dotenv(ENV_PATH)

# Path of JSON file which will be inserted to the database. 
# A sample fdg_input_file.json can be found inside data-release/ directory.
INPUT_FILE_PATH = os.path.join(BASE_DIR, "fdg_input_file.json")

DIST = "D"  # Prefix in every node distance key [eg. D1, D2]
REV_DIST = "RD"
base_time = datetime.datetime.now()

# Fetching Mongo DB Credentials
try:
    USERNAME = os.environ['MONGO_INITDB_ROOT_USERNAME']
    PASSWORD = os.environ['MONGO_INITDB_ROOT_PASSWORD']
    MONGO_DB_NAME = os.environ['MONGO_DB_NAME']
    MONGO_COLLECTION_NAME = os.environ['MONGO_COLLECTION_NAME']
except KeyError as e:
    raise Exception(f"Undefined ENV variable {e.args[0]}")

# Change this to container_name:port inside docker container
HOSTNAME = "localhost:27017"


def main(input_filepath=INPUT_FILE_PATH):
    with open(input_filepath) as f:
        data = json.loads(f.read())

    init_adjacency_shelf(data)


def init_adjacency_shelf(aggregate_data):
    """
    Stores adjacency Map or distance 1 list with nodes metadata into shelve dB
    """
    adjacency_map = init_adjacency_map(aggregate_data)
    add_node_metadata(adjacency_map, aggregate_data)
    print(
        f"{datetime.datetime.now() - base_time}"
        f" Saving Adjacency map to MongoDB: {MONGO_DB_NAME}"
    )
    client = pymongo.MongoClient(f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}")
    db = client.get_database(name=MONGO_DB_NAME)
    node_collection = db.get_collection(name=MONGO_COLLECTION_NAME)
    count = 0
    curr_batch = []
    for k in adjacency_map:
        curr_batch.append({"_id": k, **adjacency_map[k]})
        count += 1
        if count % 1000 == 0:
            node_collection.insert_many(curr_batch)
            curr_batch.clear()
            print(f"{datetime.datetime.now()-base_time}", f"Added {count} nodes")

    # Adding elems which are left
    node_collection.insert_many(curr_batch)
    print(f"{datetime.datetime.now()-base_time}", f"Added {count} nodes")
    print(f"{datetime.datetime.now() - base_time}" f" Adjacency Map saved")


def init_adjacency_map(aggregate_data):
    """
    Converts the {'nodes': [], 'links': []} into Adjancency Map
    """
    print(f"{datetime.datetime.now() - base_time}" f" Creating adjacency map")
    links = aggregate_data["links"]
    adjacency_map = {}
    dist_1_out_key = f"{DIST}1"
    dist_1_in_key = f"{REV_DIST}1"

    for link in links:
        adjacency_map.setdefault(
            link["source"], {dist_1_out_key: [], dist_1_in_key: []}
        )[dist_1_out_key].append({"target": link["target"], "value": link["value"]})

        adjacency_map.setdefault(
            link["target"], {dist_1_out_key: [], dist_1_in_key: []}
        )[dist_1_in_key].append({"source": link["source"], "value": link["value"]})
    print(
        f"{datetime.datetime.now() - base_time}"
        f" Adjacency map created. Length: {len(adjacency_map)}"
    )
    return adjacency_map


def add_node_metadata(adjacency_map, aggregate_data):
    print(f"{datetime.datetime.now() - base_time}" f" Adding nodes metadata")
    dist_1_out_key = f"{DIST}1"
    dist_1_in_key = f"{REV_DIST}1"

    nodes = aggregate_data["nodes"]
    for node in nodes:
        curr_node = node
        if curr_node["cc_licenses"]:
            curr_node["cc_licenses"] = json.dumps(curr_node["cc_licenses"])

        adjacency_map.setdefault(node["id"], {dist_1_out_key: [], dist_1_in_key: []})[
            "metadata"
        ] = curr_node

    print(f"{datetime.datetime.now() - base_time}" f" Nodes metadata added.")


if __name__ == "__main__":
    main()
