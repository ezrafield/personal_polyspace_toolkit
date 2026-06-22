# Agent Context Index

Load the smallest relevant context for the task.

## Setup, Discovery, Download, Or Uninstall
1. `docs/agent/module-cards/installer.md`
2. `docs/agent/ARCHITECTURE.md`
3. `skills/toolkit-setup/SKILL.md`
4. Related unit and integration tests

## Client Integration
1. `docs/agent/module-cards/clients.md`
2. `docs/setup/qwen-local.md` only for Qwen Code
3. Current official client documentation when configuration behavior may have changed

## Polyspace Workflow Or Skill Change
1. `docs/agent/module-cards/skills.md`
2. The exact skill under `skills/`
3. `.polyspace-toolkit.schema.json` when project configuration is involved
4. Related policy tests

## Project Configuration
1. `docs/product/REQUIREMENTS.md`
2. `.polyspace-toolkit.schema.json`
3. `src/personal_polyspace_toolkit/project_config.py`
4. Configuration tests

## Agent Context Or Memory Change
1. `docs/agent/AGENTS_AND_SKILLS.md`
2. Relevant memory policy under `docs/agent/`
3. `.agent/memory/index.json`

## Source Understanding
1. `docs/agent/CODEMAP.md`
2. `docs/agent/CODE_SEARCH.md`
3. Exact searches with `rg`
