# MCPs

Model Context Protocol servers should be added only when they provide useful external context or reliable actions that scripts cannot provide locally.

## General MCP Categories

| MCP Category | Use |
| --- | --- |
| Semble | Natural-language project search before broad file reads. |
| Serena | Optional language-server semantics for references, declarations, diagnostics, and refactors. |
| Filesystem | Structured file reads, writes, and project resources. |
| GitHub | Issues, pull requests, review comments, CI state, and repository metadata. |
| Browser | Local app inspection, screenshots, and interactive UI verification. |
| Database | Schema inspection and safe read-only query workflows. |
| Documentation | Current official docs for unstable APIs or SDKs. |
| Design | Figma, FigJam, or design-system workflows. |
| Secrets | Controlled credential provisioning without exposing plaintext. |

## MCP Selection Rules

- Use local scripts first for deterministic repo checks.
- Use Semble as the default low-cost code retrieval profile when available.
- Use Serena only when symbol-level accuracy or refactoring support is needed.
- Use MCPs when external state matters.
- Keep write-capable MCPs scoped and documented.
- Prefer read-only modes for research and review agents.
- Document required MCPs in `docs/agent/COMMANDS.md` or a project-specific setup guide.

## Project Template

Use `.mcp/README.md` to document candidate MCPs for a project. Use `.mcp/servers.example.json` as a non-secret placeholder. Add real MCP configuration only when the team knows which runtime will consume it.
