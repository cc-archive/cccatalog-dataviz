import json
import datetime
import pymongo
import os
from dotenv import load_dotenv
import sys

"""Run the build_db_script.py with the HOSTNAME of the MongoDB server 
Command: python build_db_script.py HOSTNAME
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")

# Loading env variables
load_dotenv(ENV_PATH)

# Path of JSON file which will be inserted to the database.
# A sample fdg_input_file.json can be found inside data-release/ directory.
INPUT_FILE_PATH = os.path.join(BASE_DIR, "fdg_input_file.json")

DIST = "D"  # Prefix in every node distance key [eg. D1, D2]
REV_DIST = "RD"  # Prefix in every node reverse distance key [eg. D1, D2]
# base time to log the time elapsed
base_time = datetime.datetime.now()

# Fetching Mongo DB Credentials
try:
    USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
    PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
    MONGO_DB_NAME = os.environ["MONGO_DB_NAME"]
    MONGO_COLLECTION_NAME = os.environ["MONGO_COLLECTION_NAME"]
except KeyError as e:
    raise Exception(f"Undefined ENV variable {e.args[0]}")

# fetching the hostname from command line arguments
HOST = sys.argv[1]
# Port of the server socket
PORT = "27017"
# Change this to the actual port of the mongoDB server
SOCKET = f"{HOST}:{PORT}"


def main(input_filepath=INPUT_FILE_PATH):
    # loading the input json file
    with open(input_filepath) as f:
        data = json.loads(f.read())

    # calling method to build modified adjacency list and update the mongodb
    init_adjacency_shelf(data)


def init_adjacency_shelf(aggregate_data):
    """
    Stores adjacency Map or distance 1 list with nodes metadata into mongo dB
    """
    # Building adjacency list
    adjacency_map = init_adjacency_map(aggregate_data)
    # Adding nodes metadata
    add_node_metadata(adjacency_map, aggregate_data)
    print(
        f"{datetime.datetime.now() - base_time}"
        f" Saving Adjacency map to MongoDB: {MONGO_DB_NAME}"
    )
    MONGO_URL = f"mongodb://{USERNAME}:{PASSWORD}@{SOCKET}"
    print(f"Connecting to {MONGO_URL}")
    # connecting to mongodb
    client = pymongo.MongoClient(f"{MONGO_URL}")
    db = client.get_database(name=MONGO_DB_NAME)
    node_collection = db.get_collection(name=MONGO_COLLECTION_NAME)
    count = 0
    # list to store the current batch
    curr_batch = []

    for k in adjacency_map:
        # appending the elems into current batch bucket
        curr_batch.append({"_id": k, **adjacency_map[k]})
        count += 1
        if count % 1000 == 0:
            # uploading the batch only at 1000, 2000, . . . (1000*n) th count
            # inserting into the mongodb collection in batch mode
            node_collection.insert_many(curr_batch)
            # clearing the current batch bucket
            curr_batch.clear()
            # logging timestamp
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
    # dictionary to store the adjacency list
    adjacency_map = {}
    # key in the node dictionary which store immediate outward edges info
    dist_1_out_key = f"{DIST}1"
    # key in the node dictionary which store immediate inward edges info
    dist_1_in_key = f"{REV_DIST}1"

    for link in links:
        # adding a outward link from source to target in source's object
        adjacency_map.setdefault(
            link["source"], {dist_1_out_key: [], dist_1_in_key: []}
        )[dist_1_out_key].append({"target": link["target"], "value": link["value"]})

        # adding a inward link from source to target in target's object
        adjacency_map.setdefault(
            link["target"], {dist_1_out_key: [], dist_1_in_key: []}
        )[dist_1_in_key].append({"source": link["source"], "value": link["value"]})

    # logging time
    print(
        f"{datetime.datetime.now() - base_time}"
        f" Adjacency map created. Length: {len(adjacency_map)}"
    )
    return adjacency_map


def add_node_metadata(adjacency_map, aggregate_data):
    """Adds metadata to the node in adjacency_map"""
    print(f"{datetime.datetime.now() - base_time}" f" Adding nodes metadata")
    # key in the node dictionary which store immediate outward edges info
    dist_1_out_key = f"{DIST}1"
    # key in the node dictionary which store immediate inward edges info
    dist_1_in_key = f"{REV_DIST}1"

    nodes = aggregate_data["nodes"]
    for node in nodes:
        curr_node = node
        if curr_node["cc_licenses"]:
            # converting the python dictionary object to json string
            # since in mongoDB keys cannot have dots '.' and some keys in cc_licenses contains dot '.'
            curr_node["cc_licenses"] = json.dumps(curr_node["cc_licenses"])

        # updating the metadata
        adjacency_map.setdefault(node["id"], {dist_1_out_key: [], dist_1_in_key: []})[
            "metadata"
        ] = curr_node

    # logging time
    print(f"{datetime.datetime.now() - base_time}" f" Nodes metadata added.")


if __name__ == "__main__":
    main()
