# Context Router

Use this router when a task is more than a one-line command or isolated question.

## Routing Policy

Do not scan the whole repository for non-trivial code tasks. Start with the cheapest reliable context, then expand only when uncertainty remains.

## Standard Route

1. Read `docs/agent/INDEX.md`.
2. Read the relevant module card or `docs/agent/CODEMAP.md`.
3. Use Semble for natural-language retrieval.
4. Use `rg` for exact confirmation.
5. Use Serena when language-server semantics are valuable.
6. Read full files only after retrieval identifies likely targets.
7. Run targeted tests before broad suites.

## Tool Profiles

### Default

Use Semble + `rg` + CODEMAP/module cards.

This profile has low setup cost, low token cost, high portability, and works well across Codex, Claude Code, Cursor, and similar agents.

### Advanced Coding

Use Semble + Serena + `rg` + CODEMAP/module cards.

Enable this profile for serious Python, TypeScript, Java, C#, and Go projects where references, declarations, diagnostics, and refactors benefit from language-server semantics.

### Export

Use Repomix only when the task requires sending a bundled repository snapshot to an external model or reviewer. It should not be the default daily retrieval workflow.

## Escalation Signals

Escalate from CODEMAP/module cards to Semble when:
- The task is phrased in product or behavior language.
- You do not know the exact symbol name.
- Relevant files could span docs, config, tests, and source.

Escalate from Semble or `rg` to Serena when:
- You must identify all references.
- A rename or refactor crosses files.
- Diagnostics or type-aware symbol information affects correctness.

Escalate to graph tools when:
- Dependency impact matters.
- You need architecture-level relationships.
- The task is onboarding, review, or broad source understanding.
