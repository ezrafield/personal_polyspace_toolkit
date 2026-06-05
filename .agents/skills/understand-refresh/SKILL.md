# Understand Refresh

## Purpose
Refresh the Understand Anything graph at appropriate moments.

## Trigger
Use after large refactors, module moves, architecture changes, onboarding prep, or before broad codebase Q&A.

## Workflow
1. Read `.understand-anything/README.md`.
2. Review `.understand-anything/.understandignore`.
3. Run `make understand` or the runtime's `/understand` command.
4. Run `make validate-understand-graph` when available.
5. Report analyzed files, warnings, graph path, and dashboard availability.

## Output
- Refresh command
- Graph path
- Validation result
- Warnings
- Suggested next query or dashboard step

## Constraints
- Do not commit generated graph files unless explicitly requested.
- Do not refresh during tiny code edits unless graph staleness affects the task.
