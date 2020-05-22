from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import shelve

MAX_DISTANCE = 10
OUTPUT_FILE_NAME = 'fdg_output_file'

'''
Filters the Graph using nodeName and distance
'''
def getFilteredData(db, nodeName, distance):
    nodes = []
    links = []
    nodeDistanceList = db[nodeName]
    # Iterating over all nodes which are at a distance of [1, distance] 
    for i in range(1, distance+1):
        # For all links at a distance of "i"
        for j in nodeDistanceList[str(i)]:
            # Appending to the links list
            links.append({**j, "source": nodeName})
            # If "i" is at the last level then not adding distance one links
            if(i == distance):
                continue
            # For all target nodes adding their distance one links
            for k in db[j['target']]['1']:
                links.append({**k, "source": j['target'] })
    
    # Adding nodes metadata
    nodes.append(nodeDistanceList['metadata'])
    for i in links:
        if not i in nodes:
            nodes.append(db[i['target']]['metadata'])

    return {'links': links, 'nodes': nodes}


'''
Serves Graph Data
'''
def serve_graph_data(request):
    # Retrieving node name params
    nodeName = request.GET.get('name')

    # If node name is not provided sending whole file
    if(nodeName == None):
        data = open('api/data/'+OUTPUT_FILE_NAME+'.json', 'rb')
        return FileResponse(data)

    with shelve.open('api/data/'+OUTPUT_FILE_NAME, writeback=False) as db:
        if( not nodeName in db ):
            return JsonResponse({"error": True, "message": "node " + nodeName + " doesn't exist"}, json_dumps_params={'indent': 4})

        # Retrieving distance params 
        distance = request.GET.get('distance')
        if(distance == None or int(distance) <=0):
            distance=MAX_DISTANCE
        else:
            distance = min(int(distance), MAX_DISTANCE)

        getData = getFilteredData(db, nodeName, distance)
        db.close()
        return JsonResponse(getData, json_dumps_params={'indent': 4})

    return JsonResponse({"error": "true", "message": "Server Error"})