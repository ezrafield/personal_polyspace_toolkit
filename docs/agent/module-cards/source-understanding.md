# Module: Source Understanding

## Responsibility
Provides knowledge-graph based source discovery, search, onboarding, and architecture exploration.

## Key Files
- `.understand-anything/README.md`: local setup notes
- `.understand-anything/.understandignore`: analysis exclusions
- `docs/agent/SOURCE_UNDERSTANDING.md`: workflow guidance
- `scripts/search_understand_graph.py`: local graph search helper
- `scripts/validate_understand_graph.py`: graph shape validator

## Public Interfaces
- `.understand-anything/knowledge-graph.json`
- `make understand`
- `make understand-search`
- `make understand-dashboard`

## Rules
- Do not commit generated graph files unless explicitly agreed.
- Search the graph before broad source scanning.
- Verify graph answers against source files before changing code.
- Keep `.understandignore` aligned with generated and dependency folders.

## Common Tasks
- Refresh graph: run `make understand`.
- Search graph: run `make understand-search QUERY="term"`.
- Visual explore: run `make understand-dashboard`.
- Validate graph: run `make validate-understand-graph`.

## Known Pitfalls
- A stale graph can mislead agents after large refactors.
- Generated graph files can become large and noisy in Git.
- Graph search supplements source reads; it does not replace verification.
