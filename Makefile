PYTHON ?= python

.PHONY: install dev test test-unit test-integration test-polyspace-smoke lint typecheck validate-product sync-plugin \
	docs-map validate-agent-docs check-context-staleness audit-module-cards audit-memory \
	git-status git-diff

install:
	$(PYTHON) -m pip install -e ".[dev]"

dev:
	$(PYTHON) -m personal_polyspace_toolkit.cli doctor --json

test: test-unit test-integration

test-unit:
	$(PYTHON) -m pytest tests/unit -q

test-integration:
	$(PYTHON) -m pytest tests/integration -q

test-polyspace-smoke:
	$(PYTHON) -m pytest tests/smoke -q -m polyspace

lint:
	$(PYTHON) -m ruff check src tests scripts

typecheck:
	$(PYTHON) -m mypy

validate-product:
	$(PYTHON) scripts/validate_product_surfaces.py
	$(PYTHON) scripts/sync_codex_plugin.py --check

sync-plugin:
	$(PYTHON) scripts/sync_codex_plugin.py

docs-map:
	$(PYTHON) scripts/generate_codemap.py

validate-agent-docs:
	$(PYTHON) scripts/validate_agent_docs.py

check-context-staleness:
	$(PYTHON) scripts/check_context_staleness.py

audit-module-cards:
	$(PYTHON) scripts/audit_module_cards.py

audit-memory:
	$(PYTHON) scripts/validate_memory_links.py
	$(PYTHON) scripts/audit_memory_staleness.py

git-status:
	git status --short --branch

git-diff:
	git diff --stat
