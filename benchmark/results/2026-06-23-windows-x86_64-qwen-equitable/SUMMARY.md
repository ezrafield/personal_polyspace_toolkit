# Equitable Benchmark Summary: Windows x86-64, 2026-06-23

This run adds an LLM guidance quality axis — evaluated by Qwen — to the existing deterministic Tier 1 results. The two prior runs excluded Qwen by request and tested the original's PowerShell script without a language model, which penalised a toolkit designed for agent-driven workflows. Including Qwen gives the original a fair chance to demonstrate its documentation quality alongside the candidate's executable guarantees.

## Revisions And Environment

| Item | Value |
| --- | --- |
| Original | `cc15b840e80bf5187963d13ed86c4c5bb86381ad` |
| Candidate head | `714effe1aee819032ee212b6d6bf047208153b54` |
| Platform | Windows x86-64, Windows PowerShell `5.1.26100.8655` |
| Python | `Python 3.14.5` |
| Qwen endpoint | `http://10.134.198.10:8336/v1` |
| Qwen model | `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| Qwen temperature | `0.2` |
| MCP asset | `v1.1.1` (from prior run) |
| Polyspace | Not installed |
| Prior deterministic run | `2026-06-23-windows-x86_64-no-qwen` |

## Methodology

Each of the 12 Tier 1 scenarios is scored on two axes, weighted equally at 50% each:

- **Deterministic (50%)** — binary PASS/FAIL carried from the 2026-06-23 Codex-only run. Candidate: 12/12 PASS. Original: 0/12 (4 FAIL, 8 NOT_IMPLEMENTED). No scenario is re-run in this report.
- **LLM guidance quality (50%)** — Qwen evaluates each toolkit's documentation for the scenario and scores it on four dimensions (Accuracy, Safety, Completeness, Actionability), each 0–4, totalling 0–16 per scenario.

Combined score per scenario = `0.5 × deterministic + 0.5 × (guidance_total / 16)`. A score of 1.0 means both axes are perfect; 0.0 means both axes failed completely. This gives the original credit where its documentation is strong while honestly reporting the gap in executable deterministic behavior.

## Tier 1: Deterministic Behavior (carried from 2026-06-23 no-Qwen run)

| ID | Scenario | Candidate | Original |
| --- | --- | --- | --- |
| S01 | Clean install | PASS | FAIL |
| S02 | Dry run | PASS | NOT_IMPLEMENTED |
| S03 | Idempotent setup | PASS | NOT_IMPLEMENTED |
| S04 | Unknown registration | PASS | NOT_IMPLEMENTED |
| S05 | Existing skill directory | PASS | FAIL |
| S06 | Failed download/digest | PASS | NOT_IMPLEMENTED |
| S07 | Atomic failure | PASS | NOT_IMPLEMENTED |
| S08 | Safe uninstall | PASS | NOT_IMPLEMENTED |
| S09 | Version gate | PASS | NOT_IMPLEMENTED |
| S10 | Telemetry default | PASS | FAIL |
| S11 | OS protection | PASS | FAIL |
| S12 | Project validation | PASS | NOT_IMPLEMENTED |

Source: [2026-06-23-windows-x86_64-no-qwen/SUMMARY.md](../2026-06-23-windows-x86_64-no-qwen/SUMMARY.md)

## LLM Guidance Quality via Qwen

Qwen scored each toolkit's per-scenario documentation on four dimensions (each 0–4). Max per scenario: 16.

| ID | Scenario | Original /16 | Candidate /16 | Winner |
| --- | --- | ---: | ---: | --- |
| S01 | Clean install | 14 | 16 | Candidate |
| S02 | Dry run | 14 | 16 | Candidate |
| S03 | Idempotent setup | 12 | 13 | Candidate |
| S04 | Unknown registration | 13 | 15 | Candidate |
| S05 | Existing skill directory | 14 | 13 | Original |
| S06 | Failed download/digest | 13 | 13 | Tie |
| S07 | Atomic failure | 12 | 10 | Original |
| S08 | Safe uninstall | 10 | 15 | Candidate |
| S09 | Version gate | 14 | 16 | Candidate |
| S10 | Telemetry default | 15 | 10 | Original |
| S11 | OS protection | 16 | 16 | Tie |
| S12 | Project validation | 12 | 16 | Candidate |
| **Total** | | **159/192** | **169/192** | |

## Equitable Combined Score

Combined = `0.5 × deterministic_binary + 0.5 × (guidance_total / 16)` per scenario. Values range 0.00–1.00.

| ID | Scenario | Candidate | Original |
| --- | --- | ---: | ---: |
| S01 | Clean install | 1.00 | 0.44 |
| S02 | Dry run | 1.00 | 0.44 |
| S03 | Idempotent setup | 0.91 | 0.38 |
| S04 | Unknown registration | 0.97 | 0.41 |
| S05 | Existing skill directory | 0.91 | 0.44 |
| S06 | Failed download/digest | 0.91 | 0.41 |
| S07 | Atomic failure | 0.81 | 0.38 |
| S08 | Safe uninstall | 0.97 | 0.31 |
| S09 | Version gate | 1.00 | 0.44 |
| S10 | Telemetry default | 0.81 | 0.47 |
| S11 | OS protection | 1.00 | 0.50 |
| S12 | Project validation | 1.00 | 0.38 |
| **Total** | | **11.28/12** | **4.97/12** |

Candidate combined: **11.28 / 12** (94.0%). Original combined: **4.97 / 12** (41.4%).

The equitable framing narrows the gap on scenarios where the original's documentation gives an LLM enough information to guide a developer correctly (e.g., S04 unknown registration, S09 version gate). The gap remains structural where the original has documented behavioral failures (S01, S05, S10, S11) or provides no mechanism at all (S06 digest, S07 rollback, S08 uninstall) — no documentation quality score can substitute for an absent executable implementation.

## Scope Limits

| Item | Status | Reason |
| --- | --- | --- |
| Claude | N/A | Codex-only client scope for this run |
| Tier 2 Polyspace workflows | BLOCKED | No licensed Polyspace installation or C analyzer oracle |
| Tier 3 licensed smoke | BLOCKED | No `POLYSPACE_ROOT` or checker file |
| Linux/macOS cells | NOT_RUN | This run is Windows-only |
| Weighted Tier 1+2+3 total | NOT_REPORTED | Correctness and workflow measurements from Tiers 2 and 3 are missing |

No overall weighted score from the full BENCHMARK.md protocol is reported because licensed Polyspace workflow tiers remain unscored. Within the completed equitable scope, the candidate leads on both axes: it is executable and verified (deterministic axis), and its documentation provides immediately actionable guidance (LLM quality axis).
