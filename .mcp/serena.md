# Serena MCP Profile

Serena is an optional advanced coding profile. Do not require every project or contributor to install it.

## When To Enable

Enable Serena for serious coding projects where language-server semantics matter, especially:
- Python
- TypeScript
- Java
- C#
- Go

## Best Uses

- Find declarations and implementations.
- Find all symbol references.
- Inspect diagnostics.
- Navigate class, function, and method relationships.
- Plan safe multi-file refactors and renames.

## Agent Policy

Use Serena after CODEMAP/module cards, Semble, and `rg` when exact symbol relationships or diagnostics affect correctness.

Do not use Serena as the first step for every task. The default template profile remains Semble + `rg` + CODEMAP/module cards.

## Setup Notes

Document project-specific Serena startup, language-server requirements, and workspace roots here after adoption. Keep secrets and user-local paths out of this file.
