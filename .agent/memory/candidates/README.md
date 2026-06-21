# Candidate Memory

This folder holds generated memory candidates.

Candidates are not long-term memory until a human or agent reviews them, removes
low-value or sensitive content, moves them into `semantic/` or `procedural/`,
and updates `.agent/memory/index.json`.

Use:

```bash
make extract-task-memory TASK=.agent/tasks/<task>.md
```
