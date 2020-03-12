// Queue Data Structure (Use for BFS traversal with first in first out (FIFO) rule)
class Queue{
  //Initialize a queue
  constructor(){
    this.items = [];
  }
  //Push element in the queue
  enqueue(element){
    this.items.push(element);
  }
  //Remove element from the queue
  dequeue(){
    if(this.isEmpty())return -1;
    return this.items.shift();
  }
  //Get the front element from the queue (FIFO rule)
  front(){
    if(this.isEmpty())return -1;
    return this.items[0];
  }
  //Check if queue is empty or not.
  isEmpty(){
    return this.items.length==0;
  }
}

// Graph Data Structure
class Graph { 

  //Initialize Adjacency List
	constructor(){
  		this.AdjList = new Map(); 
	} 

  //Initialize a vertex
	addVertex(v){
		this.AdjList.set(v,[]);
	}

  //Edges are undirected. (u->v and v->u)
	addEdge(u,v,weight){
		this.AdjList.get(u).push([v,weight]);
		this.AdjList.get(v).push([u,weight]);
   }
}

//Gobal Declarations (Which will going to use for further queries)
G = new Graph();

//Creating an array for autocomplete suggestions 
Id = new Array();

//Mapping ID with domain object. (For retrival of domain from domain ID)
nodesMap = new Map();

var noOfNodes = 0;
var noOfEdges = 0;

//Check if filter query is valid or not
function validId(id){
  for(var i=0;i<Id.length;i++){
    if(Id[i]==id)return true;
  }
  return false;
}

function plotGraph(){

  //This two array will provided to data object for d3-force graph
  var nodesList = new Array();
  var linksList = new Array();
  
  // User filter query depth and domain-id
  var depth = document.getElementById("depth").value;
  var id = document.getElementById("myFilterInput").value;
  
  if(depth!="Choose..."){
    //converting string value to int.
    depth = parseInt(depth);  
  }
  else{
    //If depth is not given then visit till leaf nodes.
    var MAXIMUM_DEPTH = 100;
    depth = MAXIMUM_DEPTH;
  }

  if(validId(id)){
      
    var links = new Array();
    var nodes = new Array();

    var iteratorObj = nodesMap.entries();

    var visited = new Map();
    var depthList = new Map();
    
    //Initialise depth list to -1 and visited to false.
    for(var i=0;i<noOfNodes;i++){
      var nodeId = iteratorObj.next().value[0];
      visited.set(nodeId,false);
      depthList.set(nodeId,-1);
    }

    //First visited the queried domain then push it into queue and assign depth to 0.
    visited.set(id,true);
    var q = new Queue();
    q.enqueue(nodesMap.get(id));
    depthList.set(id,0);      

    while(!q.isEmpty()){
      
      node = q.front();  

      // Checking the distance travel for each node if it goes beyond depth then terminate (BFS).
      if(depthList.get(node["id"])>depth)break;

      nodesList.push(node);
      q.dequeue();
      
      // Traverse all the neighbours of "node" which is currently visited.
      get_List = G.AdjList.get(node);
      for(i=0 ;i<get_List.length;i++){
        
        var neigh = get_List[i][0];
        var weight = get_List[i][1];

        // Checking if particular node is already visited or not.
        if(!visited.get(neigh["id"])){
          
          visited.set(neigh["id"],true);
          q.enqueue(neigh);
          depthList.set(neigh["id"],depthList.get(node["id"])+1);

          if(depthList.get(neigh["id"])<=depth){
            var dataMap = {
              source : node,
              target : neigh,
              value : weight
            };
            linksList.push(dataMap);
          }

        }
      }
    }
    
    // creating an object using BFS for plotting visual.
    var data = {
      nodes : nodesList,
      links : linksList
    }

    // Data is provided to d3force graph for further plotting.
    console.log(data);
    const MAX_FONT_SIZE = 6;//0.15;
    const ending = '...';
    const MIN_FONT_SIZE = 0.08;

    window.devicePixelRatio = 1; // use standard resolution in retina displays
    //Start by loading nodes and links from a file

    let hoverLink = null;
    let hoverNode = null;
    highlightNodes = new Map();
    linksPerDomains = indexBy(data.links, ['source', 'target']);//

    const elem = document.getElementById('graph');

    const Graph = ForceGraph()
    (elem)
    .backgroundColor('#07263b')
    .graphData(data)
    // links
    .onLinkHover(link => hoverLink = link)
    .linkWidth(link => (hoverLink === link || highlightNodes.has(link.source.id) || highlightNodes.has(link.target.id) ) ? 2 : 1)
    .linkColor(link => (link === hoverLink || highlightNodes.has(link.source.id) || highlightNodes.has(link.target.id)) ? 'white' : 'rgb(155, 216, 240, 0.25)')
    .nodeCanvasObjectMode(() => 'replace')
    .zoom(0.05)

    //draw source and targets on the links
    .linkCanvasObjectMode(() => 'after')
    .linkCanvasObject((link, ctx) => {
      const MAX_FONT_SIZE = 6;
      const LABEL_NODE_MARGIN = Graph.nodeRelSize() * 1.5;
      const start = link.source;
      const end = link.target;
      // ignore unbound links
      if (typeof start !== 'object' || typeof end !== 'object') return;
      // calculate label positioning
      const textPos = Object.assign(...['x', 'y'].map(c => ({
        [c]: start[c] + (end[c] - start[c]) / 2 // calc middle point
      })));
      const relLink = { x: end.x - start.x, y: end.y - start.y };
      const maxTextLength = Math.sqrt(Math.pow(relLink.x, 2) + Math.pow(relLink.y, 2)) - LABEL_NODE_MARGIN * 2;
      let textAngle = Math.atan2(relLink.y, relLink.x);
      // maintain label vertical orientation for legibility
      if (textAngle > Math.PI / 2) textAngle = -(Math.PI - textAngle);
      if (textAngle < -Math.PI / 2) textAngle = -(-Math.PI - textAngle);
      const label = `${link.source.id} > ${link.target.id}`;
      // estimate fontSize to fit in link length
      ctx.font = '2px Sans-Serif';
      const fontSize = Math.min(MAX_FONT_SIZE, maxTextLength / ctx.measureText(label).width);
      ctx.font = `${fontSize}px Sans-Serif`;
      const textWidth = ctx.measureText(label).width;
      const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding
      // draw text label (with background rect)
      ctx.save();
      ctx.translate(textPos.x, textPos.y);
      ctx.rotate(textAngle);
      ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
      ctx.fillRect(- bckgDimensions[0] / 2, - bckgDimensions[1] / 2, ...bckgDimensions);
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = 'lightgrey'; // '#C8C8C8'; // '#E8E8E8'; // 'lightgrey';
      ctx.fillText(label, 0, 0);
      ctx.restore();
    })

     //draw nodes
    .onNodeClick(node => {
      Graph.centerAt(node.x, node.y, 1000);
      Graph.zoom(5, 2000);
      drawPieChart(node);
    })

    .nodeLabel(node => `${node.id}`)
    .nodeCanvasObject((node, ctx, globalScale) => {
      ctx.beginPath();
      var node_size = `${node.node_size}`;
      var radius = node_size/2;
      ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI, false);
      ctx.lineWidth = 0.5;//Math.min(globalScale*0.05,2);
      ctx.fillStyle = '#32B2B0'; //fill color
      ctx.strokeStyle = '#07263b'; //border color
      ctx.fill();
      ctx.stroke();

      //add text to nodes
      var label = node.id;
      // start with a large font size
      /*var fontsize = Math.min(MAX_FONT_SIZE,globalScale*1.6);
      ctx.font = "bold "+`${fontsize}em Sans-Serif`;
      */
      ctx.font = `bold 1px Sans-Serif`; //First set the font size to be 1
      let fontsize = Math.floor(node_size / ctx.measureText(label).width +0.5);  //Check the no. of times the font size should be enlarged compared to 1px
      if(fontsize <=1){  //If the whole text can't be displayed
        label = label.slice(0,5)
        label = label+ending;
        fontsize = Math.floor(node_size / ctx.measureText(label).width +0.5);
      }
      //Wrapping up the text inside the node with some logic based on node size and text length
        if(fontsize>=5 && node.node_size>70 && node.id.length <=5)
          fontsize -= 5;
        else if(fontsize>=3 && node.node_size>70)
          fontsize -= 3;
        else
          fontsize--;
      ctx.font = fontsize>1?"bold "+`${fontsize}px Sans-Serif`:"bold 0.08em Sans-Serif";
      //set bounds for the labels
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#D3D3D3'; // '#279e9c'; //text color cream: #f2ebcf gray: #e9eaea
      ctx.fillText(label, node.x, node.y);

    })
    //highlighting neighbors
    .onNodeHover( node => {
        hoverNode = node;
        elem.style.cursor = node ? 'pointer' : null;

        highlightNodes.clear();
        if (node) {
          otherGraph = traverseHighlight(node.id);
        }
      });

      Graph.d3Force('charge', null)
      Graph.d3Force('charge', d3.forceManyBody().strength(-120));
      Graph.d3Force('collide',d3.forceCollide(Graph.nodeRelSize()))
  }
  else{
      alert("Select valid domain !");
  }
}