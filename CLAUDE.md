# CLAUDE.md

Use this project as an agent-native codebase.

## Start Here
For every non-trivial task:
1. Read `docs/agent/INDEX.md`.
2. Read the relevant module card.
3. Create or update a task note in `.agent/tasks/` if the task has more than one step.
4. Use `.agent/plans/template.md` for complex or multi-phase work.

## Token-Saving Behavior
- Do not explore unrelated directories.
- Use Semble for natural-language code search before reading many files.
- Use `rg` for exact symbol and string confirmation.
- Use Serena only when symbol references, declarations, implementations, diagnostics, or safe refactors require language-server semantics.
- Prefer targeted reads over broad scans.
- Summarize findings before expanding scope.

## Safety
- Never delete files, rewrite migrations, rotate secrets, or change production config without explicit approval.
- Prefer small patches.
- Run targeted tests first.

## Final Response Format
- Summary
- Files changed
- Tests or commands run
- Risks or follow-up
