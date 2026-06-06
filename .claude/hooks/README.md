# Claude Hooks

These hooks are optional examples for teams that want lightweight guardrails.

Start with warnings before blocking developer flow. Useful hooks include:

- `block-secret-output.sh`: rejects obvious secret-like output.
- `warn-large-agent-files.sh`: warns when auto-loaded agent files grow past the context budget.

Keep hook configuration local to the project runtime. Do not store secrets in hook files.
