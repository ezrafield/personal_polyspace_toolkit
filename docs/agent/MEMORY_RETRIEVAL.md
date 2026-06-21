# Memory Retrieval

Use memory after the standard context router and before code search.

## Startup Flow

1. Read `docs/agent/INDEX.md`.
2. Check `.agent/memory/index.json` for relevant semantic or procedural memory.
3. Read only memory cards that match the task scope or keywords.
4. Use memory to choose likely files, workflows, tests, and risks.
5. Verify memory with current docs, code, Semble, `rg`, or Serena before editing.
6. Ignore memory that conflicts with current source, tests, specs, or agent docs.

## Retrieval Hints

- Use semantic memory for project facts, conventions, and decisions.
- Use procedural memory for workflows, debugging steps, testing strategy, and refactors.
- Use episodic memory only when a recent task log is directly relevant or a handoff points to it.

## With Existing Tools

| Tool | Role |
| --- | --- |
| Module cards and CODEMAP | Explain current architecture and ownership |
| Memory | Recall durable lessons from previous work |
| Semble | Find current relevant code snippets |
| `rg` | Confirm exact names, paths, and strings |
| Serena | Check references, declarations, diagnostics, and safe refactors |
| RTK | Compress noisy command output |

Memory should reduce blind searching, not replace verification.
