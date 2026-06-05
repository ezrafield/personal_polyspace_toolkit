# Source Understanding

## Purpose
Use Understand Anything as a shared source-code understanding layer for humans and agents.

## Trigger
Use when the task requires codebase orientation, architecture discovery, onboarding, source search, or mapping a feature to files.

## Workflow
1. Read `docs/agent/SOURCE_UNDERSTANDING.md`.
2. Check whether `.understand-anything/knowledge-graph.json` exists.
3. If the graph exists, search it before broad source scanning.
4. If the graph is missing or stale, recommend `make understand`.
5. Read only the source files identified by the graph and module cards.
6. Verify graph conclusions against real files before making changes.

## Output
- Graph status
- Relevant graph matches
- Candidate source files
- Related tests or docs
- Confidence and stale-graph risks

## Constraints
- Do not load the whole graph into context unless it is tiny.
- Do not edit generated graph files manually.
- Do not treat graph output as authoritative without source verification.
