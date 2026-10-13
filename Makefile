.PHONY: fmt lint test check fix-staged orchestrator-init orchestrator-status orchestrator-validate

fmt:
	@pre-commit run --hook-stage manual --all-files

lint:
	@SKIP=codex-autofix-fallback pre-commit run --hook-stage pre-commit --all-files

test:
	@bash -euo pipefail -c '\
		if [[ -d tests ]]; then \
			python3 -m unittest discover -s tests -p "test_*.py"; \
		else \
			echo "test: skipping python unittest discovery (no tests/ directory)"; \
		fi'
	@tools/context-check-lite

check: lint test

fix-staged:
	@tools/git_precommit

orchestrator-init:
	@python3 scripts/orchestrator_guard.py init
	@python3 scripts/orchestrator_guard.py assert
	@python3 scripts/orchestrator_guard.py run-status
	@python3 scripts/orchestrator_guard.py policy-show

orchestrator-status:
	@python3 scripts/orchestrator_guard.py run-status
	@python3 scripts/orchestrator_guard.py policy-show

orchestrator-validate:
	@python3 scripts/orchestrator_validate.py --output-json .orchestrator/validation_summary.json
