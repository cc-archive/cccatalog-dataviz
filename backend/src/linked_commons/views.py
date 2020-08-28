from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import shelve
from linked_commons.models import Node
import random, string
import json
import pymongo

# Importing Mongo DB credentials
from config.settings import MONGO_DB_CRED

# Landing random graph maximum links and nodes
LANDING_GRAPH_META = {
    "links": 500,
    "nodes": 500,
}

# Mongo DB cred
USERNAME = MONGO_DB_CRED["USERNAME"]
PASSWORD = MONGO_DB_CRED["PASSWORD"]
DB_NAME = MONGO_DB_CRED["DB_NAME"]
COLLECTION_NAME = MONGO_DB_CRED["COLLECTION_NAME"]
HOSTNAME = MONGO_DB_CRED["HOSTNAME"]


def add_nodes_metadata(node_list):
    """Adds metadata to the nodes list"""
    nodes = []
    # Adding nodes metadata
    for node in node_list:
        curr_node = node["metadata"]
        if curr_node["cc_licenses"]:
            # Loading the json string as python dictionary
            curr_node["cc_licenses"] = json.loads(curr_node["cc_licenses"])

        nodes.append(curr_node)

    return nodes


def get_filtered_data(node_name, collection_instance):
    """
    Filters the Graph using node_name and returns the D1 list
    """
    nodes_id = {node_name}
    links = []
    node_list = collection_instance.find_one(node_name)

    # Adding outgoing D1 links
    for link in node_list["D1"]:
        links.append({**link, "source": node_name})
        nodes_id.add(link["target"])

    # Adding incoming D1 links
    for link in node_list["RD1"]:
        links.append({**link, "target": node_name})
        nodes_id.add(link["source"])

    # Finding the MongoDB collection for all the nodes inside nodes_id list
    node_list = collection_instance.find(
        {"_id": {"$in": list(nodes_id)}}, projection=["metadata"]
    )

    # Adding nodes metadata
    nodes = add_nodes_metadata(node_list)

    return {"links": links, "nodes": nodes}


def build_random_landing_graph(db, landing_graph_size=LANDING_GRAPH_META):
    """Builds a random graph of size landing_graph_size"""

    links = []
    # Retrieving the total number of documents/nodes in db
    total_nodes = db.count()
    # Calculating a random index
    index = random.randint(a=1, b=total_nodes - 1)
    # Finding the id of the root node
    root_node = db.find(projection=[]).limit(-1).skip(index).next()["_id"]
    # Making a copy of the root_node as base_node
    base_node = root_node
    # Set to store all nodes which are already taken into the current random graph
    nodes_id = set()
    nodes_id.add(root_node)

    while (
        len(nodes_id) < landing_graph_size["nodes"]
        and len(links) < landing_graph_size["links"]
    ):
        # Bucket to store the current batch of nodes which are getting added to graph
        temp_nodes_id = []
        node_list = db.find_one(root_node)
        # Adding links
        for link in node_list["D1"]:
            links.append({**link, "source": root_node})
            temp_nodes_id.append(link["target"])
            if len(nodes_id) + len(temp_nodes_id) > 500:
                break

        # Adding incoming D1 links
        for link in node_list["RD1"]:
            links.append({**link, "target": root_node})
            temp_nodes_id.append(link["source"])
            if len(nodes_id) + len(temp_nodes_id) > 500:
                break

        # Adding the nodes added in this iteration to the global set
        nodes_id.update(temp_nodes_id)
        if temp_nodes_id and len(nodes_id) < 500:
            # selecting a random node as root_node
            root_node = random.choice(temp_nodes_id)
        else:
            break

    # Finding the MongoDB collection for all the nodes inside nodes_id list
    node_list = db.find({"_id": {"$in": list(nodes_id)}}, projection=["metadata"])
    # Adding nodes metadata
    nodes = add_nodes_metadata(node_list)

    return {"root_node": base_node, "links": links, "nodes": nodes}


def serve_graph_data(request):
    """Returns the Graph In {'nodes':[], 'links':[]} format
    
    Returns a random graph if 'name' query param is None
    else returns the filtered graph with 'name' as root node
    """

    # Retrieving node name params
    node_name = request.GET.get("name")
    # connecting to mongodb with the credentials defined above
    client = pymongo.MongoClient(f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}")
    db = client.get_database(name=DB_NAME)
    collection_instance = db.get_collection(name=COLLECTION_NAME)

    # If node name is not provided sending whole file
    if node_name == None:
        # building a random graph
        data = build_random_landing_graph(collection_instance)
        client.close()
        return JsonResponse(data)
    else:
        # counting the number of documents with id as given node_name query
        node_count = collection_instance.count_documents({"_id": node_name})
        if node_count == 0:
            # returning error response
            return JsonResponse(
                {"error": True, "message": "node " + node_name + " doesn't exist"},
                json_dumps_params={"indent": 2},
            )

        # getting the filtered data with node_name as the central node
        data = get_filtered_data(node_name, collection_instance)
        client.close()
        return JsonResponse(data)

    client.close()
    # returning server error
    return JsonResponse({"error": True, "message": "Server Error"})


def serve_suggestions(request):
    """Returns a list of nodes matching the given query"""

    # Retrieving the query
    query = request.GET.get("q")
    if query:
        # connecting to mongodb with the credentials defined above
        client = pymongo.MongoClient(f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}")
        db = client.get_database(name=DB_NAME)
        collection_instance = db.get_collection(name=COLLECTION_NAME)

        # using regex to check for documents whose id matches with the given query
        # limiting the results to 8
        res = collection_instance.find(
            {"_id": {"$regex": query}}, return_key=True
        ).limit(8)

        # changing the format for frontend's consumption
        query_set = []
        for node in res:
            query_set.append({"id": node["_id"]})

        return JsonResponse({"error": False, "suggestions": query_set})
    else:
        # Sending error response if no query params are passed
        return JsonResponse({"error": True, "message": "No query params passed"})
