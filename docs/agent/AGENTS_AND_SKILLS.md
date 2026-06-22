# Agents And Skills

`skills/` is the sole product skill source. Client installers copy from it; plugin metadata points to
it; Qwen users link or copy it manually.

The Codex plugin contains a generated copy because plugin bundles must be self-contained. Refresh it
with `python scripts/sync_codex_plugin.py` and enforce parity with `--check`.

## Product Skills

| Skill | Responsibility |
| --- | --- |
| `toolkit-setup` | Deterministic setup and verification |
| `c-compliance-loop` | End-to-end compliance workflow |
| `run-analysis` | C translation-unit analysis |
| `fix-findings` | Evidence-led remediation |
| `justify-findings` | Approval-gated annotations |
| `configure-build-options` | C build capture |
| `configure-checkers` | Explicit C checker profiles |
| `find-checker-documentation` | Finding documentation |
| `find-option-documentation` | Installed-release option documentation |
| `query-justification-catalog` | Exact approved-text lookup |
| `generate-c-pstunit-tests` | Approval-gated C unit tests |

General repository skills under `.agents/skills/` remain development aids, not product deliverables.
Product skills must have YAML frontmatter, stay focused, use exact MCP tool names, and place lengthy
reference material beside the owning skill.
