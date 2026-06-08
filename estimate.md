# Estimated Benefits

This estimate models how much time, token usage, and rework this template can save by replacing broad repository scanning with progressive context loading:

1. `AGENTS.md` / `CLAUDE.md`
2. `docs/agent/INDEX.md`
3. `docs/agent/CODEMAP.md`
4. Relevant module cards
5. Semble natural-language search
6. `rg` exact confirmation
7. Optional Serena symbol navigation
8. Targeted tests before broad tests

These are directional estimates, not guaranteed benchmark results. Measure your own project with the retrieval evals and task traces once the template is installed.

## Assumptions

| Factor | Small repo | Medium repo | Large repo |
| --- | ---: | ---: | ---: |
| Source files | 50-150 | 150-800 | 800-3,000 |
| Average file size | 150-300 lines | 150-350 lines | 150-400 lines |
| Typical task scope | 1-3 modules | 2-5 modules | 3-8 modules |
| Baseline agent behavior | Reads many likely files | Reads module trees | Reads broad folders or repo bundles |
| Template behavior | Reads index, CODEMAP, module cards, search hits, and exact source files |

## Token Savings

| Scenario | Baseline context | Template context | Estimated savings |
| --- | ---: | ---: | ---: |
| Small bug fix | 25k-60k tokens | 8k-20k tokens | 40%-70% |
| Medium feature change | 80k-180k tokens | 20k-55k tokens | 60%-80% |
| Cross-module refactor | 150k-400k tokens | 45k-120k tokens | 55%-75% |
| Onboarding / architecture question | 100k-300k tokens | 25k-90k tokens | 50%-75% |
| External whole-repo review | 250k+ tokens | No savings if Repomix export is required | 0%-20% |

Expected average across normal coding tasks: **50%-75% fewer input tokens**.

For a team doing 100 agent-assisted coding tasks per month, with a baseline of 100k input tokens per task, this template could reduce monthly input context from about **10M tokens** to **2.5M-5M tokens**.

## Time Savings

| Activity | Baseline | With template | Estimated savings |
| --- | ---: | ---: | ---: |
| Initial repo orientation per task | 5-20 min | 1-5 min | 50%-80% |
| Finding relevant files | 5-30 min | 2-8 min | 40%-75% |
| Confirming related tests | 3-15 min | 1-5 min | 40%-70% |
| Reviewing agent context choices | 5-15 min | 2-6 min | 40%-60% |
| New contributor/agent onboarding | 2-8 hr | 30-90 min | 50%-85% |

Expected average for normal implementation tasks: **10-45 minutes saved per task**, depending on repo size and ambiguity.

For 100 tasks per month, that is roughly **17-75 engineering hours saved per month**.

## Cost Savings Model

Use this formula:

```txt
monthly_token_savings =
  tasks_per_month
  * baseline_input_tokens_per_task
  * savings_rate
```

Example:

```txt
100 tasks/month * 100,000 input tokens/task * 0.60 savings
= 6,000,000 input tokens saved/month
```

If an input token costs `C` dollars per million tokens:

```txt
monthly_cost_savings = 6 * C
```

This excludes secondary savings from fewer retries, fewer wrong-file edits, shorter review cycles, and reduced output tokens.

## Other Quantitative Benefits

| Benefit | Estimated impact |
| --- | ---: |
| Fewer irrelevant files read by agents | 50%-80% reduction |
| Faster first useful patch | 30%-70% faster |
| Fewer wrong-file edits | 20%-50% reduction |
| Fewer "where is this implemented?" loops | 40%-70% reduction |
| Faster test selection | 30%-60% faster |
| Lower context-window pressure | 50%-75% less routine context load |
| Better handoff quality | 25%-50% fewer missing-context handoffs |
| Lower chance of stale generated context being trusted blindly | Improved by explicit risk notes and validation checks |

## Why The Savings Happen

- `INDEX.md` routes the task to the smallest relevant context.
- `CODEMAP.md` gives a quick generated map of files, symbols, APIs, dependencies, tests, and risk notes.
- Module cards preserve ownership and pitfalls without reading full architecture docs.
- Semble finds behavior-level matches without knowing exact symbol names.
- `rg` confirms exact strings and paths cheaply.
- Serena is optional, so projects only pay the setup cost when language-server semantics are valuable.
- Repomix is kept out of the daily workflow, avoiding large bundled context by default.

## Measurement Plan

Track these metrics for 20-50 real tasks before and after installing the template:

| Metric | How to collect |
| --- | --- |
| Files read before first edit | Agent transcript or task trace |
| Input tokens per task | Model/provider usage logs |
| Time from task start to first patch | Task timestamps |
| Time from task start to accepted patch | Task timestamps |
| Search commands used | Agent transcript |
| Test commands used | Task handoff / logs |
| Wrong-file or reverted edits | Review notes |
| Missing-context review comments | PR comments |

Run retrieval checks with:

```bash
make retrieval-eval
```

Use the results to tune `docs/agent/CODEMAP.md`, module cards, `.sembleignore`, and the retrieval fixtures.

## Conservative Summary

For day-to-day agent-assisted coding, this template should reasonably save:

- **50%-75% input tokens**
- **10-45 minutes per normal coding task**
- **17-75 engineering hours per 100 tasks**
- **30%-70% faster file discovery**
- **20%-50% fewer wrong-context edits**

The largest gains come from medium and large repositories where agents otherwise read broad folders, bundled repo maps, or unrelated docs before editing.
