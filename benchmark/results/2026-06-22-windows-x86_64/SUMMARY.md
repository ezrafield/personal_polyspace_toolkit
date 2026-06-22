# Benchmark Summary: Windows x86-64, 2026-06-22

This is a partial benchmark run under the protocol in `BENCHMARK.md`. Tier 1 deterministic setup
and safety checks were run. Model-driven Polyspace workflows and licensed analysis were not run
because this host has no Polyspace installation, Claude Code, Qwen Code, or configured Qwen model
endpoint.

## Revisions

| Variant | Revision |
| --- | --- |
| Original | `cc15b840e80bf5187963d13ed86c4c5bb86381ad` |
| Candidate | Dirty tree based on `85f45bbbc3383e071e3c31d730f3f25ffc7143ab` |
| Candidate post-fix snapshot | `92ab6e5bc824fe1de7a54bd96e799094d0a42d612873bd58ecfa197b98c86d20` |
| MCP asset | `v1.1.1` Windows x86-64, SHA-256 `affe106247b5a1830b02379afa07738a203523bfd51bf3d3404ae3b8af1b257e` |

The snapshot digest covers the base commit, worktree status, and hashes of all present tracked and
untracked product files, excluding this results directory.

## Environment

- Windows x86-64 with Windows PowerShell `5.1.26100.8655`
- Python `3.14.5`
- Codex CLI `0.142.0-alpha.6`
- Polyspace, Claude Code, and Qwen Code not found
- Every setup mutation ran in a new temporary user home

## Tier 1 Results

| ID | Candidate | Original | Evidence / note |
| --- | --- | --- | --- |
| S01 Clean install | PASS | FAIL | Candidate completed a real verified download and Codex install. The original Windows script exited before installing anything because its documented Windows PowerShell invocation uses an unsupported `Join-Path` form. |
| S02 Dry run | PASS | NOT_IMPLEMENTED | Candidate made zero sandbox mutations. The original has no deterministic dry-run command. |
| S03 Idempotent setup | PASS | NOT_IMPLEMENTED | Candidate sandbox tree hash was unchanged after setup rerun. The original has no executable full setup operation to rerun. |
| S04 Unknown registration | PASS | NOT_IMPLEMENTED | Candidate returned exit 2, preserved the user TOML hash, and rolled back all copied skills. Original behavior is delegated to an agent prompt. |
| S05 Existing skill | PASS | FAIL | Candidate returned exit 2 and preserved the only user skill. Original script unconditionally removes an existing destination before linking. |
| S06 Digest failure | PASS | NOT_IMPLEMENTED | Candidate test proves tampered content is rejected while the previous binary survives. Original setup has no digest gate. |
| S07 Atomic failure | PASS | NOT_IMPLEMENTED | Candidate binary-probe rollback, registration rollback, and post-fix collision preflight passed. Original has no state-backed rollback. |
| S08 Safe uninstall | PASS | NOT_IMPLEMENTED | Candidate removed only its binary, MCP registration, and 11 owned skills. Original has no uninstall operation. |
| S09 Version gate | PASS | NOT_IMPLEMENTED | Candidate executable tests reject R2024a and accept R2024b and later. Original expresses this only as prompt guidance. |
| S10 Telemetry default | PASS | FAIL | Candidate installed `--disable-telemetry=true`. Original setup does not disable telemetry by default. |
| S11 OS protection | PASS | FAIL | Candidate active surfaces contain no protection-removal command. Original directs Windows setup to run `Unblock-File` automatically. |
| S12 Project validation | PASS | NOT_IMPLEMENTED | Candidate CLI accepted the valid example and rejected empty profiles. Original has no versioned project-config validator. |

Tier 1 score by all declared scenarios:

- Candidate: **12 PASS, 0 FAIL, 0 NOT_IMPLEMENTED (12/12)**
- Original: **0 PASS, 4 FAIL, 8 NOT_IMPLEMENTED (0/12)**

`NOT_IMPLEMENTED` is not presented as a behavioral failure. It identifies requirements for which
the original offers no deterministic mechanism; the original may still attempt some of them when
an LLM interprets its setup skill.

## Defect Found And Fixed

The first candidate collision run preserved the user-owned skill but left nine earlier skills
behind after reporting failure. Evidence remains in `candidate-s05-metrics.json`. The installer now
preflights every skill collision before copying any skill, and the integration test asserts that
only the original user directory remains. The post-fix real run and focused test pass; see
`candidate-s05-postfix-metrics.json` and `candidate-postfix-targeted-tests.log`.

## Other Observations

- Candidate unit/integration suite: **41 passed**.
- Candidate Ruff, mypy, product-surface, and documentation checks passed.
- Original test discovery: **no tests**, pytest exit 5.
- Original documented release API URL returned HTTP 404; the actual MathWorks repository URL
  returned HTTP 200 during this run.
- Candidate clean post-fix setup took 9.900 seconds including the real MCP download. The idempotent
  rerun did not download or alter the sandbox tree.
- Candidate verification confirmed binary, digest, and Codex registration. Overall readiness was
  correctly false because Polyspace was absent.

## Unfinished Tiers

| Tier | Status | Blocking input |
| --- | --- | --- |
| Tier 2 agent workflows | BLOCKED | Same-client/model repeated runs plus a licensed Polyspace installation and C fixture oracle |
| Tier 3 licensed smoke | BLOCKED | `POLYSPACE_ROOT` and a real checker file |
| Claude comparison | BLOCKED | Claude Code CLI |
| Qwen coverage | BLOCKED | Qwen Code CLI, local base URL, model ID, and configured credential environment variable |
| Cross-OS matrix | BLOCKED | Linux and macOS hosts/runners |

No weighted total is reported because correctness and workflow measurements from Tiers 2 and 3
are missing. The completed evidence supports a narrower conclusion: on this Windows host, the
candidate is materially safer and more reproducible for deterministic setup than the original
baseline.
