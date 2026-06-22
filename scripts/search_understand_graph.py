import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / ".understand-anything" / "knowledge-graph.json"


def as_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return ""


def main() -> None:
    query = " ".join(sys.argv[1:]) or os.getenv("QUERY", "")
    if not query.strip():
        print('Usage: python scripts/search_understand_graph.py "query"')
        raise SystemExit(2)

    if not GRAPH.exists():
        print("No Understand Anything graph found at .understand-anything/knowledge-graph.json")
        print("Generate it with `make understand` or the Understand Anything runtime command.")
        raise SystemExit(1)

    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    terms = [term.lower() for term in query.split()]
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    layers = graph.get("layers", [])

    matches = []
    for node in nodes:
        haystack = " ".join(
            [
                as_text(node.get("id")),
                as_text(node.get("name")),
                as_text(node.get("filePath")),
                as_text(node.get("summary")),
                as_text(node.get("tags")),
            ]
        ).lower()
        if all(term in haystack for term in terms):
            matches.append(node)

    if not matches:
        print(f"No graph matches found for: {query}")
        raise SystemExit(0)

    match_ids = {node.get("id") for node in matches}
    connected = [
        edge for edge in edges if edge.get("source") in match_ids or edge.get("target") in match_ids
    ]
    layer_hits = [
        layer
        for layer in layers
        if any(node_id in match_ids for node_id in layer.get("nodeIds", []))
    ]

    print(f"Query: {query}")
    print(f"Matches: {len(matches)}")
    for node in matches[:10]:
        print("")
        print(f"- {node.get('id')}")
        if node.get("filePath"):
            print(f"  file: {node.get('filePath')}")
        if node.get("summary"):
            print(f"  summary: {node.get('summary')}")

    if layer_hits:
        print("")
        print("Layers:")
        for layer in layer_hits[:5]:
            print(f"- {layer.get('name')}: {layer.get('description')}")

    if connected:
        print("")
        print(f"Connected edges: {len(connected)}")
        for edge in connected[:10]:
            print(f"- {edge.get('source')} --{edge.get('type')}--> {edge.get('target')}")


if __name__ == "__main__":
    main()
