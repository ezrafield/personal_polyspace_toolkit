# Memory Policy

Long-term memory helps agents reuse durable lessons without reading old task logs.
It is guidance, not source of truth.

## Memory Types

| Type | Meaning | Location |
| --- | --- | --- |
| Semantic | Stable facts, conventions, and decisions | `.agent/memory/semantic/` |
| Procedural | Reusable workflows and playbooks | `.agent/memory/procedural/` |
| Episodic | Raw task logs and audit trails | `.agent/tasks/` |

## Authority

Use memory to choose likely files, workflows, commands, and risks. Before editing,
verify memory against current source files, tests, and docs. If memory conflicts
with the repository, the repository wins.

## Safety

Never promote:

- secrets, credentials, tokens, or private keys
- customer data or private user content
- raw stack traces containing sensitive paths or data
- one-off debugging noise
- claims that were not verified
- guidance that says to always edit a specific file when the real issue may vary

## Card Requirements

Promoted memory cards should include:

- `Type`
- `Scope`
- `Confidence`
- `Last verified`
- `Source task`
- `When to use`
- `Content` or `Procedure`
- `Related files`
- `Staleness triggers`
