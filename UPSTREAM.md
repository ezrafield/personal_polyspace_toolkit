# Upstream Tracking

## Baseline

- Repository: `https://github.com/mathworks/polyspace-agentic-toolkit`
- Source commit: `cc15b840e80bf5187963d13ed86c4c5bb86381ad`
- Tested MCP server release: `v1.1.1`

## Sync Policy

Upstream updates are reviewed manually. Never merge platform manifests, setup prompts, or skill text
blindly. For every candidate update:

1. Read its license and release notes.
2. Compare MCP tool names and argument contracts.
3. Port only C-relevant domain corrections.
4. Preserve local safety, explicit-profile, telemetry, and approval policies.
5. Update tested release digests only after cross-platform fake integration tests and an available
   licensed smoke run.
6. Record the upstream commit and local changes here.
