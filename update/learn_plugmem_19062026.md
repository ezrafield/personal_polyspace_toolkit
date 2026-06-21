What we should learn from PlugMem
1. Separate memory into 3 types

PlugMem uses:

PlugMem memory type	Meaning	Apply to your template as
Semantic memory	Facts, concepts, preferences	Project facts, stack facts, conventions
Procedural memory	Workflows and how-to steps	“How we fix X in this repo” playbooks
Episodic memory	Past interaction/task sessions	Raw task logs under .agent/tasks/

PlugMem’s README explicitly lists semantic, procedural, and episodic memory and describes graph structure, LLM-based extraction, retrieval, reasoning, and memory evolution.

Your template should adopt this taxonomy.

Recommended structure:

.agent/
├── tasks/                         # episodic memory: raw task traces
├── memory/
│   ├── semantic/
│   │   ├── project-facts.md
│   │   ├── conventions.md
│   │   └── decisions.md
│   ├── procedural/
│   │   ├── debugging-playbooks.md
│   │   ├── testing-playbooks.md
│   │   └── refactor-playbooks.md
│   ├── episodic/
│   │   └── index.md
│   └── memory-graph.json          # optional lightweight graph
2. Extract reusable lessons from task logs

Right now, .agent/tasks/ is mostly an audit trail. That is useful, but it is still episodic memory. PlugMem’s important insight is: raw episodes are too verbose; useful memory is abstracted knowledge.

The paper argues that raw memory retrieval often fails because useful decision-making information is sparse inside verbose episodes, while agents usually need compact factual or procedural knowledge.

So after each meaningful task, your template should produce:

# Memory Extraction

## Semantic facts learned
- The API routes are registered in `src/api/routes.py`.
- Environment variables are loaded through `src/config.py`.

## Procedural lessons learned
- When changing request validation, update both schema tests and route tests.
- Run `make test-unit` before full lint because unit tests fail faster.

## Files related
- `src/api/routes.py`
- `tests/api/test_routes.py`

## Confidence
High / Medium / Low

## Should promote to long-term memory?
Yes / No

This is more valuable than saving the whole chat or command output.

3. Use memory as a “decision aid,” not as source of truth

PlugMem improves performance by retrieving relevant memory and then reasoning over it; the paper reports that retrieval is essential, but retrieval alone is insufficient because memory structure controls what can be found and reused.

For your template, memory should guide the agent like this:

Task starts
→ read AGENTS.md / CLAUDE.md
→ route through docs/agent/INDEX.md
→ retrieve relevant memory cards
→ use Semble / rg / Serena to verify current code
→ patch
→ test
→ extract new memory if useful

Important rule: memory can suggest where to look, but current source code is the authority.

Is PlugMem suitable for your project now?
Suitable as an idea: yes

Very suitable.

Your template is becoming an agent-native operating system for repositories. Long-term memory is the next logical layer after:

Semble = find relevant code
RTK = compress noisy command output
Understand Anything = graph/source understanding
.agent/tasks = task audit
PlugMem-style memory = learn from previous tasks

This aligns with production AI system design: the product is not just the model; it includes context building, retrieval, tool use, validation, UX, feedback, analytics, monitoring, and evaluation.

Suitable as a direct dependency: not yet

I would not add PlugMem itself as a default dependency now.

Reasons:

Concern	Why it matters
Too research-heavy	PlugMem is benchmark/research-oriented, not a small template utility.
Setup complexity	Quick start references OpenAI keys, Azure endpoint, Qwen server, and embedding server setup.
Heavy inference assumptions	Local Qwen + NV-Embed via vLLM is not lightweight for every repo template user.
Memory quality risk	Bad extracted memory can mislead future agents.
Privacy/security risk	Task logs may contain secrets, customer data, stack traces, or credentials.
Staleness risk	Memory can become wrong after refactors.
Not needed for MVP	Your template first needs clean context routing and measurable retrieval before complex memory graphs.

The right product decision is: implement a lightweight PlugMem-inspired memory layer first.

Best implementation for your template

Add a minimal memory pipeline:

1. Task completed
2. Agent writes `.agent/tasks/<task-id>/summary.md`
3. Script extracts candidate memory
4. Human or rule-based gate decides promotion
5. Promoted memory goes into `.agent/memory/semantic` or `.agent/memory/procedural`
6. Future agents retrieve memory before code search
7. Memory is validated against current files before use

Recommended new files:

.agent/
├── memory/
│   ├── README.md
│   ├── semantic/project-facts.md
│   ├── semantic/conventions.md
│   ├── procedural/debugging-playbooks.md
│   ├── procedural/testing-playbooks.md
│   ├── procedural/refactor-playbooks.md
│   └── index.json

docs/agent/
├── MEMORY_POLICY.md
├── MEMORY_RETRIEVAL.md
└── MEMORY_PROMOTION_RULES.md

scripts/
├── extract_task_memory.py
├── validate_memory_links.py
└── audit_memory_staleness.py

eval/
└── memory/
    ├── queries.json
    └── expected_memory.json
Add this to AGENTS.md
## Long-Term Memory Policy

Use long-term memory as guidance, not truth.

Before starting non-trivial tasks:

1. Read `docs/agent/INDEX.md`.
2. Check `.agent/memory/index.json` for relevant semantic/procedural memory.
3. Use memory to choose likely files, workflows, and risks.
4. Verify all memory against current source files before editing.
5. Do not rely on memory if it conflicts with code, tests, or docs.
6. After completing a task, extract reusable lessons only if they are likely to help future tasks.

Memory types:
- Semantic: stable project facts and conventions.
- Procedural: reusable workflows, debugging steps, testing rules.
- Episodic: raw task logs under `.agent/tasks/`.

Never promote secrets, credentials, private customer data, or one-off noisy details into long-term memory.
Memory card format

Use simple Markdown first, not a graph database.

# Memory: Request Validation Workflow

Type: procedural
Scope: api
Confidence: medium
Last verified: 2026-06-19
Source task: .agent/tasks/2026-06-19-request-validation/

## When to use

Use this when changing request validation or API schemas.

## Procedure

1. Find route handler.
2. Find request schema.
3. Update validation logic.
4. Run route-level tests.
5. Run schema-level tests.

## Verification commands

```bash
make test-unit
make lint
Related files
src/api/
tests/api/
Staleness triggers

Re-check this memory if:

API framework changes
schema library changes
test layout changes

## How it fits with Semble and RTK

```text
Semble:
Find current relevant code snippets.

RTK:
Compress command/test/log output.

PlugMem-inspired memory:
Recall lessons from past successful tasks.

CODEMAP/module cards:
Explain intended architecture.

Eval:
Prove retrieval and memory actually help.

The complete flow:

User task
→ AGENTS.md
→ docs/agent/INDEX.md
→ retrieve relevant memory cards
→ Semble / rg / Serena verify current code
→ edit
→ RTK-compressed tests/lint/git output
→ raw fallback if needed
→ task audit
→ memory extraction
→ memory promotion gate
Biggest risk

The biggest risk is polluting memory with low-quality lessons.

Bad memory example:

Always edit `src/api/routes.py` when tests fail.

Good memory example:

For request validation failures, first check schema definitions, then route binding, then tests. Do not assume the route handler is wrong.

This is why promotion must be gated.