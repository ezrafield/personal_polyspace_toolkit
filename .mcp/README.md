# MCP Setup

This directory documents candidate Model Context Protocol servers for the project.

Do not commit secrets here.

## Candidate MCPs

| Name | Purpose | Scope |
| --- | --- | --- |
| filesystem | Structured local project access | Read/write by project root |
| github | Issues, PRs, CI, review threads | Repository metadata and selected actions |
| browser | Local UI verification | Browser automation |
| docs | Current official documentation | Read-only |
| database | Schema and safe queries | Prefer read-only |

## Configuration Notes

- Keep project-specific MCP config separate from user-local secrets.
- Prefer read-only permissions until write access is required.
- Record required setup steps in `docs/agent/COMMANDS.md`.
- Use `servers.example.json` as a placeholder, not as a working secret-bearing config.
