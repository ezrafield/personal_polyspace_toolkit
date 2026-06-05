# Safe Implementation

## Purpose
Provide the standard workflow for a feature or bug fix.

## Trigger
Use when the user asks to implement, patch, refactor, or fix behavior.

## Workflow
1. Restate the goal.
2. Identify affected modules.
3. Read only relevant docs and files.
4. Make the smallest safe patch.
5. Add or update tests.
6. Run targeted checks.
7. Summarize files changed, commands run, and risks.

## Output
- Goal
- Plan
- Changed files
- Tests or commands run
- Remaining risks

## Constraints
- Do not add dependencies without justification.
- Do not change public contracts without updating specs.
- Do not broaden scope unless needed for correctness.
