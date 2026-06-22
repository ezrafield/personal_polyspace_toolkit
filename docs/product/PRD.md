# Product Requirements Document

## Product

Personal Polyspace Toolkit is an unofficial, local-first, C-only integration layer for Polyspace as
You Code and strong coding agents.

## Goals

- Make setup deterministic, reversible, and supply-chain aware.
- Give agents focused Polyspace expertise without loading every workflow at once.
- Drive an analyze, explain, fix, test, and re-analyze loop for C translation units.
- Keep compliance choices and source justifications under human control.
- Support Codex, Claude Code, and manually configured local Qwen Code.

## Non-Goals

- Implementing or redistributing the Polyspace MCP server.
- Supporting additional languages or coding clients.
- Automatically selecting coding standards, justifying findings, or trusting generated executables.
- Managing Qwen model endpoints or credentials.
