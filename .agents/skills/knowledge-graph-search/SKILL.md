# Knowledge Graph Search

## Purpose
Answer source-code questions through targeted search of `.understand-anything/knowledge-graph.json`.

## Trigger
Use when a human or agent asks where something lives, how components connect, what depends on a file, or which tests/docs relate to a feature.

## Workflow
1. Confirm `.understand-anything/knowledge-graph.json` exists.
2. Search node names, summaries, tags, and file paths for the query terms.
3. Follow one-hop edges around matching node IDs.
4. Identify relevant layers and tour steps when available.
5. Read the smallest set of source files needed to verify the answer.

## Output
- Query
- Matching nodes
- Connected nodes or edges
- Relevant layers
- Files to inspect
- Answer with source-backed caveats

## Constraints
- Do not dump the full graph into context.
- If no graph exists, ask for `make understand` or fall back to `repo-navigator`.
- If no matches appear, suggest related search terms from nearby graph metadata.
