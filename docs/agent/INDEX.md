# Agent Context Index

Use this file to choose the smallest useful context for the task.

## For Bug Fixes
Read:
1. `docs/agent/CODEMAP.md`
2. Relevant module card in `docs/agent/module-cards/`
3. Related tests

Do not read:
- Full product docs
- Full architecture docs
- Unrelated modules

## For New API Endpoints
Read:
1. `docs/agent/module-cards/api.md`
2. `docs/specs/api-contracts.md`
3. Existing similar endpoint
4. Relevant service module card

## For Database Changes
Read:
1. `docs/agent/module-cards/database.md`
2. Relevant ADRs in `docs/adr/`
3. Existing migrations or model files
4. Related model tests

## For Frontend Changes
Read:
1. `docs/agent/module-cards/frontend.md`
2. `docs/product/USER_FLOWS.md`
3. Existing similar screen or component
4. Related tests

## For Refactors
Read:
1. `docs/agent/ARCHITECTURE.md`
2. Relevant module cards
3. Current tests
4. `docs/agent/PITFALLS.md`

## For Planning Or Product Questions
Read:
1. `docs/product/PRD.md`
2. `docs/product/REQUIREMENTS.md`
3. `docs/product/USER_FLOWS.md`

## For Agent, Skill, Tool, Or MCP Changes
Read:
1. `docs/agent/AGENTS_AND_SKILLS.md`
2. `docs/agent/TOOLS.md`
3. `docs/agent/MCPS.md`
4. Relevant files under `.agents/skills/`, `.claude/agents/`, `.mcp/`, or `scripts/`

## For Agent Kit Setup, Install, Or Audit
Read:
1. `agentkit-manifest.json`
2. `docs/agent/TOOLS.md`
3. `.agents/skills/agent-setup/SKILL.md`
4. Relevant installer, setup, audit, or hook files under `scripts/`, `.agent/`, or `.claude/hooks/`

## For Source Understanding Or Code Search
Read:
1. `docs/agent/SOURCE_UNDERSTANDING.md`
2. `docs/agent/module-cards/source-understanding.md`
3. `.understand-anything/README.md`
4. `.understand-anything/knowledge-graph.json` only through targeted search when it exists
