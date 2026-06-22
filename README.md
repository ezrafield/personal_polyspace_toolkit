# Personal Polyspace Toolkit

Deterministic, C-only Polyspace workflows for coding agents.

Personal Polyspace Toolkit is an unofficial, independently maintained derivative of the
[MathWorks Polyspace Agentic Toolkit](https://github.com/mathworks/polyspace-agentic-toolkit). It
keeps the useful Polyspace domain workflows, replaces prompt-driven installation with tested
automation, and adds explicit safety boundaries around configuration, justifications, and generated
test execution.

> [!IMPORTANT]
> This project is not an official MathWorks product. Version `0.1.0-alpha.1` is intended for
> evaluation and development. It is licensed solely for use with MathWorks products and services;
> see [LICENSE.md](LICENSE.md) and [NOTICE.md](NOTICE.md).

## At A Glance

| Area | Current scope |
| --- | --- |
| Language | C translation units only |
| Polyspace | Polyspace as You Code R2024b or later |
| Automated clients | OpenAI Codex and Claude Code, user scope |
| Local model client | Qwen Code, manual configuration only |
| MCP server | Tested release `v1.1.1`, pinned by platform and SHA-256 digest |
| Telemetry | Disabled by default |
| Project configuration | Versioned `.polyspace-toolkit.json` with explicit checker profiles |
| Release status | Alpha; licensed Polyspace smoke testing is still pending |

## Why This Exists

The upstream toolkit contains valuable analysis, remediation, documentation, justification, and
PSTUnit guidance. Its setup flow, however, is primarily an agent interpreting Markdown. That makes
installation behavior depend on the client and model performing it.

This derivative moves the risky parts into deterministic Python code:

- previewable setup with `--dry-run`;
- tested release selection and digest-verified downloads;
- conservative client registration that preserves unrelated settings;
- ownership records, backups, rollback, drift detection, and safe uninstall;
- explicit C-only project configuration and source filtering;
- approval gates before source justifications or generated test execution;
- unit and fake-client integration coverage on Windows, Linux, and macOS.

The goal is not to replace official product support. It is to provide a smaller, inspectable toolkit
for the specific C and local-model workflow described here.

## What You Get

### Deterministic Setup CLI

The `polyspace-toolkit` command diagnoses prerequisites, installs the tested MCP server, configures
supported clients, verifies owned state, and uninstalls only what it can prove it owns.

```text
polyspace-toolkit doctor [--json]
polyspace-toolkit setup --client codex|claude [options]
polyspace-toolkit verify --client codex|claude|qwen|all
polyspace-toolkit uninstall --client codex|claude|all
polyspace-toolkit config validate [PATH]
```

### C Compliance Workflow

The canonical skills under [`skills/`](skills/) cover:

- C analysis and configuration resolution;
- finding explanation and documentation lookup;
- behavior-preserving remediation;
- exact, approval-gated justification proposals;
- checker and build-option configuration;
- justification catalog lookup;
- C PSTUnit generation with separate approval before execution.

The five upstream MCP tool names remain unchanged for server compatibility. Direct Polyspace CLI
fallbacks are documented where applicable.

### Machine-Readable Project Contract

Every project selects its own profiles and paths. No checker profile is silently assumed, and
non-C source patterns are rejected before analysis.

## Requirements

- Python 3.11 or later
- Polyspace as You Code R2024b or later
- A licensed, per-user MathWorks installation
- Codex, Claude Code, or manually configured Qwen Code
- Windows x86-64, Linux x86-64, or macOS x86-64/arm64

## Quick Start

Clone the repository to a permanent location. The alpha release installs from a source checkout
because client skill and marketplace metadata resolve assets from that checkout.

```sh
git clone https://github.com/ezrafield/personal_polyspace_toolkit.git
cd personal_polyspace_toolkit
python -m pip install -e ".[dev]"
polyspace-toolkit doctor --json
```

Preview every change before applying it:

```sh
polyspace-toolkit setup --client codex --dry-run
polyspace-toolkit setup --client codex --yes
polyspace-toolkit verify --client codex
```

Configure both automated clients by repeating `--client`:

```sh
polyspace-toolkit setup --client codex --client claude --dry-run
polyspace-toolkit setup --client codex --client claude --yes
polyspace-toolkit verify --client all
```

Setup refuses an unknown existing `polyspace` registration or same-named skill directory. Review
the conflict before using `--replace-existing`. Telemetry remains disabled unless
`--enable-telemetry` is explicitly supplied.

`verify` reports overall readiness as false when no supported Polyspace installation is available,
even if the MCP binary, digest, and client registration are valid.

### Qwen Code

Qwen Code support is intentionally manual. The toolkit does not ship a Qwen extension and never
writes `~/.qwen/settings.json`.

Follow [docs/setup/qwen-local.md](docs/setup/qwen-local.md) to configure:

- an OpenAI-compatible localhost base URL;
- the exact local model ID;
- an API key environment-variable reference;
- the Polyspace stdio MCP server with `trust: false`;
- copied or linked toolkit skills.

The example keeps placeholders until real endpoint details are supplied. Never commit a real key.

## Configure A C Project

Commit `.polyspace-toolkit.json` at the project root:

```json
{
  "schemaVersion": 1,
  "language": "c",
  "profiles": ["misra-c-2012", "polyspace-defects"],
  "checkersFile": ".polyspace/checkers.xml",
  "buildOptionsFile": ".polyspace/build-options.txt",
  "include": ["src/**/*.c"],
  "exclude": ["vendor/**"]
}
```

Supported built-in profile identifiers are:

- `misra-c-2012`
- `misra-c-2023`
- `cert-c`
- `cwe`
- `polyspace-defects`
- `custom`

Validate the contract before invoking an agent:

```sh
polyspace-toolkit config validate .polyspace-toolkit.json
```

Paths are resolved relative to the configuration file. Headers are analyzed through a containing C
translation unit. Unsupported entries in mixed compilation databases are ignored with a warning.

## Use The Compliance Loop

Ask a configured agent:

> Analyze the changed C translation units with the configured Polyspace profiles. Explain each new
> finding, apply behavior-preserving fixes first, run targeted tests, and re-analyze until the
> changed scope is clean.

The `c-compliance-loop` skill guides the agent through this sequence:

1. Load and validate project configuration.
2. Resolve the requested `.c` translation units.
3. Run Polyspace through MCP or the documented CLI fallback.
4. Explain findings using documentation for the installed release.
5. Prefer a source fix, then compile and test it.
6. Re-run analysis until the requested scope is clean or a real blocker is reported.

The toolkit never authorizes a justification automatically. It must show the exact annotation and
wait for approval, including when a catalog entry matches. Generated PSTUnit binaries require a
separate approval immediately before execution.

## Safety Model

- Downloads are accepted only when the asset and digest match the tested manifest.
- Setup plans are shown before mutation and require confirmation unless `--yes` is explicit.
- Existing user configuration is preserved unless replacement is explicitly requested.
- Owned files, hashes, backups, selected release, and client registrations are recorded locally.
- Secrets are never written to toolkit state.
- Operating-system download protections are never removed automatically.
- Uninstall refuses to remove files or registrations that changed after setup.

User-local state is stored under the platform state directory. It contains paths, versions, hashes,
and backups, not credentials or model-provider secrets.

## Current Verification

The Codex-only Windows benchmark completed all 12 deterministic setup and safety scenarios. The
candidate passed 12/12; the fixed upstream baseline recorded 0 passes, 4 observed failures, and 8
requirements without deterministic implementations. A live Codex CLI also parsed the installed MCP
registration successfully.

See [BENCHMARK.md](BENCHMARK.md) for the protocol and
[the latest evidence summary](benchmark/results/2026-06-23-windows-x86_64-no-qwen/SUMMARY.md) for
raw-result links and scope limits.

This evidence does **not** prove analyzer correctness. A licensed Polyspace installation and checker
file were unavailable on the benchmark host, so model-driven analyzer workflows and the real smoke
suite remain unscored.

## Development

Install development dependencies and run the same checks used by CI:

```sh
python -m pip install -e ".[dev]"
make test
make lint
make typecheck
make validate-product
make validate-agent-docs
```

The test workflow runs fake-client integration tests on Windows, Linux, and macOS. Licensed
Polyspace smoke tests are separate and opt-in:

```sh
export POLYSPACE_ROOT=/absolute/path/to/polyspace-release
export POLYSPACE_SMOKE_CHECKERS_FILE=/absolute/path/to/checkers.xml
make test-polyspace-smoke
```

On PowerShell, set the same variables through `$env:POLYSPACE_ROOT` and
`$env:POLYSPACE_SMOKE_CHECKERS_FILE` before running `make test-polyspace-smoke`.

Product skills are canonical under `skills/`. After changing one, regenerate and verify the Codex
plugin mirror:

```sh
make sync-plugin
make validate-product
```

## Project Layout

| Path | Purpose |
| --- | --- |
| `src/personal_polyspace_toolkit/` | CLI, discovery, release, state, client, and config logic |
| `skills/` | Canonical C-only agent skills |
| `plugins/personal-polyspace-toolkit/` | Generated Codex plugin metadata and skill mirror |
| `.claude-plugin/` | Claude marketplace metadata |
| `docs/setup/` | Client-specific setup guidance |
| `tests/` | Unit, fake integration, policy, and opt-in smoke tests |
| `benchmark/` | Reproducible upstream comparison protocol and evidence |

## Known Limits

- This is an unofficial alpha, not a stable or supported MathWorks release.
- A real licensed Polyspace smoke run has not completed on the development host.
- Claude registration is covered by fake-client tests but was not exercised with a live Claude CLI
  on the development host.
- Qwen configuration is manual and awaits a real localhost URL and model ID.
- Non-C translation units and additional client integrations are outside the active product scope.

## Upstream, License, And Contributions

The initial domain workflows derive from MathWorks' toolkit at commit
`cc15b840e80bf5187963d13ed86c4c5bb86381ad`. [UPSTREAM.md](UPSTREAM.md) records provenance and the
sync policy. Copyright notices and third-party license material are retained.

Before contributing, read [CONTRIBUTING.md](CONTRIBUTING.md). Changes should preserve the C-only
scope, the five MCP compatibility names, explicit approval gates, and the MathWorks-product-only
license condition.
