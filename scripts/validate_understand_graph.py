import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / ".understand-anything" / "knowledge-graph.json"


def main() -> None:
    if not GRAPH.exists():
        print("No graph found at .understand-anything/knowledge-graph.json")
        raise SystemExit(1)

    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    issues = []

    for key in ["project", "nodes", "edges"]:
        if key not in graph:
            issues.append(f"Missing top-level key: {key}")

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    layers = graph.get("layers", [])
    tour = graph.get("tour", [])

    if not isinstance(nodes, list):
        issues.append("nodes must be a list")
        nodes = []
    if not isinstance(edges, list):
        issues.append("edges must be a list")
        edges = []
    if layers and not isinstance(layers, list):
        issues.append("layers must be a list when present")
        layers = []
    if tour and not isinstance(tour, list):
        issues.append("tour must be a list when present")
        tour = []

    node_ids = {node.get("id") for node in nodes if isinstance(node, dict)}
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            issues.append(f"Node {index} is not an object")
            continue
        for key in ["id", "type", "name"]:
            if not node.get(key):
                issues.append(f"Node {index} missing {key}")

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            issues.append(f"Edge {index} is not an object")
            continue
        if edge.get("source") not in node_ids:
            issues.append(f"Edge {index} has missing source {edge.get('source')}")
        if edge.get("target") not in node_ids:
            issues.append(f"Edge {index} has missing target {edge.get('target')}")

    if issues:
        print("Understand graph validation failed:")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(1)

    print("Understand graph looks valid.")
    print(f"Nodes: {len(nodes)}")
    print(f"Edges: {len(edges)}")
    print(f"Layers: {len(layers)}")
    print(f"Tour steps: {len(tour)}")


if __name__ == "__main__":
    main()
