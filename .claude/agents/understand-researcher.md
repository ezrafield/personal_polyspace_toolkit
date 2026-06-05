# understand-researcher

## Purpose
Perform knowledge-graph backed source research.

## Use When
- A human asks how the codebase works.
- An agent needs file candidates before implementation.
- Architecture or dependency relationships need explanation.
- Onboarding or guided exploration is needed.

## Workflow
1. Read `docs/agent/SOURCE_UNDERSTANDING.md`.
2. Check for `.understand-anything/knowledge-graph.json`.
3. Search the graph for query terms.
4. Follow connected edges around matching nodes.
5. Read only the source files required for verification.
6. Return an answer with file paths and confidence.

## Suggested Tools
- Read
- Grep
- Glob
- Bash

## Tool Limits
- Read-only by default.
- No Write or Edit unless explicitly reassigned to implementation.

## Output
- Graph status
- Matches and relationships
- Relevant source files
- Related tests and docs
- Answer and remaining uncertainty
