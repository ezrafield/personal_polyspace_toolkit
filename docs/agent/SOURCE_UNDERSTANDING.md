# Source Understanding

Use Understand Anything as the shared source-code understanding and search layer for humans and agents.

## Purpose

Understand Anything generates a code knowledge graph at:

```txt
.understand-anything/knowledge-graph.json
```

That graph can support:
- Architecture discovery
- Component and dependency search
- Guided onboarding tours
- Code question answering
- Diff and risk analysis
- Human review and agent handoff

## Human Workflow

1. Generate or refresh the graph.
2. Open the dashboard when visual exploration helps.
3. Ask graph-backed questions before scanning the whole repository.
4. Use source links from the graph to inspect actual files.

Recommended commands:

```bash
make understand
make understand-dashboard
make understand-search QUERY="auth service"
```

## Agent Workflow

Before broad source exploration:

1. Read `docs/agent/INDEX.md`.
2. Read this file.
3. Check whether `.understand-anything/knowledge-graph.json` exists.
4. If it exists, search the graph before reading many files.
5. If it does not exist or is stale, recommend `make understand`.
6. Use targeted file reads for final verification.

## What To Commit

Commit:
- `.understand-anything/README.md`
- `.understand-anything/.understandignore`
- `.understand-anything/config.example.json`
- Docs and scripts that explain how to use the graph

Usually ignore:
- `.understand-anything/knowledge-graph.json`
- `.understand-anything/meta.json`
- `.understand-anything/intermediate/`
- `.understand-anything/tmp/`
- Generated graph variants unless the team explicitly wants them versioned

## Search Strategy

For a question like "where is request validation handled?":

1. Search node names, summaries, and tags in the graph.
2. Follow connected edges for imports, calls, tests, and documents.
3. Identify the architectural layer.
4. Read only the few relevant source files.
5. Summarize the answer with file paths and relationships.

## Refresh Policy

Refresh the graph:
- After adding or moving modules.
- After large refactors.
- Before onboarding a new human or agent.
- Before architecture review.
- Before asking broad codebase questions.

For small isolated edits, graph refresh can wait until the end of the task.
