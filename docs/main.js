const examples = {
  "Simple": "../examples/simple.json",
  "Open Permit": "../examples/open_permit.json",
  "Open Tax": "../examples/open_tax.json",
  "Agent Interaction": "../examples/agent_interaction.json"
};

function populate() {
  const select = document.getElementById('packSelect');
  for (const label in examples) {
    const opt = document.createElement('option');
    opt.value = examples[label];
    opt.textContent = label;
    select.appendChild(opt);
  }
}

function validate(data) {
  if (typeof data.pack !== 'string') return false;
  if ('nodes' in data) {
    if (!Array.isArray(data.nodes)) return false;
    for (const n of data.nodes) {
      if (!n.name || !n.type) return false;
    }
  }
  if ('edges' in data) {
    if (!Array.isArray(data.edges)) return false;
    for (const e of data.edges) {
      if (!e.from || !e.to) return false;
    }
  }
  return true;
}

function draw(data) {
  const width = 600, height = 400;
  const nodes = (data.nodes || []).map(n => ({id: n.name, type: n.type}));
  const links = (data.edges || []).map(e => ({source: e.from, target: e.to}));
  d3.select('#graph').selectAll('*').remove();
  const svg = d3.select('#graph').append('svg')
      .attr('width', width)
      .attr('height', height);
  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(100))
    .force('charge', d3.forceManyBody().strength(-200))
    .force('center', d3.forceCenter(width / 2, height / 2));

  const link = svg.append('g')
    .attr('stroke', '#999')
    .selectAll('line')
    .data(links)
    .enter().append('line');

  const node = svg.append('g')
    .attr('stroke', '#fff')
    .attr('stroke-width', 1.5)
    .selectAll('circle')
    .data(nodes)
    .enter().append('circle')
    .attr('r', 10)
    .attr('fill', '#1f77b4')
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended));

  const label = svg.append('g')
    .selectAll('text')
    .data(nodes)
    .enter().append('text')
    .attr('dy', -15)
    .text(d => d.id);

  simulation.on('tick', () => {
    link.attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

    node.attr('cx', d => d.x)
        .attr('cy', d => d.y);

    label.attr('x', d => d.x)
         .attr('y', d => d.y);
  });

  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }
  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }
  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
}

function runAllTests() {
  const log = document.getElementById('testOutput');
  log.textContent = 'Running tests...';
  const entries = Object.entries(examples).map(([label, path]) =>
    fetch(path)
      .then(resp => resp.json())
      .then(data => label + ': ' + (validate(data) ? 'pass' : 'fail'))
      .catch(() => label + ': error')
  );
  Promise.all(entries).then(results => {
    log.textContent = results.join('\n');
  });
}

function repoInfo() {
  const hostParts = location.hostname.split('.');
  const owner = hostParts[0];
  const repo = location.pathname.split('/')[1];
  return {owner, repo};
}

document.addEventListener('DOMContentLoaded', () => {
  populate();
  const {owner, repo} = repoInfo();
  document.getElementById('prBtn').href =
    `https://github.com/${owner}/${repo}/compare`;

  document.getElementById('loadBtn').addEventListener('click', () => {
    const path = document.getElementById('packSelect').value;
    fetch(path).then(resp => resp.json()).then(data => {
      draw(data);
      document.getElementById('testOutput').textContent =
        validate(data) ? 'Valid' : 'Invalid';
    });
  });

  document.getElementById('testBtn').addEventListener('click', runAllTests);
});
