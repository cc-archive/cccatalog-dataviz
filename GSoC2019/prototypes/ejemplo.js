const Graph = ForceGraph();

// Controls
const gui = new dat.GUI();
const controls = {
  'Dataset': '2018-03',
  'Find user': ''
};
gui.add(controls, 'Dataset', ['2015-11', '2016-05', '2016-10', '2018-03']).onChange(year => {
  Graph.stopAnimation();
  loadSet(`blocks-${year}.json`);
});
const userSearchControl = gui.add(controls, 'Find user');

loadSet(`blocks-${controls.Dataset}.json`);

function loadSet(file) {
  fetch(file).then(res => res.json())
    .then(parseGraphData)
    .then(graphData => {

      let hoverLink = null;
      let hoverNode = null;
      const highlightUsers = new Map();
      const linksPerUsers = indexBy(graphData.links, ['source', 'target']); // Dual-indexed by source user > target user
      const users = new Set(graphData.nodes.map(d => d.user.toLowerCase()));

      const elem = document.getElementById('graph');

      const graph = Graph(elem)
        .graphData(graphData)

        // nodes
        .nodeId('user')
        .nodeCanvasObject(drawNodeText)
        .nodeRelSize(7) // Determines size of hover area (circle)
        .nodeVal(node => Math.cbrt(node.blocks.length))

        // links
        .linkWidth(link => (hoverLink === link || highlightUsers.has(link.source.user)) ? 2.5 : 1)
        .linkHoverPrecision(10)

        // photons
        .linkDirectionalParticles(l => Math.sqrt(l.blockLinks.length) * 1.5)
        .linkDirectionalParticleWidth(link => Math.sqrt(link.blockLinks.length) / 3)
        .linkDirectionalParticleSpeed(l => Math.sqrt(l.blockLinks.length) * 0.002)

        // tooltips
        //.nodeLabel(({ user, blocks }) => `${user} (${blocks.length} blocks)`)
        //.linkLabel(({ source: { user: sourceUser }, target: { user: targetUser }, blockLinks}) => `${targetUser} > ${sourceUser} (${blockLinks.length} block references)`)

        // colors
        .backgroundColor('rgb(10, 10, 20)')
        .linkColor(link => link === hoverLink ? 'rgba(240, 230, 140, 0.5)' : 'rgba(255, 255, 255, 0.09)')
        .linkDirectionalParticleColor(() => 'rgba(255, 255, 255, 0.5)')

        // interaction
        .onNodeClick(node => window.open(`https://bl.ocks.org/${node.user}`, '_blank'))
        .onNodeHover(node => {
          hoverNode = node;
          elem.style.cursor = node ? 'pointer' : null;

          highlightUsers.clear();
          if (node) {
            traverseHighlight(node.user);
          }
        })
        .onLinkHover(link => hoverLink = link)

        // force engine
        .d3AlphaDecay(0.02)
        .d3VelocityDecay(0.2)

        // initial zoom
        .zoom(1.3);

      userSearchControl.onChange(user => {
        const userLc = user.toLowerCase();
        if (userLc && users.has(userLc)) {
          const node = graphData.nodes[graphData.nodes.map(d => d.user.toLowerCase()).indexOf(userLc)];

          if (node && node.hasOwnProperty('x')) {
            graph.centerAt(node.x, node.y, 1000);
            graph.zoom(6, 2000);
          }
        }
      });

      //

      function drawNodeText(node, ctx, globalScale) {
        const hovered = node === hoverNode;
        const highlight = (hoverLink && (hoverLink.source === node || hoverLink.target === node)) || highlightUsers.has(node.user);
        const degreeDistance = highlight && highlightUsers.has(node.user) ? highlightUsers.get(node.user) : null;

        const label = node.user;
        const fontSize = Math.max(hovered ? 16 : 0, Math.cbrt(node.blocks.length) * 5) / globalScale;
        ctx.font = `${fontSize}px Sans-Serif`;
        const textWidth = fontSize * label.length * 0.55;
        const bckgDimensions = [textWidth, fontSize * 0.7].map(n => n + fontSize * 0.4); // some padding

        ctx.fillStyle = 'rgba(10, 10, 20, 0.6)';
        ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = hovered
          ? 'crimson'
          : highlight
            ? (degreeDistance ? tinycolor('khaki').desaturate(Math.sqrt(degreeDistance) * 20).toString() : 'khaki')
            : 'lightsteelblue';
        ctx.fillText(label, node.x, node.y);
      }

      function traverseHighlight(user, degree = -1) {
        if (!user) return;

        if (highlightUsers.has(user)) { // already been here
          highlightUsers.set(user, Math.min(degree, highlightUsers.get(user))); // keep closest degree
          return;
        }

        highlightUsers.set(user, degree);

        Object.entries(linksPerUsers[user] || {})
          .forEach(([targetUser]) => traverseHighlight(targetUser, degree + 1));
      }
    });

//

  function parseGraphData({ graph: { nodes, links }}) {
    const blocksPerUser = indexBy(nodes, 'user');
    const blocksPerId = indexBy(nodes, 'id', false);
    const verifiedLinks = links.filter(({ source, target }) =>
      [source, target].every(id => blocksPerId.hasOwnProperty(id) && blocksPerId[id].user) // exclude broken links
      && blocksPerId[source].user !== blocksPerId[target].user                             // exclude self links
    );
    const directionalLinksPerUser = indexBy(
      verifiedLinks,
      ['source', 'target'].map(prop => ({ [prop]: blockId }) => blocksPerId[blockId].user) // Dual-indexed by source user > target user
    );

    const allLinksPerUser = {};
    verifiedLinks.forEach(link => ['source', 'target'].map(prop => blocksPerId[link[prop]].user).forEach(user => {
      if (!allLinksPerUser.hasOwnProperty(user)) allLinksPerUser[user] = [];
      allLinksPerUser[user].push(link);
    }));

    return {
      nodes: Object.entries(blocksPerUser).map(([user, blocks]) => ({user, blocks}))
        .filter(({ user }) => user !== 'null' && user !== 'undefined')                    // exclude nully users
        .filter(({ user }) => allLinksPerUser[user] && allLinksPerUser[user].length > 0)  // exclude single nodes
        .sort((a, b) => a.blocks.length - b.blocks.length),
      links: [].concat(...Object.entries(directionalLinksPerUser).map(([source, targets]) =>
          Object.entries(targets).map(([target, blockLinks]) => ({source: target, target: source, blockLinks})) // Reverse source<>target direction
      ))
        .filter(({ source, target }) => source !== target && source !== 'undefined' && target !== 'undefined') // Exclude self references
    };
  }
}