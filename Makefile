.PHONY: install dev test test-unit test-integration lint typecheck docs-map validate-docs validate-agent-docs detect-large-context-docs check-architecture-boundaries update-module-cards targeted-tests task-trace understand understand-dashboard understand-search validate-understand-graph

install:
	@echo "Install project dependencies here."

dev:
	@echo "Start the development server here."

test: test-unit test-integration

test-unit:
	@echo "Run unit tests here."

test-integration:
	@echo "Run integration tests here."

lint:
	@echo "Run lint checks here."

typecheck:
	@echo "Run type checks here."

docs-map:
	python scripts/generate_codemap.py

validate-docs:
	python scripts/validate_docs.py

validate-agent-docs:
	python scripts/validate_agent_docs.py

detect-large-context-docs:
	python scripts/detect_large_context_docs.py

check-architecture-boundaries:
	python scripts/check_architecture_boundaries.py

update-module-cards:
	python scripts/update_module_cards.py

targeted-tests:
	python scripts/run_targeted_tests.py

task-trace:
	python scripts/collect_task_trace.py

understand:
	python scripts/understand_placeholder.py

understand-dashboard:
	@echo "Open the Understand Anything dashboard with the installed runtime command, for example /understand-dashboard."

understand-search:
	python scripts/search_understand_graph.py "$(QUERY)"

validate-understand-graph:
	python scripts/validate_understand_graph.py
