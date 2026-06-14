# Estimated Benefits With Progressive Context And RTK

This estimate models how much time, token usage, and rework this template can save when it combines two context controls:

1. Progressive source retrieval:
   `AGENTS.md` / `CLAUDE.md` -> `docs/agent/INDEX.md` -> module cards / `CODEMAP.md` -> Semble -> `rg` -> optional Serena -> targeted files.
2. RTK-aware command output:
   compact `git`, search, test, lint, typecheck, and log output by default, with raw reruns only when exact details matter.

These are directional estimates, not benchmark guarantees. Use `make retrieval-eval`, `make rtk-gain`, task traces, and provider usage logs to measure your own project.

## What Changed With RTK Joining

Before RTK, this template mostly reduced tokens spent reading the wrong files. RTK adds a second savings layer: reducing tokens spent reading noisy terminal output.

| Context source | Template control | RTK control | Expected effect |
| --- | --- | --- | --- |
| Broad source reads | Index, module cards, CODEMAP, Semble, `rg` | None | Fewer irrelevant files loaded |
| Git status / diff | Compact make targets | RTK filters | Shorter patch review loops |
| Search output | Targeted `rg` / Semble | `rtk grep`, `rtk find` | Less repeated scan noise |
| Test output | Targeted tests first | `rtk pytest`, `rtk npm test`, `rtk cargo test` | Failures stay visible without full logs |
| Lint / typecheck output | Compact make targets | `rtk eslint`, `rtk tsc` | Faster diagnosis of actionable errors |
| Large runtime logs | Manual narrowing | RTK log filtering when available | Lower context-window pressure |

RTK is part of the context layer, not the correctness layer. It should preserve failures, degrade gracefully when missing, and allow raw output reruns whenever compressed output is incomplete or suspicious.

## Assumptions

| Factor | Small repo | Medium repo | Large repo |
| --- | ---: | ---: | ---: |
| Source files | 50-150 | 150-800 | 800-3,000 |
| Average file size | 150-300 lines | 150-350 lines | 150-400 lines |
| Typical task scope | 1-3 modules | 2-5 modules | 3-8 modules |
| Baseline source behavior | Reads many likely files | Reads module trees | Reads broad folders or repo bundles |
| Baseline command behavior | Raw command output | Raw noisy test/diff output | Raw logs, broad diffs, large suites |
| Template behavior | Reads routed context and likely targets; compresses noisy command output when RTK is available |

## Token Savings

### Source Context

| Scenario | Baseline source context | Template source context | Estimated savings |
| --- | ---: | ---: | ---: |
| Small bug fix | 25k-60k tokens | 8k-20k tokens | 40%-70% |
| Medium feature change | 80k-180k tokens | 20k-55k tokens | 60%-80% |
| Cross-module refactor | 150k-400k tokens | 45k-120k tokens | 55%-75% |
| Onboarding / architecture question | 100k-300k tokens | 25k-90k tokens | 50%-75% |
| External whole-repo review | 250k+ tokens | No major savings if a full Repomix export is required | 0%-20% |

Expected average across normal coding tasks: **50%-75% fewer source-context input tokens**.

### Command Output

RTK savings vary more by workflow than source savings. A task with one clean unit test may save very little. A task with repeated test failures, large diffs, or broad lint output can save a lot.

| Command/output type | Raw output pattern | With RTK or compact wrappers | Estimated savings |
| --- | ---: | ---: | ---: |
| `git status` / `git diff` | Full status and patch context | Condensed file/change summary | 30%-70% |
| Search output | Many matches and paths | Ranked or reduced matches | 30%-75% |
| Passing tests | Full runner output | Short pass summary | 40%-80% |
| Failing tests | Full trace/log output | Actionable failure sections preserved | 20%-60% |
| Lint/typecheck | Long issue lists | Compact actionable diagnostics | 30%-70% |
| Runtime logs | Large raw log blocks | Filtered relevant sections | 40%-85% |

Expected average across command-heavy coding tasks: **25%-60% fewer command-output tokens**.

### Combined Context Impact

For a typical implementation task, assume:

- 70%-85% of input context is source/docs.
- 15%-30% of input context is command output.
- Progressive retrieval saves 50%-75% of source/docs context.
- RTK saves 25%-60% of command-output context when available.

That yields a practical combined estimate of **45%-75% fewer routine input tokens** across normal agent-assisted coding tasks.

For a team doing 100 agent-assisted coding tasks per month, with a baseline of 100k input tokens per task:

| Savings rate | Monthly input context after template | Tokens saved/month |
| --- | ---: | ---: |
| 45% | 5.5M tokens | 4.5M tokens |
| 60% | 4.0M tokens | 6.0M tokens |
| 75% | 2.5M tokens | 7.5M tokens |

## Time Savings

| Activity | Baseline | With template + RTK | Estimated savings |
| --- | ---: | ---: | ---: |
| Initial repo orientation per task | 5-20 min | 1-5 min | 50%-80% |
| Finding relevant files | 5-30 min | 2-8 min | 40%-75% |
| Inspecting git diff/status | 2-10 min | 1-4 min | 30%-60% |
| Confirming related tests | 3-15 min | 1-5 min | 40%-70% |
| Diagnosing test/lint/typecheck output | 5-30 min | 2-12 min | 30%-65% |
| Reviewing agent context choices | 5-15 min | 2-6 min | 40%-60% |
| New contributor/agent onboarding | 2-8 hr | 30-90 min | 50%-85% |

Expected average for normal implementation tasks: **10-50 minutes saved per task**, depending on repo size, command noise, and ambiguity.

For 100 tasks per month, that is roughly **17-83 engineering hours saved per month**.

## Cost Savings Model

Use this formula:

```txt
monthly_token_savings =
  tasks_per_month
  * baseline_input_tokens_per_task
  * combined_savings_rate
```

Example:

```txt
100 tasks/month * 100,000 input tokens/task * 0.60 savings
= 6,000,000 input tokens saved/month
```

If input tokens cost `C` dollars per million tokens:

```txt
monthly_cost_savings = 6 * C
```

This excludes secondary savings from fewer retries, fewer wrong-file edits, shorter review cycles, reduced output tokens, and less human time spent reading noisy command output.

## Other Quantitative Benefits

| Benefit | Estimated impact |
| --- | ---: |
| Fewer irrelevant files read by agents | 50%-80% reduction |
| Less noisy command output in context | 25%-60% reduction on command-heavy tasks |
| Faster first useful patch | 30%-70% faster |
| Fewer wrong-file edits | 20%-50% reduction |
| Fewer "where is this implemented?" loops | 40%-70% reduction |
| Faster test selection | 30%-60% faster |
| Faster failure triage | 25%-60% faster |
| Lower context-window pressure | 45%-75% less routine context load |
| Better handoff quality | 25%-50% fewer missing-context handoffs |
| Lower chance of stale generated context being trusted blindly | Improved by explicit risk notes and validation checks |

## Why The Savings Happen

- `INDEX.md` routes the task to the smallest relevant context.
- `CODEMAP.md` gives a quick generated map of files, symbols, APIs, dependencies, tests, and risk notes.
- Module cards preserve ownership and pitfalls without reading full architecture docs.
- Semble finds behavior-level matches without knowing exact symbol names.
- `rg` confirms exact strings and paths cheaply.
- Serena is optional, so projects only pay the setup cost when language-server semantics are valuable.
- RTK compresses noisy terminal output while preserving actionable failures.
- Compact make targets keep command-output behavior discoverable for agents.
- Raw reruns remain available for exact failures, security review, and generated artifact verification.
- Repomix is kept out of the daily workflow, avoiding large bundled context by default.

## Measurement Plan

Track these metrics for 20-50 real tasks before and after installing the template:

| Metric | How to collect |
| --- | --- |
| Files read before first edit | Agent transcript or task trace |
| Input tokens per task | Model/provider usage logs |
| Command-output tokens per task | Agent transcript or RTK gain report |
| Time from task start to first patch | Task timestamps |
| Time from task start to accepted patch | Task timestamps |
| Search commands used | Agent transcript |
| Test commands used | Task handoff / logs |
| RTK used vs raw reruns | Command summary or task log |
| Wrong-file or reverted edits | Review notes |
| Missing-context review comments | PR comments |

Run retrieval checks with:

```bash
make retrieval-eval
```

Check RTK savings with:

```bash
make rtk-gain
```

Use the results to tune `docs/agent/CODEMAP.md`, module cards, `.sembleignore`, retrieval fixtures, compact make targets, and RTK command-output rules.

## Conservative Summary

For day-to-day agent-assisted coding, this template should reasonably save:

- **45%-75% routine input tokens overall**
- **50%-75% source/docs input tokens**
- **25%-60% command-output tokens on command-heavy tasks**
- **10-50 minutes per normal coding task**
- **17-83 engineering hours per 100 tasks**
- **30%-70% faster file discovery**
- **20%-50% fewer wrong-context edits**

The largest gains come from medium and large repositories where agents otherwise read broad folders, bundled repo maps, raw diffs, full test output, and unrelated logs before editing.
