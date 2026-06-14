# Command Output Policy

Terminal output is project context. Treat noisy command output the same way as noisy source reads: compress it by default, then inspect raw output only when needed.

## Default

Use compressed command output for noisy commands when RTK or an equivalent output filter is available.

Prefer compressed output for:
- `git status`
- `git diff`
- `git log`
- `grep`, `find`, `ls`, and `tree`
- `pytest`, `vitest`, `cargo test`, and `go test`
- lint and typecheck commands
- Docker, Kubernetes, and application logs

## Raw Output

Use raw output when:
- debugging parser or filter behavior
- a test failure is unclear
- exact stdout or stderr matters
- reviewing security-sensitive output
- verifying generated artifacts
- the compressed result looks incomplete or suspicious

## Fallback

- If RTK is unavailable, run the original command.
- If compressed output is insufficient, rerun the smallest relevant command in raw mode.
- Do not hide failures. Exit codes, stack traces, failed assertions, and actionable errors must remain visible.
- Mention raw reruns in the final command summary or task log.
