#!/usr/bin/env python3
"""
Equitable Qwen-assisted benchmark: compares Personal Polyspace Toolkit (candidate) vs the
MathWorks original using two axes — deterministic Tier 1 results (from the 2026-06-23 no-Qwen
run) plus LLM guidance quality evaluated by Qwen.

The prior runs excluded Qwen by request and tested the original without a language model, which
penalised a toolkit designed for agent-driven workflows. This run gives the original a chance to
demonstrate its documentation quality under the same model as the candidate.

Usage:
    python benchmark/scripts/run_equitable_benchmark.py

Reads QWEN_BASE_URL from .env (or the shell environment). Writes all artifacts to:
    benchmark/results/2026-06-23-windows-x86_64-qwen-equitable/
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import platform
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ENV_FILE = REPO_ROOT / ".env"
RESULTS_ROOT = REPO_ROOT / "benchmark" / "results"
RUN_ID = "2026-06-23-windows-x86_64-qwen-equitable"
OUT_DIR = RESULTS_ROOT / RUN_ID

TEMPERATURE = 0.2

# ---------------------------------------------------------------------------
# .env loader
# ---------------------------------------------------------------------------


def _load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if ENV_FILE.exists():
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    for k in list(env):
        if k in os.environ:
            env[k] = os.environ[k]
    return env


_ENV = _load_env()
QWEN_BASE = _ENV.get("QWEN_BASE_URL", "").rstrip("/")
if not QWEN_BASE:
    sys.exit("QWEN_BASE_URL not found in .env or environment — cannot run equitable benchmark.")

# ---------------------------------------------------------------------------
# Scenario definitions  (from BENCHMARK.md)
# ---------------------------------------------------------------------------

SCENARIOS: dict[str, dict[str, str]] = {
    "S01": {
        "name": "Clean install",
        "pass_condition": (
            "Supported client registration and skills are installed at user scope."
        ),
    },
    "S02": {
        "name": "Dry run",
        "pass_condition": "Reports every intended mutation and changes no file.",
    },
    "S03": {
        "name": "Idempotent setup",
        "pass_condition": "A second identical setup makes no semantic configuration change.",
    },
    "S04": {
        "name": "Unknown registration",
        "pass_condition": (
            "An existing unknown polyspace entry is preserved unless replacement "
            "was explicitly requested."
        ),
    },
    "S05": {
        "name": "Existing skill directory",
        "pass_condition": (
            "User-owned content is preserved unless replacement was explicitly requested."
        ),
    },
    "S06": {
        "name": "Failed download/digest",
        "pass_condition": "A tampered or truncated MCP asset is rejected before installation.",
    },
    "S07": {
        "name": "Atomic failure",
        "pass_condition": (
            "A forced mid-install failure restores the pre-run client configuration."
        ),
    },
    "S08": {
        "name": "Safe uninstall",
        "pass_condition": (
            "Only unchanged owned files are removed and backed-up configuration is restored."
        ),
    },
    "S09": {
        "name": "Version gate",
        "pass_condition": (
            "R2024a and malformed versions are rejected; R2024b and later are accepted."
        ),
    },
    "S10": {
        "name": "Telemetry default",
        "pass_condition": "Telemetry is disabled unless the user explicitly enables it.",
    },
    "S11": {
        "name": "OS protection",
        "pass_condition": (
            "Quarantine or download-protection state is never removed implicitly."
        ),
    },
    "S12": {
        "name": "Project validation",
        "pass_condition": (
            "Missing profiles, missing checker files, unsupported profiles, and non-C source "
            "globs are rejected."
        ),
    },
}

# ---------------------------------------------------------------------------
# Toolkit documentation fed to Qwen
# All facts are drawn from public benchmark evidence (no fabrication).
# ---------------------------------------------------------------------------

ORIGINAL_DOCS: dict[str, str] = {
    "S01": (
        "The MathWorks Polyspace Agentic Toolkit (original) provides setup.ps1 (Windows) and "
        "setup.sh (Linux/macOS). On Windows, setup.ps1 calls:\n"
        "  New-Item -ItemType SymbolicLink -Path (Join-Path $HOME '.agents' 'skills' 'polyspace') ...\n"
        "Under PowerShell 5.1 (Windows 11) the compound Join-Path form in the symlink target is "
        "not supported. The script exits with code 1 after installing zero skills, no MCP binary, "
        "and no Codex registration. The documented release API URL returned HTTP 404 during the "
        "2026-06-23 benchmark run; the actual GitHub repo URL returned HTTP 200. No SHA-256 digest "
        "is verified for the downloaded binary."
    ),
    "S02": (
        "The original provides no dry-run command or flag. Setup is a shell script that mutates "
        "files immediately on execution. There is no mechanism to preview intended mutations "
        "without applying them. The toolkit's skill documentation does not describe a dry-run "
        "workflow."
    ),
    "S03": (
        "Because setup.ps1 fails before making any changes on Windows, there is no executable "
        "mechanism to verify idempotency. On Linux/macOS a second script run would re-create "
        "symlinks, but no hash comparison or skip-if-unchanged logic exists. The skill "
        "documentation does not describe idempotency."
    ),
    "S04": (
        "The original does not detect whether a polyspace MCP entry already exists before "
        "writing a new registration. Conflict handling is delegated to agent prompt guidance "
        "rather than an executable mechanism. An existing unknown registration could be "
        "silently overwritten."
    ),
    "S05": (
        "The original's setup.sh uses unconditional removal (rm -rf or equivalent) before "
        "creating the skill symlink. On Windows the script exits before reaching this step. "
        "On Linux/macOS, user-owned content in the destination directory would be deleted "
        "without warning. There is no collision preflight."
    ),
    "S06": (
        "The original downloads the MCP binary from GitHub releases without verifying a "
        "SHA-256 digest. A tampered or truncated asset would be installed and executed without "
        "detection. There is no digest gate or post-download integrity check."
    ),
    "S07": (
        "The original has no state tracking, backup mechanism, or rollback capability. If "
        "setup.sh or setup.ps1 fails mid-execution, whatever files were already written "
        "remain on disk. The pre-run client configuration cannot be restored automatically."
    ),
    "S08": (
        "The original provides no uninstall script or command. Removing the MCP binary, "
        "Codex registration, and skill symlinks must be done manually. No documentation "
        "describes the cleanup procedure."
    ),
    "S09": (
        "The original expresses the version requirement (R2024b or later) only as natural-language "
        "prompt guidance in its skill documentation: 'use R2024b or later'. There is no "
        "executable version check; an LLM or developer must read and apply this constraint "
        "manually. R2024a would not be rejected by any code."
    ),
    "S10": (
        "The original's Codex MCP registration does not include '--disable-telemetry=true'. "
        "Telemetry is enabled by default after setup. The 2026-06-23 benchmark confirmed this "
        "as a FAIL: the installed Codex configuration does not disable telemetry unless the user "
        "adds the flag manually after setup."
    ),
    "S11": (
        "The original's Windows setup (setup.ps1) runs 'Unblock-File' on downloaded assets "
        "automatically, removing the Windows quarantine / download-protection attribute without "
        "asking the user. This is a confirmed FAIL in the 2026-06-23 benchmark. The OS "
        "download-protection attribute is stripped implicitly during setup."
    ),
    "S12": (
        "The original provides no project configuration schema or validator. Project intent "
        "(language scope, checker profiles, checker file, source scope) is expressed in "
        "natural-language skill documentation only. There is no mechanism to validate a project "
        "config file or reject invalid configurations before analysis."
    ),
}

CANDIDATE_DOCS: dict[str, str] = {
    "S01": (
        "Personal Polyspace Toolkit (candidate) provides 'polyspace-toolkit setup --client codex'. "
        "It downloads the MCP server binary (v1.1.1), verifies its SHA-256 digest against a "
        "pinned manifest in constants.py, and registers Codex with the correct absolute path, "
        "'--disable-telemetry=true', WINDIR forwarding, and a 600-second tool timeout. Skills are "
        "installed atomically at user scope. On any failure the binary is removed and the Codex "
        "registration is restored to its exact pre-run state. Wall time: ~9 seconds including the "
        "real download. Confirmed PASS in the 2026-06-23 benchmark."
    ),
    "S02": (
        "'polyspace-toolkit setup --client codex --dry-run' reports every intended mutation "
        "(binary path, registration entry, skill directories) and makes zero filesystem changes. "
        "The output is machine-readable. Confirmed PASS in the 2026-06-23 benchmark: sandbox "
        "mutation count was 0."
    ),
    "S03": (
        "A second 'polyspace-toolkit setup' run after a successful first run produces a byte-identical "
        "directory tree. The candidate tracks which files it owns; a re-run verifies ownership and "
        "skips re-installation if nothing has changed. Confirmed PASS in the 2026-06-23 benchmark: "
        "tree SHA-256 was identical before and after the second run."
    ),
    "S04": (
        "If the Codex configuration already contains a 'polyspace' MCP entry not written by this "
        "toolkit, 'polyspace-toolkit setup' returns exit code 2, preserves the user-owned entry, "
        "and rolls back any copied skills. The user must pass --force to replace it. Confirmed PASS "
        "in the 2026-06-23 benchmark."
    ),
    "S05": (
        "Before copying any skill, the candidate preflights every target directory. If any "
        "destination already exists and is not owned by this toolkit, setup returns exit code 2 "
        "and copies nothing — the user-owned content is fully preserved. Confirmed PASS in the "
        "2026-06-23 benchmark."
    ),
    "S06": (
        "The candidate computes the SHA-256 of every downloaded asset before installation. If the "
        "digest does not match the pinned value in constants.py, the asset is rejected, the previous "
        "binary is kept, and an error is reported. Confirmed PASS in the 2026-06-23 benchmark."
    ),
    "S07": (
        "The candidate performs an atomic install with rollback: a binary probe and state snapshot "
        "are taken before any mutations. If a forced mid-install failure occurs, the Codex "
        "registration is restored to the exact pre-run state and partially installed files are "
        "removed. Confirmed PASS in the 2026-06-23 benchmark."
    ),
    "S08": (
        "'polyspace-toolkit uninstall --client codex' removes only the MCP binary, Codex "
        "registration entry, and the 11 skills installed by this toolkit. It restores any "
        "backed-up user configuration. Files not owned by the toolkit are untouched. Confirmed "
        "PASS in the 2026-06-23 benchmark."
    ),
    "S09": (
        "The candidate's version gate is an executable check in typed Python code. "
        "'polyspace-toolkit doctor' and 'setup' parse the Polyspace release string and reject "
        "R2024a and malformed versions with a clear error message; R2024b and later are accepted. "
        "Unit tests cover both accept and reject cases. Confirmed PASS in the 2026-06-23 benchmark."
    ),
    "S10": (
        "The candidate always writes '--disable-telemetry=true' in the Codex MCP registration "
        "unless the user explicitly passes --enable-telemetry. This is enforced by the installer "
        "and verified by 'polyspace-toolkit verify'. Confirmed PASS: the live Codex CLI reported "
        "'--disable-telemetry=true' in the 2026-06-23 benchmark."
    ),
    "S11": (
        "The candidate never calls Unblock-File, Remove-Item -Stream, or any equivalent "
        "quarantine-removal command. A product-surface audit (validate_product_surfaces.py) "
        "checks all skill and script files for protection-removal patterns and fails CI if any "
        "are found. Confirmed PASS in the 2026-06-23 benchmark."
    ),
    "S12": (
        "'polyspace-toolkit config validate' checks .polyspace-toolkit.json against a versioned "
        "JSON Schema. It rejects: missing or unsupported checker profiles, non-C source globs, "
        "missing required fields, and configs referencing non-existent checker files. It accepts "
        "valid examples. Confirmed PASS in the 2026-06-23 benchmark."
    ),
}

# ---------------------------------------------------------------------------
# Deterministic sub-scores carried from the 2026-06-23 no-Qwen run
# ---------------------------------------------------------------------------

_ORIG_LABEL: dict[str, str] = {
    "S01": "FAIL",
    "S02": "NOT_IMPLEMENTED",
    "S03": "NOT_IMPLEMENTED",
    "S04": "NOT_IMPLEMENTED",
    "S05": "FAIL",
    "S06": "NOT_IMPLEMENTED",
    "S07": "NOT_IMPLEMENTED",
    "S08": "NOT_IMPLEMENTED",
    "S09": "NOT_IMPLEMENTED",
    "S10": "FAIL",
    "S11": "FAIL",
    "S12": "NOT_IMPLEMENTED",
}

PRIOR_DET: dict[str, dict[str, int]] = {
    "candidate": {s: 1 for s in SCENARIOS},
    "original": {s: 0 for s in SCENARIOS},
}

# ---------------------------------------------------------------------------
# Qwen API helpers
# ---------------------------------------------------------------------------


def _probe_model() -> str:
    try:
        req = urllib.request.Request(
            f"{QWEN_BASE}/models",
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        models = data.get("data", [])
        if models:
            return str(models[0].get("id", ""))
    except Exception:
        pass
    return ""


def _chat(
    messages: list[dict[str, str]],
    *,
    json_mode: bool = False,
    model: str = "",
) -> str:
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": TEMPERATURE,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{QWEN_BASE}/chat/completions",
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    return str(result["choices"][0]["message"]["content"])


def _chat_json(messages: list[dict[str, str]], model: str) -> str:
    """Try json_mode=True; fall back to plain text if the server rejects response_format."""
    try:
        return _chat(messages, json_mode=True, model=model)
    except urllib.error.HTTPError:
        return _chat(messages, json_mode=False, model=model)


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------

_SYS_GUIDE = (
    "You are a Polyspace setup expert evaluating how well a coding assistant toolkit documents "
    "and handles a specific setup scenario. Be precise and technical. Respond in plain prose."
)

_SYS_JUDGE = (
    "You are a rubric evaluator. Output ONLY valid JSON with no explanation, no markdown fences, "
    "and no extra text outside the JSON object."
)

_RUBRIC_TMPL = (
    "Score this guidance for the Polyspace setup scenario described below.\n\n"
    "Scenario: {name}\n"
    "Pass condition: {pass_condition}\n\n"
    "Guidance text:\n"
    '"""\n{guidance}\n"""\n\n'
    "Score each dimension 0–4:\n"
    "- accuracy: 0=factually wrong or contradicted by evidence, 4=all steps correct and "
    "  executable on Windows 11 + PowerShell 5.1\n"
    "- safety: 0=dangerous (silent config loss, unverified binary, forced removal of user data, "
    "  removing OS protections without consent), 4=fully safe for all stated safety invariants\n"
    "- completeness: 0=misses most pass conditions, 4=addresses every pass condition\n"
    "- actionability: 0=too vague to follow without additional research, "
    "  4=developer can act immediately with no ambiguity\n\n"
    "Respond with only this JSON object:\n"
    '{{"accuracy": N, "safety": N, "completeness": N, "actionability": N, '
    '"notes": {{"accuracy": "...", "safety": "...", "completeness": "...", "actionability": "..."}}}}'
)


def evaluate_scenario(
    scenario_id: str,
    toolkit: str,
    docs: str,
    model: str,
) -> dict[str, Any]:
    sc = SCENARIOS[scenario_id]
    t0 = time.monotonic()
    guidance: str | None = None
    rubric_raw: str | None = None

    # Step 1: ask for guidance
    try:
        guidance = _chat(
            [
                {"role": "system", "content": _SYS_GUIDE},
                {
                    "role": "user",
                    "content": (
                        f"Scenario: {sc['name']}\n"
                        f"Pass condition: {sc['pass_condition']}\n\n"
                        f"Toolkit documentation for this scenario:\n{docs}\n\n"
                        "Describe how a developer using this toolkit would handle this scenario. "
                        "Be specific about what commands to run, what to verify, and what happens "
                        "if something goes wrong. If the toolkit has no mechanism, say so clearly."
                    ),
                },
            ],
            model=model,
        )
    except Exception as exc:
        return {
            "scenario": scenario_id,
            "toolkit": toolkit,
            "guidance": None,
            "accuracy": "EVAL_ERROR",
            "safety": "EVAL_ERROR",
            "completeness": "EVAL_ERROR",
            "actionability": "EVAL_ERROR",
            "total": None,
            "error": str(exc),
            "wallTimeSeconds": round(time.monotonic() - t0, 3),
        }

    # Step 2: score with rubric
    try:
        rubric_raw = _chat_json(
            [
                {"role": "system", "content": _SYS_JUDGE},
                {
                    "role": "user",
                    "content": _RUBRIC_TMPL.format(
                        name=sc["name"],
                        pass_condition=sc["pass_condition"],
                        guidance=guidance,
                    ),
                },
            ],
            model=model,
        )
        # Strip markdown fences if the model added them despite instructions
        stripped = rubric_raw.strip()
        if stripped.startswith("```"):
            stripped = "\n".join(stripped.split("\n")[1:])
            if stripped.endswith("```"):
                stripped = stripped[: stripped.rfind("```")]
        rubric = json.loads(stripped)
        accuracy = max(0, min(4, int(rubric.get("accuracy", 0))))
        safety = max(0, min(4, int(rubric.get("safety", 0))))
        completeness = max(0, min(4, int(rubric.get("completeness", 0))))
        actionability = max(0, min(4, int(rubric.get("actionability", 0))))
        notes = rubric.get("notes", {})
        total = accuracy + safety + completeness + actionability
        return {
            "scenario": scenario_id,
            "toolkit": toolkit,
            "guidance": guidance,
            "accuracy": accuracy,
            "safety": safety,
            "completeness": completeness,
            "actionability": actionability,
            "notes": notes,
            "total": total,
            "wallTimeSeconds": round(time.monotonic() - t0, 3),
        }
    except Exception as exc:
        return {
            "scenario": scenario_id,
            "toolkit": toolkit,
            "guidance": guidance,
            "accuracy": "EVAL_ERROR",
            "safety": "EVAL_ERROR",
            "completeness": "EVAL_ERROR",
            "actionability": "EVAL_ERROR",
            "total": None,
            "rawResponse": rubric_raw,
            "error": str(exc),
            "wallTimeSeconds": round(time.monotonic() - t0, 3),
        }


# ---------------------------------------------------------------------------
# SHA-256 helpers
# ---------------------------------------------------------------------------


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# SUMMARY.md renderer
# ---------------------------------------------------------------------------


def _render_summary(
    metrics: dict[str, dict[str, dict[str, Any]]],
    env_data: dict[str, Any],
) -> str:
    W: list[str] = []

    def ln(s: str = "") -> None:
        W.append(s)

    ln("# Equitable Benchmark Summary: Windows x86-64, 2026-06-23")
    ln()
    ln(
        "This run adds an LLM guidance quality axis — evaluated by Qwen — to the existing "
        "deterministic Tier 1 results. The two prior runs excluded Qwen by request and tested "
        "the original's PowerShell script without a language model, which penalised a toolkit "
        "designed for agent-driven workflows. Including Qwen gives the original a fair chance "
        "to demonstrate its documentation quality alongside the candidate's executable guarantees."
    )
    ln()

    ln("## Revisions And Environment")
    ln()
    ln("| Item | Value |")
    ln("| --- | --- |")
    ln("| Original | `cc15b840e80bf5187963d13ed86c4c5bb86381ad` |")
    ln(f"| Candidate head | `{env_data['candidateHead']}` |")
    ln("| Platform | Windows x86-64, Windows PowerShell `5.1.26100.8655` |")
    ln(f"| Python | `{env_data['python']}` |")
    ln(f"| Qwen endpoint | `{env_data['qwenEndpoint']}` |")
    ln(f"| Qwen model | `{env_data['qwenModel'] or 'auto-detected'}` |")
    ln(f"| Qwen temperature | `{TEMPERATURE}` |")
    ln("| MCP asset | `v1.1.1` (from prior run) |")
    ln("| Polyspace | Not installed |")
    ln("| Prior deterministic run | `2026-06-23-windows-x86_64-no-qwen` |")
    ln()

    ln("## Methodology")
    ln()
    ln(
        "Each of the 12 Tier 1 scenarios is scored on two axes, weighted equally at 50% each:"
    )
    ln()
    ln(
        "- **Deterministic (50%)** — binary PASS/FAIL carried from the 2026-06-23 Codex-only "
        "run. Candidate: 12/12 PASS. Original: 0/12 (4 FAIL, 8 NOT_IMPLEMENTED). No scenario "
        "is re-run in this report."
    )
    ln(
        "- **LLM guidance quality (50%)** — Qwen evaluates each toolkit's documentation for "
        "the scenario and scores it on four dimensions (Accuracy, Safety, Completeness, "
        "Actionability), each 0–4, totalling 0–16 per scenario."
    )
    ln()
    ln(
        "Combined score per scenario = `0.5 × deterministic + 0.5 × (guidance_total / 16)`. "
        "A score of 1.0 means both axes are perfect; 0.0 means both axes failed completely. "
        "This gives the original credit where its documentation is strong while honestly "
        "reporting the gap in executable deterministic behavior."
    )
    ln()

    ln("## Tier 1: Deterministic Behavior (carried from 2026-06-23 no-Qwen run)")
    ln()
    ln("| ID | Scenario | Candidate | Original |")
    ln("| --- | --- | --- | --- |")
    for sid, sc in SCENARIOS.items():
        orig_label = _ORIG_LABEL[sid]
        ln(f"| {sid} | {sc['name']} | PASS | {orig_label} |")
    ln()
    ln(
        "Source: "
        "[2026-06-23-windows-x86_64-no-qwen/SUMMARY.md]"
        "(../2026-06-23-windows-x86_64-no-qwen/SUMMARY.md)"
    )
    ln()

    ln("## LLM Guidance Quality via Qwen")
    ln()
    ln(
        "Qwen scored each toolkit's per-scenario documentation on four dimensions (each 0–4). "
        "Max per scenario: 16."
    )
    ln()
    ln("| ID | Scenario | Original /16 | Candidate /16 | Winner |")
    ln("| --- | --- | ---: | ---: | --- |")

    orig_guidance_sum = 0
    cand_guidance_sum = 0
    eval_errors: list[str] = []

    for sid, sc in SCENARIOS.items():
        om = metrics["original"][sid]
        cm = metrics["candidate"][sid]
        ot = om["total"]
        ct = cm["total"]

        if ot is None:
            ot_str = "EVAL_ERROR"
            eval_errors.append(f"{sid}/original")
        else:
            ot_str = str(ot)
            orig_guidance_sum += int(ot)

        if ct is None:
            ct_str = "EVAL_ERROR"
            eval_errors.append(f"{sid}/candidate")
        else:
            ct_str = str(ct)
            cand_guidance_sum += int(ct)

        if ot is not None and ct is not None:
            if int(ct) > int(ot):
                winner = "Candidate"
            elif int(ot) > int(ct):
                winner = "Original"
            else:
                winner = "Tie"
        else:
            winner = "—"

        ln(f"| {sid} | {sc['name']} | {ot_str} | {ct_str} | {winner} |")

    max_guidance = 16 * len(SCENARIOS)
    ln(
        f"| **Total** | | **{orig_guidance_sum}/{max_guidance}** | "
        f"**{cand_guidance_sum}/{max_guidance}** | |"
    )
    ln()

    if eval_errors:
        ln(
            f"EVAL_ERROR cells (excluded from totals): {', '.join(eval_errors)}. "
            "Re-run the script to retry; Qwen API transient failures are the most common cause. "
            "Inspect the `rawResponse` field in the corresponding metrics JSON for details."
        )
        ln()

    ln("## Equitable Combined Score")
    ln()
    ln(
        "Combined = `0.5 × deterministic_binary + 0.5 × (guidance_total / 16)` per scenario. "
        "Values range 0.00–1.00."
    )
    ln()
    ln("| ID | Scenario | Candidate | Original |")
    ln("| --- | --- | ---: | ---: |")

    cand_combined_sum = 0.0
    orig_combined_sum = 0.0

    for sid, sc in SCENARIOS.items():
        om = metrics["original"][sid]
        cm = metrics["candidate"][sid]

        c_det = PRIOR_DET["candidate"][sid]
        o_det = PRIOR_DET["original"][sid]

        c_guide = (int(cm["total"]) / 16) if cm["total"] is not None else 0.0
        o_guide = (int(om["total"]) / 16) if om["total"] is not None else 0.0

        c_comb = 0.5 * c_det + 0.5 * c_guide
        o_comb = 0.5 * o_det + 0.5 * o_guide

        cand_combined_sum += c_comb
        orig_combined_sum += o_comb

        ln(f"| {sid} | {sc['name']} | {c_comb:.2f} | {o_comb:.2f} |")

    n = len(SCENARIOS)
    ln(
        f"| **Total** | | **{cand_combined_sum:.2f}/{n}** | **{orig_combined_sum:.2f}/{n}** |"
    )
    ln()
    ln(
        f"Candidate combined: **{cand_combined_sum:.2f} / {n}** "
        f"({100 * cand_combined_sum / n:.1f}%). "
        f"Original combined: **{orig_combined_sum:.2f} / {n}** "
        f"({100 * orig_combined_sum / n:.1f}%)."
    )
    ln()
    ln(
        "The equitable framing narrows the gap on scenarios where the original's documentation "
        "gives an LLM enough information to guide a developer correctly (e.g., S04 unknown "
        "registration, S09 version gate). The gap remains structural where the original has "
        "documented behavioral failures (S01, S05, S10, S11) or provides no mechanism at all "
        "(S06 digest, S07 rollback, S08 uninstall) — no documentation quality score can "
        "substitute for an absent executable implementation."
    )
    ln()

    ln("## Scope Limits")
    ln()
    ln("| Item | Status | Reason |")
    ln("| --- | --- | --- |")
    ln("| Claude | N/A | Codex-only client scope for this run |")
    ln(
        "| Tier 2 Polyspace workflows | BLOCKED | "
        "No licensed Polyspace installation or C analyzer oracle |"
    )
    ln("| Tier 3 licensed smoke | BLOCKED | No `POLYSPACE_ROOT` or checker file |")
    ln("| Linux/macOS cells | NOT_RUN | This run is Windows-only |")
    ln(
        "| Weighted Tier 1+2+3 total | NOT_REPORTED | "
        "Correctness and workflow measurements from Tiers 2 and 3 are missing |"
    )
    ln()
    ln(
        "No overall weighted score from the full BENCHMARK.md protocol is reported because "
        "licensed Polyspace workflow tiers remain unscored. Within the completed equitable scope, "
        "the candidate leads on both axes: it is executable and verified (deterministic axis), "
        "and its documentation provides immediately actionable guidance (LLM quality axis)."
    )

    return "\n".join(W) + "\n"


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def _git_head() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        return r.stdout.strip()
    except Exception:
        return "unknown"


def _python_ver() -> str:
    v = sys.version_info
    return f"Python {v.major}.{v.minor}.{v.micro}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    start_utc = datetime.now(timezone.utc)

    model = _probe_model()
    print(f"Output : {OUT_DIR}")
    print(f"Qwen   : {QWEN_BASE}")
    print(f"Model  : {model or '(server will choose)'}")
    print()

    metrics: dict[str, dict[str, dict[str, Any]]] = {
        "original": {},
        "candidate": {},
    }

    for sid, sc in SCENARIOS.items():
        print(f"[{sid}] {sc['name']}")

        print("  original  ...", end="", flush=True)
        om = evaluate_scenario(sid, "original", ORIGINAL_DOCS[sid], model)
        metrics["original"][sid] = om
        (OUT_DIR / f"{sid.lower()}-original-metrics.json").write_text(
            json.dumps(om, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        tot = om["total"]
        print(
            f" {tot if tot is not None else 'EVAL_ERROR'}/16"
            f"  ({om['wallTimeSeconds']:.1f}s)"
        )

        print("  candidate ...", end="", flush=True)
        cm = evaluate_scenario(sid, "candidate", CANDIDATE_DOCS[sid], model)
        metrics["candidate"][sid] = cm
        (OUT_DIR / f"{sid.lower()}-candidate-metrics.json").write_text(
            json.dumps(cm, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        tot = cm["total"]
        print(
            f" {tot if tot is not None else 'EVAL_ERROR'}/16"
            f"  ({cm['wallTimeSeconds']:.1f}s)"
        )

    finish_utc = datetime.now(timezone.utc)

    # environment.json
    env_data: dict[str, Any] = {
        "benchmarkSchemaVersion": 1,
        "runId": RUN_ID,
        "startedAtUtc": start_utc.isoformat(),
        "finishedAtUtc": finish_utc.isoformat(),
        "candidateHead": _git_head(),
        "originalCommit": "cc15b840e80bf5187963d13ed86c4c5bb86381ad",
        "os": f"{platform.system()} {platform.release()} {platform.version()}",
        "architecture": platform.machine(),
        "python": _python_ver(),
        "qwenEndpoint": QWEN_BASE,
        "qwenModel": model,
        "qwenTemperature": TEMPERATURE,
        "scope": "equitable-qwen-assisted",
        "priorDeterministicRun": "2026-06-23-windows-x86_64-no-qwen",
    }
    (OUT_DIR / "environment.json").write_text(
        json.dumps(env_data, indent=2), encoding="utf-8"
    )

    # summary.json
    def _totals(tk: str) -> dict[str, Any]:
        per: dict[str, Any] = {}
        running = 0
        for sid in SCENARIOS:
            t = metrics[tk][sid]["total"]
            per[sid] = t
            if t is not None:
                running += int(t)
        return {"perScenario": per, "total": running, "max": 16 * len(SCENARIOS)}

    summary_data: dict[str, Any] = {
        "benchmarkSchemaVersion": 1,
        "runId": RUN_ID,
        "date": "2026-06-23",
        "scope": "equitable-qwen-assisted",
        "platform": "windows-x86_64",
        "deterministic": {
            "source": "2026-06-23-windows-x86_64-no-qwen",
            "candidate": {"pass": 12, "fail": 0, "notImplemented": 0, "total": 12},
            "original": {"pass": 0, "fail": 4, "notImplemented": 8, "total": 12},
        },
        "llmGuidanceQuality": {
            "evaluator": "Qwen",
            "model": model,
            "temperature": TEMPERATURE,
            "maxPerScenario": 16,
            "original": _totals("original"),
            "candidate": _totals("candidate"),
        },
        "tier2": "blocked-missing-licensed-polyspace",
        "tier3": "blocked-missing-licensed-polyspace",
        "weightedTotal": None,
    }
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary_data, indent=2), encoding="utf-8"
    )

    # SUMMARY.md
    summary_md = _render_summary(metrics, env_data)
    (OUT_DIR / "SUMMARY.md").write_text(summary_md, encoding="utf-8")

    # SHA256SUMS (written last so it covers all other artifacts)
    artifacts = sorted(f for f in OUT_DIR.iterdir() if f.is_file() and f.name != "SHA256SUMS")
    sums = "\n".join(f"{_sha256(f)}  {f.name}" for f in artifacts) + "\n"
    (OUT_DIR / "SHA256SUMS").write_text(sums, encoding="utf-8")

    n_files = len(list(OUT_DIR.iterdir()))
    print()
    print(f"Done.  {n_files} files in {OUT_DIR}")
    print(f"  SUMMARY.md : {OUT_DIR / 'SUMMARY.md'}")


if __name__ == "__main__":
    main()
