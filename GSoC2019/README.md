# The Linked Commons
There is no larger compendium of shared human knowledge and creativity than the Commons, including over 1.4 billion digital works available under CC tools. Although a huge amount of CC-licensed content has been indexed with the [CC Search project](https://search.creativecommons.org/), there is still not a way of conveying the scale of this work to the community. Being able to access visualizations of all the indexed content is a good way for the community (and CC) to see how much data has been indexed and find and explore relationships between CC-licensed content on the web.

The frontend app is built using [force-graph](https://github.com/vasturiano/force-graph), [Highcharts](https://www.highcharts.com) and [Bootstrap](https://getbootstrap.com/).

## Project Report
Technical details can be found in the [project report](https://github.com/creativecommons/cccatalog-dataviz/blob/master/GSoC2019/GSoC2019-Project-Report.pdf)

## Blog Post
- [Visualize CC Catalog data](https://opensource.creativecommons.org/blog/entries/cc-datacatalog-visualization/)
- [Visualize CC Catalog data - data processing](https://opensource.creativecommons.org/blog/entries/cc-datacatalog-data-processing/)
- [Visualize CC Catalog data - data processing part 2](https://opensource.creativecommons.org/blog/entries/cc-datacatalog-data-processing-2/)
- [Visualize CC Catalog data - data processing part 3](https://opensource.creativecommons.org/blog/entries/cc-datacatalog-data-processing-3/)
- [The Linked Commons graph: the final vis](https://opensource.creativecommons.org/blog/entries/cc-datacatalog-data-thelinkedcommons/)

## Repository structure

Everything is inside the src folder.
 - index.html: is the main file. It displays the same web page as in [Visualization in production](#visualization-in-production) and it contains the js script that builds the graph.
 - visualization_3d.html: renders the graph in 3D. 
 - js folder: contains the required dependencies for the correct visualization of the graph.
 - css folder: styling files. 
 
## Local deploy

The files can be hosted locally by running the following command in the `GSoC2019/src` folder.
```
python -m http.server 4000
```
The visualization can be found by navigating to http://localhost:4000/ in the browser.

## Demos
Visit the demo websites of the force-directed graph in [2D](http://dataviz.creativecommons.engineering/) or [3D](http://dataviz.creativecommons.engineering/visualization_3d.html).

## The team
Student: [María Belén Guaranda](https://github.com/soccerdroid)

Mentors: [Sophine Clachar](https://creativecommons.org/author/sclachar/), [Breno Ferreira](https://creativecommons.org/author/brenoferreira/) and engineering director [Kriti Godey](https://creativecommons.org/author/kriticreativecommons-org/)
