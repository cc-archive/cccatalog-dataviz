import React from 'react';
import { forceManyBody, forceCollide } from 'd3-force';
import { ForceGraph2D } from 'react-force-graph';
import LicenseChart from './LicenseChart';
import ZoomToolkit from './ZoomToolkit';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { ReactComponent as InfoIcon } from '../assets/icons/info.svg';
// Importing the Loader
import { ReactComponent as Spinner } from '../assets/icons/spinner.svg';

// source data
const SERVER_BASE_ENDPOINT = process.env.NODE_ENV === 'production' ? process.env.REACT_APP_SERVER_BASE_ENDPOINT_PROD : process.env.REACT_APP_SERVER_BASE_ENDPOINT_DEV;

// Breakpoint at which the mobile design will we used
const MOBILE_DESIGN_BREAKPOINT = 450;

// dark theme metadata
const darkThemeData = {
    'linkColor': 'rgba(196, 196, 196, 0.3)',
    'hoverLinkColor': '#fff',
    'graphCanvasColor': 'black',
    'nodeFillColor': '#EFBE00',
    'nodeTextColor': '#000'
}

// light theme metadata
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
        isDarkMode: true,
        // Show processing 
        processing: false,
        // root node name
        rootNode: "",
        // viewport layout
        width: 0,
        height: 0,
    }

    constructor() {
        super();
        this.graphRef = React.createRef();
        this.state.highlightNodes = new Map();
    }

    componentDidMount() {
        // loading the dimensions
        this.updateDimensions();
        // Adding Event listener for resize event to update the viewport dimensions
        window.addEventListener('resize', this.updateDimensions);

        // fetching value in data-theme key from localstorage
        let theme = window.localStorage.getItem('data-theme');
        if (!theme) {
            // data-theme key is not present in local storage
            window.localStorage.setItem('data-theme', 'light'); // dark || light
            theme = 'light';
        }
        // setting data-theme attribute
        document.documentElement.setAttribute('data-theme', theme);
        // updating darkMode state 
        this.setState({
            isDarkMode: theme === 'dark' ? true : false,
        });
        // Fetching the data from source endpoint
        fetch(`${SERVER_BASE_ENDPOINT}/graph-data`)
            .then((res) => res.json())
            .then(res => {
                this.setState({
                    "rootNode": res['root_node']
                })
                this.simulateForceGraph(res);
            });
    }

    // updating the canvas dimensions
    updateDimensions = () => {
        this.setState({
            'width': window.innerWidth,
            'height': window.innerHeight,
        })
        // setting --vh and --vw variables of css
        let vh = window.innerHeight * 0.01;
        let vw = window.innerWidth * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
        document.documentElement.style.setProperty('--vw', `${vw}px`);
    }

    render() {
        return (
            <React.Fragment>
                <Navbar
                    isDarkMode={this.state.isDarkMode}
                    isLoading={this.state.loading}
                    toggleThemeHandler={this.toggleThemeHandler} />
                <div className='content-wrapper'>
                    {this.state.licenseChartState ? <LicenseChart node={this.state.node} handler={this.toggleLicenseChartState} /> : null}

                    {this.state.loading ? <div className='loader'> <Spinner /></div> :
                        <div className='graph-wrapper'>

                            <Sidebar
                                showActionInitialState={this.state.width >= MOBILE_DESIGN_BREAKPOINT}
                                isDarkMode={this.state.isDarkMode}
                                handleSubmit={this.handleFilterSubmit}
                                processing={this.state.processing}
                                SERVER_BASE_URL={SERVER_BASE_ENDPOINT}
                            />
                            <div id="graph-canvas">
                                <ForceGraph2D
                                    ref={this.graphRef}
                                    graphData={this.state.graphData}
                                    onLinkHover={this.handleLinkHover}
                                    linkWidth={link => (this.state.hoverLink === link || this.state.highlightNodes.has(link.source.id) || this.state.highlightNodes.has(link.target.id)) ? 2 : 1}
                                    linkColor={(link) => {
                                        if (
                                            link === this.state.hoverLink ||
                                            this.state.highlightNodes.has(link.source.id) ||
                                            this.state.highlightNodes.has(link.target.id)) {
                                            return (this.state.isDarkMode ? darkThemeData.hoverLinkColor : lightThemeData.hoverLinkColor)
                                        } else {
                                            // node not highlighted
                                            if (this.state.isDarkMode) {
                                                if (link.source.id === this.state.rootNode) {
                                                    return '#FF0000';
                                                } else if (link.target.id === this.state.rootNode) {
                                                    return '#40E0D0';
                                                } else {
                                                    return darkThemeData.linkColor;
                                                }
                                            } else {
                                                if (link.source.id === this.state.rootNode) {
                                                    return '#FF0000';
                                                } else if (link.target.id === this.state.rootNode) {
                                                    return '#40E0D0';
                                                } else {
                                                    return lightThemeData.linkColor;
                                                }
                                            }
                                        }
                                    }
                                    }
                                    nodeCanvasObjectMode={() => 'replace'}
                                    linkCanvasObjectMode={() => 'after'}
                                    backgroundColor={this.state.isDarkMode ? darkThemeData.graphCanvasColor : lightThemeData.graphCanvasColor}
                                    linkCanvasObject={this.handleLinkCanvasObject}
                                    onNodeDragEnd={node => {
                                        node.fx = node.x;
                                        node.fy = node.y;
                                    }}
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
                                    resetZoom={this.resetZoom}
                                />
                            </div>
                            {this.state.width <= MOBILE_DESIGN_BREAKPOINT ?
                                <MobileFooter /> : <div />
                            }
                        </div>
                    }
                </div>
            </React.Fragment>
        )
    }

    // helper function to toggle the current theme and update the data-theme attribute
    toggleThemeHandler = () => {
        let newTheme = this.state.isDarkMode ? 'light' : 'dark';
        this.setState({
            isDarkMode: newTheme === 'dark' ? true : false,
        })
        window.localStorage.setItem('data-theme', newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);
    }

    // Reset the current zoom and fit the graph to viewport's canvas
    resetZoom = () => {
        // animating the transition for 1 sec
        this.graphRef.current.zoomToFit(1000);
    }

    // Update the data and simulates the graph rendering 
    simulateForceGraph = (res) => {
        let obj = {};
        // building the linksPerDomain which is a 
        // lightweight adjacency list representation of the graph
        res.links.forEach((e) => {
            if (obj[e.source] === undefined) {
                obj[e.source] = {}
            }
            obj[e.source][e.target] = [{ value: e.value }]
        })
        // updating the state
        this.setState({
            graphData: res,
            linksPerDomains: obj
        })
        // setting the loading as false
        this.setState({
            loading: false
        })

        // checking if the graphRef is not null
        if (this.graphRef.current) {
            this.graphRef.current.d3Force('charge', null)
            this.graphRef.current.d3Force('charge', forceManyBody().strength(-120))
            // performing collision among the nodes if the number of nodes are <300
            // limiting the usage since it's resource intensive and causes throttling
            if (this.state.graphData['nodes'].length < 300)
                this.graphRef.current.d3Force('collide', forceCollide(this.state.nodeRelSize))
        }
    }


    // handles server side filtering
    // fetches the data and updates the graph
    fetchFilteredData = async (nodeName) => {
        // converting and removing the spaces from start and end from the nodeName
        nodeName = nodeName.trimEnd().trimStart().toLowerCase();
        // setting the processing state as true
        this.setState({
            processing: true,
        })
        try {
            let rootNode = nodeName;
            if (rootNode === "") {
                alert(`Please enter a valid node name`)
                // raising error
                throw Error("Please enter a valid node name")
            }
            let res = await fetch(`${SERVER_BASE_ENDPOINT}/graph-data?name=${nodeName}`);
            let jsonData = await res.json();

            if (jsonData['error']) {
                this.setState({
                    processing: false
                })
                alert(`Error Occurred: ${jsonData['message']}`)
            } else {
                // simulating the graph rendering
                this.simulateForceGraph(jsonData);
                // animating after 500 ms
                setTimeout(() => {
                    this.graphRef.current.zoomToFit(1000, 10)
                }, 500)

                // setting rootNode variable to differently colour incoming and outgoing links
                this.setState({
                    "rootNode": rootNode,
                })
            }
        } catch (err) {
            console.log(err);
        }
        this.setState({
            processing: false
        })
    }

    // Handles Filtering by node name
    handleFilterSubmit = (payload) => {
        this.fetchFilteredData(payload.name);
    }

    // wrapper function to zoom out of the graph canvas
    handleZoomOut = () => {
        // Decrementing zoom level by zoom step
        this.graphRef.current.zoom(this.state.currentZoomLevel - this.getZoomStep(this.state.currentZoomLevel), 250);
    }

    // wrapper function to zoom into the graph canvas
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

    // activates the modal with license information
    handleOnNodeClick = (node) => {
        if (node) {
            // zooming into the selected node
            this.graphRef.current.centerAt(node.x, node.y, 1000);
            this.graphRef.current.zoom(5, 2000);
            setTimeout(() => {
                // activating the license chart modal
                this.setState({
                    licenseChartState: true,
                    node: node
                })
                // adding modal-active class to body element
                document.body.classList.add('modal-active');
            }, 500);
        }

    }

    // traverses all links accessible from the {domain} and highlights them
    handleOnNodeHover = (node) => {
        // setting cursor style to pointer
        document.body.style.cursor = node ? 'pointer' : null;
        // clearing all previously highlighted links
        this.state.highlightNodes.clear();
        if (node) {
            // calling travereHighlight method to traverse all links accessible from the node
            this.traverseHighlight(node.id);
        }
    }


    // traverses all links accessible from the {domain} and highlights them
    traverseHighlight(domain, degree = -1) {
        if (!domain) return;
        if (this.state.highlightNodes.has(domain)) { // already been here
            this.state.highlightNodes.set(domain, Math.min(degree, this.state.highlightNodes.get(domain))); // keep closest degree
            return;
        }
        this.state.highlightNodes.set(domain, degree);
        // traversing all nodes which are immediate neighbours of the {domain}
        Object.entries(this.state.linksPerDomains[domain] || {})
            .forEach(([targetDomain]) => this.traverseHighlight(targetDomain, degree + 1));

    }

    // callback function to handle on zoom end event
    // updates the state variable {currentZoomLevel} 
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
        if (this.state.currentZoomLevel < 2 || this.state.graphData['nodes'].length > 100) {
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
        ctx.font = '2px Source Sans Pro';
        const fontSize = Math.min(MAX_FONT_SIZE, maxTextLength / ctx.measureText(label).width);
        ctx.font = `${fontSize}px Sans-Serif`;
        const textWidth = ctx.measureText(label).width;
        const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding
        // draw text label (with background rect)
        ctx.save();
        ctx.translate(textPos.x, textPos.y);
        ctx.rotate(textAngle);
        ctx.fillStyle = this.state.isDarkMode ? 'rgba(0, 0, 0, 0.2)' : 'rgba(1, 1, 1, 0.2)';
        ctx.fillRect(- bckgDimensions[0] / 2, - bckgDimensions[1] / 2, ...bckgDimensions);
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = this.state.isDarkMode ? 'lightgrey' : 'black'; // '#C8C8C8'; // '#E8E8E8'; // 'lightgrey';
        ctx.fillText(label, 0, 0);
        ctx.restore();
    }
}


export default Graph2D;



// Mobile footer component
function MobileFooter() {
    return (
        <div className='mobile-footer'>
            <span className='info-icon'>
                <InfoIcon />
            </span>
            <span className='info-text'>
                We recommend you seeing this visualization on a desktop device for best experience
            </span>
        </div>
    )
}

