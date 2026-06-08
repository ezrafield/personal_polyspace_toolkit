# Code Search

## Purpose
Find the smallest useful code context with Semble, `rg`, CODEMAP, module cards, and optional Serena.

## Trigger
Use when the task requires locating source files, understanding where behavior lives, finding related tests, or confirming symbols before edits.

## Workflow
1. Read `docs/agent/INDEX.md`.
2. Read `docs/agent/CODE_SEARCH.md`.
3. Read `docs/agent/CODEMAP.md` or the relevant module card.
4. Search natural language with Semble:
   - `semble search "<task>" . --content code`
   - `semble search "<task>" . --content all` when docs/config/tests may matter
5. Confirm exact strings, symbols, and paths with `rg`.
6. Use Serena when references, declarations, implementations, diagnostics, or safe refactors matter.
7. Read full files only after retrieval identifies likely targets.
8. Before editing, summarize selected files, relevance, and uncertainty.

## Output
- Search terms used
- Candidate files
- Exact confirmations
- Related tests
- Confidence and risks

## Constraints
- Do not scan the whole repository unless the task requires it.
- Do not use Repomix as a normal retrieval tool.
- Do not treat natural-language retrieval as authoritative without source confirmation.
