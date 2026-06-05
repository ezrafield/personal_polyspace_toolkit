General reusable skills I would create first

These should be global, reused across projects.

~/.agents/skills/
├── repo-navigator/
├── safe-implementation/
├── test-debug-loop/
├── code-review/
├── docs-sync/
├── architecture-decision/
└── task-handoff/
1. repo-navigator

Purpose: find the right files without scanning the whole repo.

Trigger:

Use when the task requires understanding where code lives, finding related files, or mapping a feature to modules.

Behavior:

1. Read AGENTS.md / CLAUDE.md.
2. Read docs/agent/INDEX.md.
3. Read CODEMAP.md.
4. Select relevant module cards.
5. Use rg/grep only for targeted discovery.
6. Return file candidates and confidence.

This is probably the highest token-saving skill.

2. safe-implementation

Purpose: standard feature/fix workflow.

Behavior:

1. Restate goal.
2. Identify affected modules.
3. Read only relevant docs/files.
4. Make smallest safe patch.
5. Add/update tests.
6. Run targeted checks.
7. Summarize files changed and risks.
3. test-debug-loop

Purpose: handle failing tests efficiently.

Behavior:

1. Run the smallest failing test.
2. Read the failure.
3. Identify probable root cause.
4. Patch minimally.
5. Re-run same test.
6. Expand test scope only after fix.

This prevents the agent from running broad test suites too early.

4. code-review

Purpose: read-only review before merge.

Check:

- correctness
- security
- edge cases
- architecture drift
- unnecessary complexity
- test coverage
- backward compatibility
5. docs-sync

Purpose: update docs only when behavior changes.

Check:

- README
- docs/agent/CODEMAP.md
- module cards
- API contracts
- ADR if architectural decision changed
6. architecture-decision

Purpose: prevent over-engineering.

Use when:

- choosing RAG vs tool-calling vs workflow vs agent
- adding dependency
- changing database
- introducing queue/cache
- changing service boundary
7. task-handoff

Purpose: summarize long work into reusable state.

Output:

- goal
- assumptions
- files inspected
- files changed
- commands run
- unresolved risks
- next recommended action
3. General reusable tools/scripts

These should be deterministic scripts inside your reusable kit or copied into each repo.

scripts/
├── generate_codemap.py
├── summarize_changed_files.py
├── update_module_cards.py
├── run_targeted_tests.py
├── validate_agent_docs.py
├── detect_large_context_docs.py
├── check_architecture_boundaries.py
└── collect_task_trace.py
Highest ROI tools
Tool	Why it matters
generate_codemap.py	Saves file-discovery tokens
run_targeted_tests.py	Prevents expensive broad test loops
summarize_changed_files.py	Makes final review cheaper
validate_agent_docs.py	Prevents stale agent docs
check_architecture_boundaries.py	Catches imports/layer violations
detect_large_context_docs.py	Warns when AGENTS.md / CLAUDE.md becomes too large

For token saving, deterministic scripts are better than “asking another agent” because they are cheaper, repeatable, and auditable.

4. General Claude subagents I would create

For Claude Code, I would create only a few global subagents first:

~/.claude/agents/
├── repo-researcher.md
├── code-reviewer.md
├── test-debugger.md
├── security-reviewer.md
└── docs-maintainer.md

Claude supports user-level subagents in ~/.claude/agents/ and project-specific subagents in .claude/agents/; project subagents can be checked into version control for team reuse.

1. repo-researcher

Use: read-only code discovery.

Tools:

Read, Grep, Glob, Bash
No Write/Edit

Best for:

“Find where this feature is implemented”
“Map the data flow”
“Find tests related to this module”
2. code-reviewer

Use: after code changes.

Focus:

- bugs
- architecture drift
- security
- unnecessary abstraction
- missing tests
3. test-debugger

Use: failing tests or runtime errors.

Focus:

- reproduce
- isolate root cause
- suggest minimal patch
4. security-reviewer

Use: auth, secrets, permissions, data handling, dependency changes.

Keep this read-only by default.

5. docs-maintainer

Use: update module cards, CODEMAP.md, docs after implementation.

5. Project-specific skills/tools/agents

Create project-specific assets only when the project has rules that general skills cannot know.

Recommended structure:

project/
├── AGENTS.md
├── CLAUDE.md
├── .agents/
│   └── skills/
│       ├── project-domain-rules/
│       │   └── SKILL.md
│       ├── project-eval-runner/
│       │   ├── SKILL.md
│       │   └── scripts/
│       └── project-release-check/
│           └── SKILL.md
│
├── .claude/
│   └── agents/
│       ├── project-architect.md
│       ├── project-reviewer.md
│       └── project-eval-runner.md
│
└── docs/
    └── agent/
        ├── INDEX.md
        ├── CODEMAP.md
        ├── ARCHITECTURE.md
        ├── PITFALLS.md
        └── module-cards/

Codex supports repository skills under .agents/skills, and it scans skill directories from the current working directory up to the repository root, which makes module-specific skills possible. Codex also supports layered AGENTS.md guidance, where files closer to the working directory override earlier guidance, with a 32 KiB default project-doc cap.

6. What should be project-specific?
Project-specific skill examples
Project type	Skill
RAG / GraphRAG project	retrieval-eval-skill
LangGraph agent project	state-machine-change-skill
FastAPI backend	api-contract-change-skill
EPD/LCA project	epd-domain-rules-skill
Video RAG project	multimodal-evidence-skill
Embedded/AutoDrive AI	edge-ai-constraint-skill
Invoice extraction	schema-extraction-eval-skill
AI Coach	safety-and-coaching-policy-skill
Project-specific agent examples
Agent	Use
project-architect	Checks if changes violate project architecture
domain-reviewer	Checks domain-specific correctness
eval-runner	Runs project quality checks
migration-reviewer	Reviews DB/schema migrations
release-gatekeeper	Checks deployment readiness

But only create these after you see repeated mistakes.