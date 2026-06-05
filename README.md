# Agent-Native Project Template

This repository is a sample structure for projects that collaborate well with coding agents such as Codex and Claude Code.

The design uses short auto-loaded instruction files and richer on-demand documentation. Agents start with `AGENTS.md` or `CLAUDE.md`, route through `docs/agent/INDEX.md`, then read only the module cards and specs relevant to the current task.

## Structure
- `AGENTS.md` and `CLAUDE.md`: short agent entrypoints.
- `.agents/skills/`: reusable project-local skill templates.
- `.claude/agents/`: Claude Code subagent templates.
- `.mcp/`: MCP setup notes and candidate server documentation.
- `.understand-anything/`: Understand Anything setup notes for source-code knowledge graphs.
- `docs/agent/`: on-demand agent context and navigation.
- `.agent/tasks/`: task-local notes and audit trail.
- `src/`: sample application modules.
- `tests/`: sample test structure and local testing rules.
- `scripts/`: helper scripts for generated agent context.
- `eval/`: golden and regression evaluation placeholders.

## Getting Started
```bash
make install
make test-unit
make lint
```

This is a template, so most commands are placeholders until you wire them to your actual stack.

## Source Understanding

Use Understand Anything to generate a knowledge graph for humans and agents:

```bash
make understand
make understand-search QUERY="api route"
```

Generated graph files are ignored by default; setup notes and ignore rules are committed.
