from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import shelve
from dataviz_api.models import Node
import random

MAX_DISTANCE = 1
OUTPUT_FILE_PATH = 'dataviz_api/data/graph_dB'

def get_filtered_data(db, node_name):
    """
    Filters the Graph using node_name and returns the D1 list
    """
    nodes_id = {node_name}
    links = []
    nodes = []
    node_list = db[node_name]

    # Adding links
    for link in node_list['D1']:
        links.append({**link, "source": node_name})
        nodes_id.add(link['target'])


    # Adding nodes metadata
    for node in nodes_id:
        nodes.append(db[node]['metadata'])


    return {'links': links, 'nodes': nodes}


def serve_graph_data(request):
    """Serves Graph Data"""
    # Retrieving node name params
    node_name = request.GET.get('name')
    print(node_name)

    # If node name is not provided sending whole file
    if(node_name == None):
        data = open(OUTPUT_FILE_PATH+'.json', 'rb')
        return FileResponse(data)

    with shelve.open(OUTPUT_FILE_PATH, writeback=False) as db:
        if( not node_name in db ):
            return JsonResponse({"error": True, "message": "node " + node_name + " doesn't exist"}, json_dumps_params={'indent': 4})

        data = get_filtered_data(db, node_name)
        db.close()
        return JsonResponse(data, json_dumps_params={'indent': 4})

    return JsonResponse({"error": "true", "message": "Server Error"})




def serve_suggestions(request):
    query = request.GET.get('q')
    if( query ):
        query_set = list(Node.objects.filter(provider_domain__icontains=query).values())
        if(len(query_set) > 8):
            random.shuffle(query_set)
            query_set = query_set[:8]
        return JsonResponse({"error": False, "suggestions":query_set }, json_dumps_params={'indent': 2})
    else:
        return JsonResponse({"error": True, "message": "No query params passed" })