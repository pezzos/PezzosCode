.DEFAULT_GOAL := check

-include make.local.mk

FMT_HOOKS := end-of-file-fixer trailing-whitespace ruff-fix ruff-format black-format prettier-format mdformat-format
LINT_HOOKS := check-added-large-files check-json check-merge-conflict check-yaml ruff-check black-check prettier-check mdformat-check context-check-lite

.PHONY: fmt lint precommit-test test app-precommit-test app-test check ci build dev start accept accept-static accept-tests accept-build accept-smoke accept-fix fix-staged browser-profile-launch chrome-browser-profile-launch generate-native-roles verify-model-policy validate-lab promote-approved orchestrator-init orchestrator-status orchestrator-validate

fmt:
	@bash -euo pipefail -c '\
		for hook in $(FMT_HOOKS); do \
			pre-commit run --hook-stage manual "$$hook" --all-files; \
		done'

lint:
	@bash -euo pipefail -c '\
		for hook in $(LINT_HOOKS); do \
			SKIP=codex-autofix-fallback pre-commit run --hook-stage manual "$$hook" --all-files; \
		done'

precommit-test:
	@bash -euo pipefail -c '\
		if find tests -type f -name "test_*.py" -print -quit | grep -q .; then \
			python3 -m unittest discover -s tests -p "test_*.py"; \
		else \
			echo "precommit-test: skipping python unittest discovery (no test_*.py files)"; \
		fi'
	@$(MAKE) --no-print-directory app-precommit-test

test:
	@bash -euo pipefail -c '\
		if find tests -type f -name "test_*.py" -print -quit | grep -q .; then \
			python3 -m unittest discover -s tests -p "test_*.py"; \
		else \
			echo "test: skipping python unittest discovery (no test_*.py files)"; \
		fi'
	@$(MAKE) --no-print-directory app-test

ifneq ($(strip $(APP_PRECOMMIT_TEST_CMD)),)
app-precommit-test:
	@bash -euo pipefail -c '$(APP_PRECOMMIT_TEST_CMD)'
else ifneq ($(strip $(APP_TEST_CMD)),)
app-precommit-test:
	@bash -euo pipefail -c '$(APP_TEST_CMD)'
else
app-precommit-test:
	@echo "app-precommit-test: no pre-commit application test command configured"
endif

ifneq ($(strip $(APP_TEST_CMD)),)
app-test:
	@bash -euo pipefail -c '$(APP_TEST_CMD)'
else
app-test:
	@echo "app-test: no application test command configured"
endif

check: lint test

ci: check build

build:
	@bash -euo pipefail -c '\
		command="$(APP_BUILD_CMD)"; \
		if [[ -n "$$command" ]]; then \
			eval "$$command"; \
		else \
			echo "build: no application build command configured"; \
		fi'

dev:
	@bash -euo pipefail -c '\
		command="$(APP_DEV_CMD)"; \
		if [[ -n "$$command" ]]; then \
			eval "$$command"; \
		else \
			echo "dev: no application dev command configured"; \
		fi'

start:
	@bash -euo pipefail -c '\
		command="$(APP_START_CMD)"; \
		if [[ -n "$$command" ]]; then \
			eval "$$command"; \
		else \
			echo "start: no application start command configured"; \
		fi'

accept:
	@python3 scripts/accept_contract.py accept

accept-static:
	@python3 scripts/accept_contract.py static

accept-tests:
	@python3 scripts/accept_contract.py tests

accept-build:
	@python3 scripts/accept_contract.py build

accept-smoke:
	@python3 scripts/accept_contract.py smoke

accept-fix:
	@python3 scripts/accept_contract.py fix

fix-staged:
	@tools/git_precommit

browser-profile-launch:
	@python3 scripts/playwright_mcp_runtime.py launch-command --repo-root .

chrome-browser-profile-launch:
	@python3 scripts/chrome_devtools_mcp_runtime.py launch-command --repo-root .

generate-native-roles:
	@python3 repo-init-orchestrated/scripts/generate_native_roles.py --output-scope all

verify-model-policy:
	@python3 scripts/runtime_profiles.py verify-model-policy

validate-lab:
	@python3 scripts/promote_and_reseed.py --validate-only --output-json .orchestrator/validation_summary.json

promote-approved:
	@echo "promote-approved: run directly; do not wrap with tools/offload-proxy/pp because pp buffers progress until completion"
	@python3 scripts/promote_and_reseed.py

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
