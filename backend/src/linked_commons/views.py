from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import shelve
from linked_commons.models import Node
import random, string
import json
import pymongo
from config.settings import MONGO_DB_CRED


LANDING_GRAPH_META = {
    "links": 500,
    "nodes": 500,
}


USERNAME = MONGO_DB_CRED['USERNAME']
PASSWORD = MONGO_DB_CRED['PASSWORD']
DB_NAME = MONGO_DB_CRED['DB_NAME']
COLLECTION_NAME = MONGO_DB_CRED['COLLECTION_NAME']
HOSTNAME = MONGO_DB_CRED['HOSTNAME']

def add_nodes_metadata(node_list):
    nodes = []
    # Adding nodes metadata
    for node in node_list:
        curr_node=node['metadata']
        if(curr_node['cc_licenses']):
            curr_node['cc_licenses']=json.loads(curr_node['cc_licenses'])

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
    for link in node_list['D1']:
        links.append({**link, "source": node_name})
        nodes_id.add(link['target'])
    
    # Adding incoming D1 links
    for link in node_list['RD1']:
        links.append({**link, "target": node_name})
        nodes_id.add(link['source'])

    node_list = collection_instance.find({"_id": {"$in": list(nodes_id)}}, projection=['metadata'])

    nodes = add_nodes_metadata(node_list)

    return {'links': links, 'nodes': nodes}


def build_random_landing_graph(db):
    links = []
    total_nodes = db.count()
    index = random.randint(a=1, b=total_nodes-1)
    root_node = db.find(projection=[]).limit(-1).skip(index).next()['_id']
    nodes_id = set()
    nodes_id.add(root_node)

    while len(nodes_id)<LANDING_GRAPH_META['nodes'] and len(links)<LANDING_GRAPH_META['links']:
        temp_nodes_id = []
        node_list=db.find_one(root_node)
        # Adding links
        for link in node_list['D1']:
            links.append({**link, "source": root_node})
            temp_nodes_id.append(link['target'])
            if(len(nodes_id)+len(temp_nodes_id)>500):
                break

        # Adding incoming D1 links
        for link in node_list['RD1']:
            links.append({**link, "target": root_node})
            temp_nodes_id.append(link['source'])
            if(len(nodes_id)+len(temp_nodes_id)>500):
                break

        nodes_id.update(temp_nodes_id)
        if temp_nodes_id and len(nodes_id)<500:
            # selecting a random node as root_node
            root_node = random.choice(temp_nodes_id)
        else:
            break
    
    node_list = db.find({"_id": {"$in": list(nodes_id)}}, projection=['metadata'])
    nodes = add_nodes_metadata(node_list)

    return {'links': links, 'nodes': nodes}


def serve_graph_data(request):
    """Serves Graph Data"""
    # Retrieving node name params
    node_name = request.GET.get('name')
    
    client = pymongo.MongoClient(f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}")
    db = client.get_database(name=DB_NAME)
    collection_instance = db.get_collection(name=COLLECTION_NAME)
    # If node name is not provided sending whole file
    if(node_name == None):
        data = build_random_landing_graph(collection_instance)
        client.close()
        return JsonResponse(data)
    else:
        node_count=collection_instance.count_documents({'_id':node_name})
        if( node_count==0 ):
            return JsonResponse({"error": True, "message": "node " + node_name + " doesn't exist"}, json_dumps_params={'indent': 2})

        data = get_filtered_data(node_name, collection_instance)
        client.close()
        return JsonResponse(data)

    client.close()
    return JsonResponse({"error": "true", "message": "Server Error"})




def serve_suggestions(request):
    query = request.GET.get('q')
    if( query ):
        client = pymongo.MongoClient(f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}")
        db = client.get_database(name=DB_NAME)
        collection_instance = db.get_collection(name=COLLECTION_NAME)
        res = collection_instance.find({'_id':{'$regex':query}}, return_key=True).limit(8)
        query_set = []
        for node in res:
            query_set.append({'id': node['_id']})
        
        return JsonResponse({"error": False, "suggestions":query_set })
    else:
        return JsonResponse({"error": True, "message": "No query params passed" })