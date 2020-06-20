from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import shelve
from dataviz_api.models import Node


MAX_DISTANCE = 10
OUTPUT_FILE_PATH = 'dataviz_api/data/fdg_output_file'

def get_filtered_data(db, node_name, distance):
    """Filters the Graph using node_name and distance

    Keyword arguments:
    db -- database instance
    node_name -- id of the root node
    distance -- maximum level upto which nodes should be considered
    """
    nodes = []
    links = []
    node_distance_list = db[node_name]
    # Iterating over all nodes which are at a distance of [1, distance] 
    for i in range(1, distance+1):
        # For all links at a distance of "i"
        for j in node_distance_list[str(i)]:
            # Appending to the links list
            links.append({**j, "source": node_name})
            # If "i" is at the last level then not adding distance one links
            if(i == distance):
                continue
            # For all target nodes adding their distance one links
            for k in db[j['target']]['1']:
                links.append({**k, "source": j['target'] })
    
    # Adding nodes metadata
    added_nodes_id = []
    # Adding root node metadata
    nodes.append(node_distance_list['metadata'])
    added_nodes_id.append(node_name)
    for i in links:
        # checking if target metadata is in nodes list
        if not i['target'] in added_nodes_id:
            nodes.append(db[i['target']]['metadata'])
            added_nodes_id.append(i['target'])
        # checking if source metadata is in nodes list
        if not i['source'] in added_nodes_id:
            nodes.append(db[i['source']]['metadata'])
            added_nodes_id.append(i['source'])

    return {'links': links, 'nodes': nodes}


def serve_graph_data(request):
    """Serves Graph Data"""
    # Retrieving node name params
    node_name = request.GET.get('name')

    # If node name is not provided sending whole file
    if(node_name == None):
        data = open(OUTPUT_FILE_PATH+'.json', 'rb')
        return FileResponse(data)

    with shelve.open(OUTPUT_FILE_PATH, writeback=False) as db:
        if( not node_name in db ):
            return JsonResponse({"error": True, "message": "node " + node_name + " doesn't exist"}, json_dumps_params={'indent': 4})

        # Retrieving distance params 
        distance = request.GET.get('distance')
        if(distance == None or int(distance) <=0):
            distance=MAX_DISTANCE
        else:
            distance = min(int(distance), MAX_DISTANCE)

        getData = get_filtered_data(db, node_name, distance)
        db.close()
        return JsonResponse(getData, json_dumps_params={'indent': 4})

    return JsonResponse({"error": "true", "message": "Server Error"})




def serve_suggestions(request):
    query = request.GET.get('q')
    if( query ):
        query_set = Node.objects.filter(index__icontains=query)
        query_set = query_set[:8]
        return JsonResponse({"error": False, "suggestions":list(query_set.values()) }, json_dumps_params={'indent': 4})
    else:
        return JsonResponse({"error": True, "message": "No query params passed" })