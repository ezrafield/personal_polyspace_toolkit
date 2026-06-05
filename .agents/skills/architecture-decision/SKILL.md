# Architecture Decision

## Purpose
Prevent over-engineering and make larger technical choices explicit.

## Trigger
Use when choosing between architectures, adding dependencies, changing databases, adding queues or caches, changing service boundaries, or choosing RAG/tool-calling/workflow/agent patterns.

## Workflow
1. State the decision to make.
2. Identify constraints and non-goals.
3. Compare 2-3 practical options.
4. Recommend the simplest option that satisfies the constraints.
5. Update or create an ADR when the decision is durable.

## Output
- Decision
- Options considered
- Recommendation
- Tradeoffs
- ADR update needed: yes/no

## Constraints
- Prefer the existing architecture unless a real constraint requires change.
- Do not add infrastructure just because it is available.
