from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import shelve
from dataviz_api.models import Node
import random, string

# shelve dB path
OUTPUT_FILE_PATH = 'dataviz_api/data/graph_dB'
# Landing graph path
LANDING_GRAPH_FILE_PATH = 'dataviz_api/data/landing_graph.json'

LANDING_GRAPH_META = {
    "links": 500,
    "nodes": 500,
}

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


def build_random_landing_graph(db):
    nodes = []
    links = []
    count = Node.objects.count()
    index = random.randint(a=1, b=count-7)
    root_node = Node.objects.all()[index].id
    nodes_id = set()
    nodes_id.add(root_node)

    while len(nodes_id)<500 and len(links)<500:
        temp_nodes_id = []
        # Adding links
        for link in db[root_node]['D1']:
            links.append({**link, "source": root_node})
            temp_nodes_id.append(link['target'])

        nodes_id.update(temp_nodes_id)
        if temp_nodes_id:
            # selecting a random node as root_node
            root_node = random.choice(temp_nodes_id)
        else:
            break
    
    # Adding Meta Data
    for node in nodes_id:
        nodes.append(db[node]['metadata'])

    return {'links': links, 'nodes': nodes}


def serve_graph_data(request):
    """Serves Graph Data"""
    # Retrieving node name params
    node_name = request.GET.get('name')

    with shelve.open(OUTPUT_FILE_PATH, writeback=False, flag='r') as db:
    # If node name is not provided sending whole file
        if(node_name == None):
            data = build_random_landing_graph(db)
            return JsonResponse(data)
        else:
            if( not node_name in db ):
                return JsonResponse({"error": True, "message": "node " + node_name + " doesn't exist"}, json_dumps_params={'indent': 2})

            data = get_filtered_data(db, node_name)
            db.close()
            return JsonResponse(data)

    return JsonResponse({"error": "true", "message": "Server Error"})




def serve_suggestions(request):
    query = request.GET.get('q')
    if( query ):
        query_set = list(Node.objects.filter(index__icontains=query).values())
        query_set = query_set[:8]
        return JsonResponse({"error": False, "suggestions":query_set })
    else:
        return JsonResponse({"error": True, "message": "No query params passed" })