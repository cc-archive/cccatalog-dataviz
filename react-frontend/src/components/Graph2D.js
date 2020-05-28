import React from 'react';
import { forceManyBody, forceCollide } from 'd3-force';
import { ForceGraph2D } from 'react-force-graph';
import LicenseChart from './LicenseChart';
import ZoomToolkit from './ZoomToolkit';
import SearchFilterBox from './SearchFilterBox';

// source data
const ENDPOINT = '../data/fdg_input_file.json';

const darkThemeData = {
    'linkColor': 'rgba(196, 196, 196, 0.3)',
    'hoverLinkColor': '#fff',
    'graphCanvasColor': 'black',
    'nodeFillColor': '#EFBE00',
    'nodeTextColor': '#000'
}

const lightThemeData = {
    'linkColor': '#D8D8D8',
    'hoverLinkColor': '#2f4f4f',
    'graphCanvasColor': 'white',
    'nodeFillColor': '#ED592F',
    'nodeTextColor': '#FFF'
}

class Graph2D extends React.Component {
    state = {
        // stores the fetched graph data
        graphData: null,
        // state of page loader
        loading: true,
        ending: '...',
        // value of node size
        nodeRelSize: 10,
        hoverLink: null,
        // contains all node
        highlightNodes: null,
        linksPerDomains: null,
        // boolean value to handle PieChart Rendering
        licenseChartState: false,
        link: null,
        // current clicked node
        node: null,
        // value of current hovered link format: [source_dest]
        linkName: 'null_null',
        // set the inital value of zoom
        currentZoomLevel: 1, // storing the current zoom level
        // !TODO: to be used for re-setting the state
        originalGraphData: null,
        isDarkMode: true,
    }

    constructor(props) {
        super(props);
        this.graphRef = React.createRef();
        this.state.highlightNodes = new Map();
    }

    componentDidMount() {
        // fetching value in data-theme key from localstorage
        let theme = window.localStorage.getItem('data-theme');
        if(!theme){
            // data-theme key is not present in local storage
            window.localStorage.setItem('data-theme', 'dark'); // dark || light
        }
        // setting data-theme attribute
        document.documentElement.setAttribute('data-theme', theme);
        // updating darkMode state 
        this.setState({
            isDarkMode: theme === 'dark'? true : false,
        });
        // Fetching the data from source endpoint
        fetch(ENDPOINT)
            .then((res) => res.json())
            .then(res => {
                this.setState({
                    originalGraphData: res,
                })
                this.simulateForceGraph(res);
            });
    }

    render() {
        return (
            <React.Fragment>
                {/* <SearchFilterBox handleSubmit={this.handleFilterSubmit} /> */}
                <DarkModeSwitch toggleThemeState= {this.toggleThemeHandler}/>
                <div className='content-wrapper'>

                    {this.state.licenseChartState ? <LicenseChart node={this.state.node} handler={this.toggleLicenseChartState} /> : null}

                    {this.state.loading ? <h1 style={{ textAlign: "center" }}>loading...</h1> :
                        <div className='graph-wrapper'>
                            
                            <div id="graph-canvas">
                                <ForceGraph2D
                                    ref={this.graphRef}
                                    graphData={this.state.graphData}
                                    onLinkHover={this.handleLinkHover}
                                    linkWidth={link => (this.state.hoverLink === link || this.state.highlightNodes.has(link.source.id) || this.state.highlightNodes.has(link.target.id)) ? 2 : 1}
                                    linkColor={(link) => (link === this.state.hoverLink || this.state.highlightNodes.has(link.source.id) || this.state.highlightNodes.has(link.target.id)) ? (this.state.isDarkMode ? darkThemeData.hoverLinkColor : lightThemeData.hoverLinkColor) : (this.state.isDarkMode ? darkThemeData.linkColor : lightThemeData.linkColor)}
                                    nodeCanvasObjectMode={() => 'replace'}
                                    linkCanvasObjectMode={() => 'after'}
                                    backgroundColor={this.state.isDarkMode ? darkThemeData.graphCanvasColor : lightThemeData.graphCanvasColor}
                                    linkCanvasObject={this.handleLinkCanvasObject}
                                    onNodeClick={this.handleOnNodeClick}
                                    nodeLabel={(node) => `${node.id}`}
                                    nodeCanvasObject={this.handleNodeCanvasObject}
                                    linkDirectionalArrowLength={5}
                                    linkDirectionalArrowRelPos={0.99}
                                    onNodeHover={this.handleOnNodeHover}
                                    onZoomEnd={this.handleZoomEnd}
                                    enableNodeDrag={true}
                                    currentZoomLevel={this.currentZoomLevel}
                                />
                                <ZoomToolkit
                                    handleZoomIn={this.handleZoomIn}
                                    handleZoomOut={this.handleZoomOut}
                                />
                            </div>
                        </div>
                    }
                </div>
            </React.Fragment>
        )
    }

    toggleThemeHandler = () => {
        let newTheme = this.state.isDarkMode ? 'light' : 'dark';
        this.setState({
            isDarkMode : newTheme === 'dark' ? true : false,
        })
        window.localStorage.setItem('data-theme', newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);
    }

    // Update the data and simulates the graph rendering 
    simulateForceGraph = (res) => {
        let obj = {};
        res.links.forEach((e) => {
            if (obj[e.source] === undefined) {
                obj[e.source] = {}
            }
            obj[e.source][e.target] = [{ value: e.value }]
        })
        this.setState({
            graphData: res,
            linksPerDomains: obj
        })
        this.setState({
            loading: false
        })
        this.graphRef.current.d3Force('charge', null)
        this.graphRef.current.d3Force('charge', forceManyBody().strength(-120))
        this.graphRef.current.d3Force('collide', forceCollide(this.state.nodeRelSize))
    }

    searchNodesInDepth(adjacencyList, node, visited, maxLevel, currLevel, links) {
        visited.set(node, true);
        let neighbours = adjacencyList[node];
        if (currLevel === maxLevel || !neighbours) {
            // if current level is equal to max level stoping the traversal
            return;
        }
        Object.entries(neighbours).forEach(neighbour => {
            if (!visited.has(neighbour[0])) {
                // not yet visited
                links.push({ source: node, target: neighbour[0], value: neighbour[1][0]['value'] })
                // calling searchNodesInDepth again and incrementing the level by 1
                this.searchNodesInDepth(adjacencyList, neighbour[0], visited, maxLevel, currLevel + 1, links);
            }
        })
    }

    // Handles Filtering by node name and distance
    handleFilterSubmit = ({ name: startNode, distance }) => {
        startNode = startNode.toLowerCase();
        if (this.state.linksPerDomains[startNode]) {
            distance = distance.toLowerCase()
            let visited = new Map();
            let links = [];
            distance = parseInt(distance);
            this.searchNodesInDepth(this.state.linksPerDomains, startNode, visited, distance, 0, links);
            let nodes = [];
            let masterNodes = this.state.graphData['nodes'];
            let n = masterNodes.length;
            visited.clear();
            links.forEach((link) => {
                for (let i = 0; i < n; i++) {
                    if ((!visited.has(link['source']) && masterNodes[i]['id'] === link['source'])) {
                        nodes.push({ ...masterNodes[i], node_size: masterNodes[i]['node_size'] });
                        visited.set(link['source'], true);
                    }
                    if (!visited.has(link['target']) && masterNodes[i]['id'] === link['target']) {
                        nodes.push({ ...masterNodes[i], node_size: masterNodes[i]['node_size'] });
                        visited.set(link['target'], true);
                    }
                }
            });
            this.simulateForceGraph({ links, nodes });
            // A nice animated zooming effect into the filtered graph
            setTimeout(() => {
                this.graphRef.current.zoomToFit(1000, 10)
            }, 500)
        } else {
            // Invalid
            alert('Invalid Node Name');
        }
    }

    handleZoomOut = () => {
        // Decrementing zoom level by zoom step
        this.graphRef.current.zoom(this.state.currentZoomLevel - this.getZoomStep(this.state.currentZoomLevel), 250);
    }

    handleZoomIn = () => {
        // Incrementing zoom level by zoom step
        this.graphRef.current.zoom(this.state.currentZoomLevel + this.getZoomStep(this.state.currentZoomLevel), 250);
    }


    // helper function to calculate zoom step
    getZoomStep(currentZoomLevel) {
        if (currentZoomLevel > 3) {
            return 1.2;
        } else {
            return currentZoomLevel / 4;
        }
    }

    // Function to remove the modal window
    toggleLicenseChartState = () => {
        this.setState({
            licenseChartState: !this.state.licenseChartState,
        })
        document.body.classList.remove('modal-active');
    }

    handleOnNodeClick = (node) => {
        if(node){
            this.graphRef.current.centerAt(node.x, node.y, 1000);
            this.graphRef.current.zoom(5, 2000);
            setTimeout(() => {
                this.setState({
                    licenseChartState: true,
                    node: node
                })
                document.body.classList.add('modal-active');
            }, 500);
        }
            
    }

    handleOnNodeHover = node => {
        // setting cursor style to pointer
        document.body.style.cursor = node ? 'pointer' : null;
        this.state.highlightNodes.clear();
        if (node) {
            this.traverseHighlight(node.id);
        }
    }


    traverseHighlight(domain, degree = -1) {
        if (!domain) return;
        if (this.state.highlightNodes.has(domain)) { // already been here
            this.state.highlightNodes.set(domain, Math.min(degree, this.state.highlightNodes.get(domain))); // keep closest degree
            return;
        }
        this.state.highlightNodes.set(domain, degree);
        Object.entries(this.state.linksPerDomains[domain] || {})
            .forEach(([targetDomain]) => this.traverseHighlight(targetDomain, degree + 1));

    }

    // callback function to handle on zoom end
    handleZoomEnd = (e) => {
        // updating current zoom level
        this.setState({
            currentZoomLevel: e.k
        })
    }

    // function to handle whenever any link or edge is hovered 
    handleLinkHover = (link) => {
        if (link) {
            // updating linkName state
            this.setState({
                linkName: `${link.source.id}_${link.target.id}`
            })
            this.setState({ hoverLink: link })
        } else {
            this.setState({
                hoverLink: null,
                linkName: `null_null`
            })
        }
    }

    // configuring render style for nodes of the graph
    handleNodeCanvasObject = (node, ctx, globalScale) => {
        ctx.beginPath();
        var node_size = `${node.node_size}`;
        var radius = node_size / 2;
        ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI, false);
        ctx.lineWidth = 0.5;//Math.min(globalScale*0.05,2);
        ctx.fillStyle = this.state.isDarkMode ? darkThemeData.nodeFillColor : lightThemeData.nodeFillColor; //fill color
        // ctx.strokeStyle = '#07263b'; //border color
        ctx.fill();
        ctx.stroke();

        //add text to nodes
        var label = node.id;
        // start with a large font size
        /*var fontsize = Math.min(MAX_FONT_SIZE,globalScale*1.6);
        ctx.font = "bold "+`${fontsize}em Sans-Serif`;
        */
        ctx.font = `bold 1px Sans-Serif`; //First set the font size to be 1
        let fontsize = Math.floor(node_size / ctx.measureText(label).width + 0.5);  //Check the no. of times the font size should be enlarged compared to 1px
        if (fontsize <= 1) {  //If the whole text can't be displayed
            label = label.slice(0, 5)
            label = label + this.state.ending;
            fontsize = Math.floor(node_size / ctx.measureText(label).width + 0.5);
        }
        //Wrapping up the text inside the node with some logic based on node size and text length
        if (fontsize >= 5 && node.node_size > 70 && node.id.length <= 5)
            fontsize -= 5;
        else if (fontsize >= 3 && node.node_size > 70)
            fontsize -= 3;
        else
            fontsize--;
        ctx.font = fontsize > 1 ? `bold ${fontsize}px Sans-Serif` : "bold 0.08em Sans-Serif";
        //set bounds for the labels
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = this.state.isDarkMode ? darkThemeData.nodeTextColor : lightThemeData.nodeTextColor; // '#279e9c'; //text color cream: #f2ebcf gray: #e9eaea
        ctx.fillText(label, node.x, node.y);
    }

    // configuring render style for links or edges of the graph
    handleLinkCanvasObject = (link, ctx) => {
        if (this.state.currentZoomLevel < 2) {
            return;
        }
        const MAX_FONT_SIZE = 6;
        const LABEL_NODE_MARGIN = this.state.nodeRelSize * 1.5;
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
    }
}


export default Graph2D;



function DarkModeSwitch({toggleThemeState}) {
    return (
        <div className='darkmodeswitch' onClick = {toggleThemeState}>
            Explore CC
        </div>
    )
}