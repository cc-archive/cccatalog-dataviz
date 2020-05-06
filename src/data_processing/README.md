# Data for visualization

The project uses [force-graph](https://github.com/vasturiano/force-graph) to render a force-directed graph to visualize the available data on a HTML5 canvas.
The data to be visualized using `force-graph` can be found in `graph_data_input_file.old.json`. The JSON data contains two types of objects: nodes and links.

## Nodes
A node represents a unique domain containing CC licensed data. Each node has the following fields: 
1. `id`: Top level domain extracted from `provider_domain` using [tldextract](https://github.com/john-kurkowski/tldextract)
2. `provider_domain`: name of the domain with licensed content.
3. `cc_license`: CC licenses associated with the content present on `provider_domain`
4. `images`: number of images showed in the `provider_domain` web page.

## Links
A link represents the references between two domains. Each link has the following fields:
1. `source`: Domain that references the licensed content.
2. `target`: Domain that hosts the licensed content.
3. `value`: The number of references made by the `source` domain to the `target` domain.
