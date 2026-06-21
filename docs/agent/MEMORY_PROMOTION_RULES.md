# Memory Promotion Rules

Promotion is manual. Generated candidates are drafts until reviewed and indexed.

## Promotion Flow

1. Finish a meaningful task and update its `.agent/tasks/` log.
2. Run `make extract-task-memory TASK=.agent/tasks/<task>.md`.
3. Review the candidate in `.agent/memory/candidates/`.
4. Delete secrets, private data, noisy details, and unverified claims.
5. Move durable facts into `.agent/memory/semantic/` or reusable workflows into `.agent/memory/procedural/`.
6. Add or update the entry in `.agent/memory/index.json`.
7. Run `make audit-memory`.

## Promote When

- The lesson is likely to help future tasks.
- It is more compact than the original task log.
- It names when to use the lesson.
- It includes related files or docs that can be re-verified.
- It includes confidence and staleness triggers.

## Do Not Promote When

- The information is a one-off task detail.
- The claim depends on stale code that was not verified.
- The card would expose secrets or private data.
- The guidance is overbroad, such as "always edit this file when tests fail."

## Confidence

- High: verified against current code, tests, or docs.
- Medium: useful and plausible, but may need confirmation in nearby files.
- Low: keep as a candidate or task note; do not promote unless clearly marked and useful.
