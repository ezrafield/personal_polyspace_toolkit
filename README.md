# Personal Polyspace Toolkit

An unofficial, independently maintained, C-only agent toolkit for
Polyspace&reg; as You Code&trade;. It provides deterministic setup, reusable agent skills,
and guarded workflows for analysis, remediation, justifications, checker configuration, and
PSTUnit tests.

This derivative is not an official MathWorks product. It is licensed solely for use with MathWorks
products and services; see [LICENSE.md](LICENSE.md) and [NOTICE.md](NOTICE.md).

## Why This Exists

The upstream toolkit contains valuable Polyspace domain guidance, but its setup is performed by an
agent interpreting Markdown. This project turns setup into tested Python code, pins and verifies the
MCP server release, tracks ownership for safe uninstall, narrows every workflow to C translation
units, and keeps checker selection explicit.

## Supported Clients

| Client | MCP setup | Skills |
| --- | --- | --- |
| OpenAI Codex | Automated, user scope | Automated and plugin metadata |
| Claude Code | Automated, user scope | Automated and marketplace metadata |
| Qwen Code | Manual | Manual; no extension is shipped |

Qwen Code can use a local OpenAI-compatible model endpoint. The base URL and model ID remain
placeholders until you provide them; see [docs/setup/qwen-local.md](docs/setup/qwen-local.md).

## Requirements

- Python 3.11 or later
- Polyspace as You Code R2024b or later
- At least one supported coding client
- A licensed, per-user MathWorks installation

## Development Install

Clone the repository to a permanent location. Automated skill and Claude marketplace setup resolves
assets from that checkout; the alpha release is not distributed as a standalone wheel.

```sh
python -m pip install -e ".[dev]"
polyspace-toolkit doctor --json
```

Preview setup before changing user configuration:

```sh
polyspace-toolkit setup --client codex --dry-run
polyspace-toolkit setup --client codex --yes
polyspace-toolkit verify --client codex
```

Add `--client claude` to configure both automated clients. Telemetry is disabled unless
`--enable-telemetry` is explicitly passed. Existing conflicting registrations are never replaced
without `--replace-existing`.

## Project Configuration

Every analyzed project should commit `.polyspace-toolkit.json`:

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

No checker profile is assumed. Validate the file with:

```sh
polyspace-toolkit config validate .polyspace-toolkit.json
```

## Happy Path

Ask a supported agent:

> Analyze the changed C translation units with the configured Polyspace profiles. Explain each new
> finding, apply real fixes first, run targeted tests, and re-analyze until the changed scope is clean.

The `c-compliance-loop` skill resolves project configuration, calls the five compatible Polyspace
MCP tools, prefers behavior-preserving fixes, and requires explicit approval before any source
justification or generated test executable runs.

The optional Codex plugin under `plugins/personal-polyspace-toolkit` is generated from the canonical
catalog. Run `make sync-plugin` after editing a product skill.

## Verification

See [BENCHMARK.md](BENCHMARK.md) for the reproducible A/B protocol against the fixed upstream
baseline and for the distinction between verified repository evidence and pending runtime results.

```sh
make test-unit
make test-integration
make lint
make typecheck
make validate-agent-docs
```

Real Polyspace smoke tests are opt-in because CI does not have a licensed installation:

```sh
export POLYSPACE_ROOT=/absolute/path/to/polyspace-release
export POLYSPACE_SMOKE_CHECKERS_FILE=/absolute/path/to/checkers.xml
make test-polyspace-smoke
```

The first smoke test probes the installed analysis executable. Supplying the checker file additionally
runs a standalone C analysis. Setting these variables is explicit approval to execute licensed local
Polyspace commands.

## Security

- The tested MCP server release is pinned and verified against its published SHA-256 digest.
- Installation and configuration writes are atomic where supported.
- Existing client entries and skill directories are treated as user-owned unless setup records them.
- Operating-system download protections are not removed automatically.
- State contains paths, versions, hashes, and backups only; it never stores model or API secrets.

## Upstream

The initial domain workflows derive from MathWorks' Polyspace Agentic Toolkit at commit
`cc15b840e80bf5187963d13ed86c4c5bb86381ad`. See [UPSTREAM.md](UPSTREAM.md) for the sync policy.
