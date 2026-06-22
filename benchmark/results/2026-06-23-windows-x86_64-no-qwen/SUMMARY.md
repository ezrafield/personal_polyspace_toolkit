# Codex-Only Benchmark Summary: Windows x86-64, 2026-06-23

This run compares the original and candidate without Qwen. Qwen is `N/A` by request and is not a
dependency, blocker, score input, or executed client. Codex is the only client in scope.

## Revisions And Environment

| Item | Value |
| --- | --- |
| Original | `cc15b840e80bf5187963d13ed86c4c5bb86381ad` |
| Candidate base | `85f45bbbc3383e071e3c31d730f3f25ffc7143ab` plus the recorded dirty snapshot |
| Candidate snapshot | `094f35f1e5f7a431a36689e074584dd732d875e04562012d13af526694cd6799` |
| Platform | Windows x86-64, Windows PowerShell `5.1.26100.8655` |
| Python | `3.14.5` |
| Client | Codex CLI `0.142.0-alpha.6` |
| MCP asset | `v1.1.1`, SHA-256 `affe106247b5a1830b02379afa07738a203523bfd51bf3d3404ae3b8af1b257e` |
| Qwen | `N/A`, intentionally excluded |
| Polyspace | Not installed |

All setup mutations ran under fresh temporary user homes. The candidate snapshot digest covers the
base commit, worktree status, and present tracked/untracked product files while excluding benchmark
result directories.

## Results

| Measurement | Candidate | Original |
| --- | --- | --- |
| Tier 1 deterministic scenarios | **12 PASS / 12** | **0 PASS / 12** |
| Tier 1 failures | 0 | 4 |
| Tier 1 not implemented | 0 | 8 |
| Repository tests | **41 passed** | No tests; pytest exit 5 |
| Focused non-Qwen Tier 1 tests | **34 passed** | No test implementation |
| Real MCP download and digest | PASS | NOT_IMPLEMENTED |
| Live Codex registration parse | **PASS** | Not reached; installer failed first |
| Dry-run mutation count | 0 | NOT_IMPLEMENTED |
| Setup rerun | Byte-identical | NOT_IMPLEMENTED as a full setup operation |
| Safe uninstall | PASS | NOT_IMPLEMENTED |
| Ruff / mypy / product / docs | PASS | No equivalent checks |

The Tier 1 status mapping is unchanged from the 2026-06-22 run:

- Candidate passes S01-S12.
- Original fails S01, S05, S10, and S11.
- Original has no deterministic implementation for S02-S04, S06-S09, and S12.

`NOT_IMPLEMENTED` means the original delegates the behavior to prompt guidance or has no operation;
it is distinct from an observed behavioral failure.

## Live Codex Evidence

The candidate completed a real setup in 8.995 seconds, including download and digest verification.
Codex then loaded `polyspace` as an enabled stdio MCP server and reported:

- the expected absolute binary command;
- `--disable-telemetry=true`;
- `WINDIR` forwarding;
- a 600-second tool timeout.

The subsequent setup produced the same sandbox tree hash. Verification confirmed the binary,
digest, and Codex registration; overall readiness remained false because Polyspace was absent.
Uninstall removed the owned binary, registration, and all installed skills. Codex emitted a benign
warning that it would not create PATH aliases under a temporary directory, but returned exit 0 and
successfully parsed the MCP registration.

The original Windows installer again failed at its `Join-Path $HOME ".agents" "skills"` call under
its documented Windows PowerShell invocation. It installed zero skills, no MCP binary, and no Codex
configuration. Its documented release API URL also returned HTTP 404 while the actual MathWorks
repository URL returned HTTP 200.

## Scope Limits

| Item | Status | Reason |
| --- | --- | --- |
| Qwen | N/A | Explicitly excluded from this benchmark |
| Claude | N/A | Codex-only client scope |
| Tier 2 Polyspace workflows | BLOCKED | No licensed Polyspace installation or C analyzer oracle |
| Tier 3 licensed smoke | BLOCKED | No `POLYSPACE_ROOT` or checker file |
| Linux/macOS cells | NOT_RUN | This run is Windows-only |

No overall weighted score is reported because analyzer correctness is unmeasured. Within the
completed Codex-only deterministic scope, the candidate is the clear winner: it is executable,
verified, reversible, and accepted by the live Codex CLI without using Qwen.
