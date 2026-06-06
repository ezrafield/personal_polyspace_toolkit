# Agent-Native Project Template

This repository is a sample structure for projects that collaborate well with coding agents such as Codex and Claude Code.

The design uses short auto-loaded instruction files and richer on-demand documentation. Agents start with `AGENTS.md` or `CLAUDE.md`, route through `docs/agent/INDEX.md`, then read only the module cards and specs relevant to the current task.

## Structure
- `AGENTS.md` and `CLAUDE.md`: short agent entrypoints.
- `agentkit-manifest.json`, `install.sh`, and `update.sh`: installer metadata and wrappers for adding the kit to real projects.
- `.agents/skills/`: reusable project-local skill templates.
- `.claude/agents/`: Claude Code subagent templates.
- `.claude/hooks/`: optional lightweight hook examples.
- `.mcp/`: MCP setup notes and candidate server documentation.
- `.understand-anything/`: Understand Anything setup notes for source-code knowledge graphs.
- `docs/agent/`: on-demand agent context and navigation.
- `.agent/tasks/`: task-local notes and audit trail.
- `.agent/plans/`: lightweight plan lifecycle folders and template.
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

## Installing Into Another Project

From a checkout of this template:

```bash
./install.sh /path/to/project
```

The installer reads `agentkit-manifest.json`, backs up existing agent config under `.agentkit/backups/`, merges `AGENTS.md` and `CLAUDE.md`, copies harness files, and records installed paths in `.agentkit-installed-files`. Use `./update.sh /path/to/project` to refresh the harness later.

After install, run:

```bash
python scripts/agent_setup.py
```

The setup script detects the stack and common commands, refreshes `docs/agent/CODEMAP.md`, creates missing module cards, ensures task-log scaffolding exists, and runs validation.

## Audits

```bash
make validate-agent-docs
make check-context-staleness
make audit-module-cards
make audit-task-logs
make detect-large-agent-files
```

Use audits as warnings during setup and stricter gates before sharing the kit with a team.

## Source Understanding

Use Understand Anything to generate a knowledge graph for humans and agents:

```bash
make understand
make understand-search QUERY="api route"
```

Generated graph files are ignored by default; setup notes and ignore rules are committed.
