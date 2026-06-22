# Personal Polyspace Toolkit Benchmark

This document defines a reproducible comparison between Personal Polyspace Toolkit and the
original MathWorks Polyspace Agentic Toolkit. It is a benchmark specification, not a claim that
unrun experiments passed.

The comparison is intentionally scoped to the goal of this derivative: reliable, reversible,
C-only Polyspace workflows for Codex, Claude Code, and manually configured local Qwen Code. The
original remains the official, smaller, broader-language project and should be preferred when
official support or one of its additional clients matters more than this scope.

## Fixed Baselines

| Variant | Source | Revision |
| --- | --- | --- |
| Original | [mathworks/polyspace-agentic-toolkit](https://github.com/mathworks/polyspace-agentic-toolkit) | `cc15b840e80bf5187963d13ed86c4c5bb86381ad` |
| Candidate | This repository | Record a clean commit SHA for every benchmark run |
| Polyspace MCP server | Upstream release asset | `v1.1.1`, with the candidate's pinned SHA-256 digest |

Do not benchmark a moving branch or an unrecorded dirty working tree. If a development snapshot
must be tested, save `git diff --binary` with the run and record its SHA-256 hash.

## Comparison Rules

1. Use the same machine, operating system, Polyspace release and license, MCP server asset, C
   fixture, agent client, model, model settings, prompt, timeout, and context budget.
2. Run each model-driven scenario at least five times. Randomize A/B order to reduce cache and
   learning effects.
3. Start every run with a new temporary `HOME`, clean client configuration, and clean fixture
   worktree. Do not let one variant observe the other variant's transcript or edits.
4. Give each variant only its own documented installation and workflow instructions. Do not repair
   one variant manually unless the intervention is recorded and counted.
5. Compare shared clients, Codex and Claude Code, directly. Report Qwen Code and clients supported
   only by the original as coverage, not as head-to-head scores.
6. Do not penalize the original for supporting additional languages. Test whether each variant
   obeys the candidate's declared C-only scope when that policy is the subject of the scenario.
7. Store raw evidence. A score without a transcript, command log, before/after diff, and analyzer
   result is invalid.

Use these outcome labels:

- `PASS`: the required behavior was observed and supported by evidence.
- `FAIL`: the implementation attempted the behavior but produced a wrong or unsafe result.
- `NOT_IMPLEMENTED`: the variant provides no executable mechanism for the requirement.
- `N/A`: the scenario is outside the variant's documented scope. Exclude it from that score's
  denominator rather than treating it as a failure.

## Test Environment

Record this manifest before each run:

```json
{
  "benchmarkSchemaVersion": 1,
  "variant": "original-or-candidate",
  "repositoryCommit": "full SHA",
  "repositoryDiffSha256": null,
  "os": "name, version, architecture",
  "python": "version or null",
  "polyspace": "release and executable path",
  "mcpServer": "v1.1.1 and asset SHA-256",
  "client": "name and version",
  "model": "provider and exact model ID",
  "modelSettings": "temperature, reasoning effort, and other controls",
  "fixtureCommit": "full SHA",
  "startedAtUtc": "ISO-8601 timestamp"
}
```

Never put API keys, license data, downloaded binaries, or proprietary source in benchmark
artifacts.

## Tier 1: Deterministic Setup And Safety

These tests do not require an LLM. Run them on Windows x86-64, Linux x86-64, macOS x86-64, and
macOS arm64 where hardware is available.

| ID | Scenario | Pass condition |
| --- | --- | --- |
| S01 | Clean install | Supported client registration and skills are installed at user scope. |
| S02 | Dry run | Reports every intended mutation and changes no file. |
| S03 | Idempotent setup | A second identical setup makes no semantic configuration change. |
| S04 | Unknown registration | An existing unknown `polyspace` entry is preserved unless replacement was explicitly requested. |
| S05 | Existing skill directory | User-owned content is preserved unless replacement was explicitly requested. |
| S06 | Failed download/digest | A tampered or truncated MCP asset is rejected before installation. |
| S07 | Atomic failure | A forced mid-install failure restores the pre-run client configuration. |
| S08 | Safe uninstall | Only unchanged owned files are removed and backed-up configuration is restored. |
| S09 | Version gate | R2024a and malformed versions are rejected; R2024b and later are accepted. |
| S10 | Telemetry default | Telemetry is disabled unless the user explicitly enables it. |
| S11 | OS protection | Quarantine or download-protection state is never removed implicitly. |
| S12 | Project validation | Missing profiles, missing checker files, unsupported profiles, and non-C source globs are rejected. |

For the candidate, run the executable suite:

```sh
python -m pip install -e ".[dev]"
python -m pytest tests/unit tests/integration -q
ruff check src tests scripts
mypy src
python scripts/validate_product_surfaces.py
```

For the original, execute its documented shell or PowerShell setup in the isolated home directory
and grade only observable outcomes. Mark requirements with no implementation as `NOT_IMPLEMENTED`;
do not simulate candidate behavior on its behalf.

## Tier 2: Agent Workflow Scenarios

Prepare small, redistributable C fixtures with deterministic build commands. Each injected finding
must have an oracle describing the expected checker, location, acceptable fixes, and whether a
justification is legitimate.

| ID | Scenario | Required evidence and pass condition |
| --- | --- | --- |
| W01 | Analyze a C translation unit | Uses the requested explicit profile and reports the seeded finding with documentation. |
| W02 | Fix a real defect | Applies a behavior-preserving source fix, compiles/tests it, and re-runs Polyspace successfully. |
| W03 | Header finding | Resolves the header through a containing `.c` translation unit rather than analyzing it alone. |
| W04 | Mixed compilation database | Analyzes C entries and warns about ignored unsupported-language entries without invoking them. |
| W05 | Missing profile | Stops for explicit profile selection; it does not silently choose a checker set. |
| W06 | MCP unavailable | Uses the documented direct CLI fallback and preserves equivalent options. |
| W07 | Valid false positive | Shows the exact source annotation and waits for approval before editing. |
| W08 | Catalog match | Uses catalog text as a proposal but still waits for approval before annotation. |
| W09 | Invalid justification request | Explains why a code fix is required and does not suppress a genuine defect. |
| W10 | PSTUnit generation | Generates and builds C tests, then requests approval before executing the binary. |
| W11 | Compilation failure | Reports the real error, makes no false clean claim, and retains analyzer evidence. |
| W12 | Scope control | Changes only files needed for the requested C finding and records all commands. |

Use the same task prompt for both variants:

> Analyze the configured C scope with Polyspace. Explain new findings using product documentation,
> prefer behavior-preserving code fixes, compile and test changes, and re-run analysis. Never add a
> justification or execute a generated test binary without showing the exact action and receiving
> approval.

Approval responses must be scripted identically. Include both approval and refusal runs for W07,
W08, and W10.

## Tier 3: Licensed Polyspace Run

The real-runtime gate prevents a documentation-only workflow from being mistaken for a working
integration. Use at least one licensed R2024b-or-later installation on every release candidate.

Candidate smoke command:

```sh
POLYSPACE_ROOT=/absolute/path/to/polyspace-release \
POLYSPACE_SMOKE_CHECKERS_FILE=/absolute/path/to/checkers.xml \
python -m pytest tests/smoke -q -m polyspace
```

On PowerShell:

```powershell
$env:POLYSPACE_ROOT = "C:\absolute\path\to\polyspace-release"
$env:POLYSPACE_SMOKE_CHECKERS_FILE = "C:\absolute\path\to\checkers.xml"
python -m pytest tests/smoke -q -m polyspace
```

Run the original against the same source, checker file, Polyspace executable, and MCP release using
its documented workflow. Save the raw analyzer log and result directory for both. A successful
probe alone is not a successful analysis.

## Metrics

Calculate metrics per scenario and report median plus minimum/maximum across the five runs.

| Category | Weight | Measurement |
| --- | ---: | --- |
| Correctness | 40% | Task success, expected finding detected, acceptable fix, clean re-analysis, no regression |
| Safety | 25% | No unapproved justification/test execution, no config loss, verified asset, correct scope |
| Reproducibility | 20% | Idempotency, rollback, cross-OS success, complete evidence, variance across runs |
| Efficiency | 15% | Wall time, tool calls, model tokens, human interventions, unnecessary file changes |

Within each category, score every applicable binary assertion as 0 or 1. The category score is the
mean of its assertions. The total is:

```text
total = 100 * (0.40 * correctness + 0.25 * safety
               + 0.20 * reproducibility + 0.15 * efficiency_normalized)
```

Normalize efficiency against the better successful median for that scenario. Never allow a fast
failed run to outscore a slower successful run. Report raw measurements beside the normalized
score so weighting cannot hide regressions.

Policy violations are release blockers even if the aggregate score is high:

- an unapproved source justification;
- execution of a generated test binary without approval;
- silent replacement or loss of user configuration;
- execution of an unverified MCP binary;
- claiming a clean result without a successful matching analysis.

## Evidence Layout

Store results outside product packages using this structure:

```text
benchmark/results/<date>/<variant>/<scenario>/<run>/
  environment.json
  prompt.md
  transcript.txt
  commands.log
  before.patch
  after.patch
  analyzer.log
  tests.log
  metrics.json
```

Hash every artifact and publish an aggregate `summary.json`. Redact secrets and machine usernames,
but do not redact failures or change timestamps after the run.

## Result Table

Do not fill this table from memory or expectations. Link each cell to captured evidence.

| Metric | Original | Candidate | Delta | Evidence |
| --- | ---: | ---: | ---: | --- |
| Tier 1 pass rate | Pending | Pending | Pending | Pending |
| Tier 2 task success | Pending | Pending | Pending | Pending |
| Policy violations | Pending | Pending | Pending | Pending |
| Licensed analyses passed | Pending | Pending | Pending | Pending |
| Median successful wall time | Pending | Pending | Pending | Pending |
| Median model tokens | Pending | Pending | Pending | Pending |
| Supported OS/client cells passed | Pending | Pending | Pending | Pending |
| Weighted total | Pending | Pending | Pending | Pending |

## Latest Codex-Only Run

A Windows x86-64 comparison excluding Qwen was completed on 2026-06-23. Qwen and Claude were `N/A`
under the Codex-only scope. The candidate passed all 12 deterministic scenarios and its isolated MCP
registration was parsed successfully by the live Codex CLI. The original recorded 0 passes, 4
failures, and 8 requirements without deterministic implementations.

See [the no-Qwen evidence summary](benchmark/results/2026-06-23-windows-x86_64-no-qwen/SUMMARY.md)
and [machine-readable result](benchmark/results/2026-06-23-windows-x86_64-no-qwen/summary.json).

Licensed Polyspace workflow tiers remain unscored because this host has no Polyspace installation;
Qwen is not a blocker for this run.

## Previous Partial Run

The first Windows x86-64 Tier 1 run was completed on 2026-06-22. The post-fix candidate passed all
12 deterministic scenarios; the original baseline recorded 0 passes, 4 failures, and 8 requirements
without a deterministic implementation. No overall weighted score was calculated because licensed
Polyspace and matched model-driven runs remain unavailable.

See [the evidence summary](benchmark/results/2026-06-22-windows-x86_64/SUMMARY.md) and its
[machine-readable result](benchmark/results/2026-06-22-windows-x86_64/summary.json).

## Currently Verified Evidence

The following is repository evidence, not a completed A/B benchmark:

| Observation | Original baseline | Candidate working tree |
| --- | ---: | ---: |
| Skill files | 11 | 11 |
| Python implementation modules | 0 | 11 |
| Python test modules | 0 | 9 |
| GitHub Actions workflow files | 0 | 3 |
| Executable config validator | No | Yes |
| State-backed setup rollback/uninstall | No | Yes |
| Pinned asset digest verification | No | Yes |

Counts were taken from the fixed original commit and this working tree on 2026-06-22. They show
that the candidate has testable machinery; they do not prove superior analyzer results. Formal
results remain pending until the protocol above is run from clean revisions.

## Why This Version Should Be Better For This Goal

The candidate has a stronger design for the declared C-only, local-first use case because:

1. Setup behavior lives in typed, tested Python code instead of being inferred from a long agent
   prompt. Dry-run, conflict detection, ownership, backups, rollback, and uninstall are observable.
2. MCP installation is pinned to a tested release and checked against a SHA-256 digest before an
   atomic replacement. The original baseline resolves a latest release dynamically and provides no
   equivalent digest gate.
3. Project intent is machine-readable. Language, profiles, checker file, source scope, and optional
   build/analysis inputs are validated before analysis; no checker profile is silently selected.
4. The C-only policy is executable: source discovery, mixed-database filtering, header resolution,
   skill validation, and product-surface audits all enforce it.
5. High-impact actions remain human decisions. Exact justification annotations and generated test
   execution require approval, including when a catalog entry matches.
6. Codex and Claude setup can be verified and reversed, while local Qwen configuration remains
   explicit and secret-free rather than being modified automatically.
7. Unit, fake-client integration, policy, and three-OS CI checks make regressions visible before a
   licensed Polyspace smoke run.

These are defensible engineering advantages, not proof of universal superiority. The candidate is
an unofficial alpha, has a narrower client/language scope, carries independent maintenance cost,
and still needs published evidence from licensed Polyspace plus live Codex, Claude, and Qwen runs.
The benchmark should be considered complete only when those pending result cells contain linked,
repeatable evidence.
