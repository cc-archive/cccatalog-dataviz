# Google Summer of Code (GSoC) 2019
There is no larger compendium of shared human knowledge and creativity than the Commons, including over 1.4 billion digital works available under CC tools. Although a huge amount of CC-licensed content has been
indexed with the [CC Search project](https://search.creativecommons.org/), there is still not a way of conveying the scale of this work to thecommunity. Being able to access visualizations of all the indexed content is a good way for the
community (and CC) to see how much data has been indexed and find and explore
relationships between CC-licensed content on the web.

The frontend app is built using [force-graph](https://github.com/vasturiano/force-graph), [Highcharts](https://www.highcharts.com) and [Bootstrap](https://getbootstrap.com/).

## Project Report

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

Just access the index.html file in Firefox browser (in Chrome there is a restriction that requires accessing files only through HTTP or HTTPS).

## Visualization in production
Visit the production website to view a demo of the force-directed graph in [2D](http://ec2-3-80-82-250.compute-1.amazonaws.com/) or [3D](http://ec2-3-80-82-250.compute-1.amazonaws.com/visualization_3d.html).

## The team
Student: [María Belén Guaranda](https://github.com/soccerdroid)

Mentors: [Sophine Clachar](https://creativecommons.org/author/sclachar/), [Breno Ferreira](https://creativecommons.org/author/brenoferreira/) and engineering director [Kriti Godey](https://creativecommons.org/author/kriticreativecommons-org/)
