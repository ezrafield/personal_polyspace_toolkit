# RTK Integration

RTK is optional but recommended for token-efficient command execution.

## Purpose

RTK compresses noisy terminal output before an AI agent sees it. It is part of the context layer, not the correctness layer.

## Recommended Usage

- Local coding agents: enable an RTK hook when the agent runtime supports hooks.
- Codex-style agents: use `AGENTS.md` command-output rules and optional make wrappers.
- CI: do not require RTK for correctness.
- Debugging: allow raw output fallback for exact failures and generated artifacts.

## Verify

```bash
rtk --version
rtk gain
```

## Disable For One Command

```bash
RTK_DISABLED=1 <command>
```

## Design Notes

- RTK should degrade gracefully. If it is missing or filtering fails, run the original command.
- Keep raw command access available for security review, artifact verification, and unclear failures.
- Record compressed-vs-raw command usage in task logs when a task needs an audit trail.
