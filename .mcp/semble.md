# Semble MCP Profile

Semble is the default natural-language retrieval layer for this template.

## Use Cases

- Locate relevant source files from behavior-level task descriptions.
- Search code, tests, docs, prompts, and config without loading the whole repository.
- Support progressive context loading before exact `rg` confirmation.

## Recommended Commands

```bash
semble search "<task>" . --content code
semble search "<task>" . --content all
```

Use `--content code` for implementation tasks. Use `--content all` when docs, specs, config, or tests may matter.

## Agent Policy

1. Read `docs/agent/INDEX.md`.
2. Read `docs/agent/CODEMAP.md` or the relevant module card.
3. Use Semble to identify candidate files.
4. Use `rg` to confirm exact symbols and strings.
5. Read full files only after retrieval narrows the target list.

## Ignore Rules

Keep `.sembleignore` aligned with `.gitignore`, generated artifacts, dependencies, caches, build outputs, and large local context files.
