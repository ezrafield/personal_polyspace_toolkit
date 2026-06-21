# Task: Example Task

## Goal
Show how a task-local note captures useful context without bloating root agent instructions.

## User Request
Create a sample agent-native project structure.

## Relevant Docs Read
- `instruction.txt`

## Files Inspected
- `instruction.txt`

## Assumptions
- The repository is a template, not a finished application.

## Plan
1. Create thin root agent entrypoints.
2. Add on-demand agent documentation.
3. Add task-log, scripts, test, and eval placeholders.
4. Verify the resulting tree.

## Changes Made
- Added template structure and sample files.
- Added reusable general skills under `.agents/skills/`.
- Added Claude subagent templates under `.claude/agents/`.
- Added general tool, MCP, and agent docs under `docs/agent/`.
- Added deterministic helper scripts and command wiring.

## Commands Run
| Command | RTK Used | Raw Rerun | Reason |
| --- | --- | --- | --- |
| `python scripts/validate_docs.py` | no | no | docs validation |
| `python scripts/check_agent_rules.py` | no | no | agent rule validation |
| `py --version` | no | no | environment check |
| `git status --short` | no | no | repository state check |

## Token / Context Notes
- No compressed output layer was available for the original example task.
- Raw output remained small enough to inspect directly.

## Verification
- Structure was verified with a recursive file listing.
- Python validation scripts could not run because `python` and `py` are not available on PATH in this environment.
- Git status could not run because this directory is not initialized as a Git repository.

## Memory Extraction
- Candidate generated: no
- Promotion needed: no
- Notes: Example task predates the memory workflow.

## Follow-Up
Replace placeholder commands and sample modules with real project behavior.
