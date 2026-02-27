import ForceGraph2D from "react-force-graph-2d";

export default function AttackGraph({ domain, assets }) {
  const nodes = [{ id: domain, group: 1 }];
  const links = [];

  assets.forEach((a, i) => {
    nodes.push({ id: a.subdomain, group: 2 });
    links.push({ source: domain, target: a.subdomain });

    if (a.ip) {
      const ipNode = `${a.ip}-${i}`;
      nodes.push({ id: ipNode, group: 3 });
      links.push({ source: a.subdomain, target: ipNode });
    }
  });

  return (
    <div>
      <h3>Attack Surface Graph</h3>
      <ForceGraph2D
        graphData={{ nodes, links }}
        nodeAutoColorBy="group"
        height={400}
      />
    </div>
  );
}