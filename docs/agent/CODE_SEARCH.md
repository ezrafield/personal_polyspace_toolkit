# Code Search

Use Semble, `rg`, and optional semantic tools as complementary retrieval layers.

## Default Stack

Use by default:
- `docs/agent/CODEMAP.md` for quick module orientation.
- Module cards for ownership, public interfaces, tests, and pitfalls.
- Semble for natural-language source search.
- `rg` for exact symbols, strings, config keys, and paths.

Use optionally:
- Serena for language-server backed symbol navigation, references, diagnostics, and safer refactors.
- ast-grep for structural code patterns.
- Understand Anything for graph and dependency impact analysis.
- Repomix only as an export/bundling tool for external model review.

## Search Order

1. Read `docs/agent/INDEX.md`.
2. Read `docs/agent/CODEMAP.md` or the relevant module card.
3. Search natural language with Semble:

```bash
semble search "<task>" . --content code
semble search "<task>" . --content all
```

Use `--content code` for implementation tasks. Use `--content all` when docs, tests, config, prompts, or generated context may affect the answer.

4. Confirm exact names with `rg`:

```bash
rg "ExactSymbolOrString"
rg --files | rg "module-name|test-name"
```

5. Use Serena when symbol-level behavior matters:
- Find declarations and implementations.
- Find all references.
- Inspect diagnostics.
- Plan safe renames or refactors.

6. Read full files only after retrieval identifies likely targets.

## Decision Matrix

| Situation | Best tool |
| --- | --- |
| "Where is auth handled?" | Semble |
| "Find all places this function is called" | Serena |
| "Search exact env var name" | `rg` |
| "Find React components matching a structure" | ast-grep |
| "Understand repo modules quickly" | `docs/agent/CODEMAP.md` |
| "Analyze dependency impact" | Understand Anything / graph |
| "Send whole repo to external model" | Repomix |
| "Large enterprise monorepo search" | Sourcegraph/Cody |
| "General template default" | Semble + `rg` + CODEMAP |
| "Advanced coding setup" | Semble + Serena + `rg` + CODEMAP |

## Before Editing

Summarize:
- Selected files.
- Why they are relevant.
- Uncertainty or risk.

Then make the smallest safe change and run targeted tests first.
