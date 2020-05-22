from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import shelve

MAX_DISTANCE = 10
OUTPUT_FILE_NAME = 'fdg_output_file'


def getFilteredData(db, nodeName, distance):
    nodeDistanceList = db[nodeName]
    nodes = []
    links = []
    print(nodeDistanceList)
    for i in range(1, distance+1):
        # link = nodeDistanceList[str(i)]
        # link['source'] = nodeName
        # links +=link
        for j in nodeDistanceList[str(i)]:
            links.append({**j, "source": nodeName})
            for k in db[j['target']]['1']:
                links.append({**k, "source": j['target'] })

    nodes.append(nodeDistanceList['metadata'])
    for i in links:
        if not i in nodes:
            nodes.append(db[i['target']]['metadata'])

    return {'links': links, 'nodes': nodes}


'''
Serves Graph Data
'''
def serve_graph_data(request):
    # Retrieving node name 
    nodeName = request.GET.get('name')
    # If node name is not provided sending whole file
    if(nodeName == None):
        data = open('api/data/'+OUTPUT_FILE_NAME+'.json', 'rb')
        return FileResponse(data)

    with shelve.open('api/data/'+OUTPUT_FILE_NAME, writeback=False) as db:
        if( not nodeName in db ):
            return JsonResponse({"error": True, "message": "node " + nodeName + " doesn't exist"}, json_dumps_params={'indent': 4})

        distance = request.GET.get('distance')
        if(distance == None or int(distance) <=0):
            distance=MAX_DISTANCE
        else:
            distance = min(int(distance), MAX_DISTANCE)

        getData = getFilteredData(db, nodeName, distance)
        db.close()
        return JsonResponse(getData, json_dumps_params={'indent': 4})

    return JsonResponse({"error": "true", "message": "Server Error"})