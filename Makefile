.PHONY: fmt fmt-verbose lint lint-verbose test check docs-check skills-check skills-metadata-check feature feature-help feature-status ci

fmt:
	@tools/pc-hooks-run --hook-stage manual --all-files

fmt-verbose:
	@tools/pc-hooks-run --hook-stage manual --all-files --verbose

lint:
	@tools/pc-hooks-run --hook-stage pre-commit --all-files

lint-verbose:
	@tools/pc-hooks-run --hook-stage pre-commit --all-files --verbose

test:
	@python -m unittest discover -s tests -p "test_*.py"
	@$(MAKE) skills-check
	@$(MAKE) skills-metadata-check
	@$(MAKE) docs-check

feature:
	@if [[ "$(HELP)" == "1" || "$(HELP)" == "true" || "$(HELP)" == "yes" ]]; then \
		tools/pc-feature --help; \
	else \
		tools/pc-feature F=$(F) MANUAL=$(MANUAL); \
	fi

feature-help:
	@tools/pc-feature --help

feature-status:
	@args=""; \
	if [ -n "$(WI)" ]; then args="$$args --wi $(WI)"; fi; \
	if [ -n "$(ROOT)" ]; then args="$$args --root $(ROOT)"; fi; \
	if [ "$(HISTORY)" = "1" ] || [ "$(HISTORY)" = "true" ]; then args="$$args --history"; fi; \
	if [ "$(FOLLOW)" = "1" ] || [ "$(FOLLOW)" = "true" ]; then args="$$args --follow"; fi; \
	if [ -n "$(LIMIT)" ]; then args="$$args --limit $(LIMIT)"; fi; \
	if [ -n "$(INTERVAL)" ]; then args="$$args --interval $(INTERVAL)"; fi; \
	tools/pc-feature-status $$args

skills-check:
	@bash -euo pipefail -c '\
		root=".codex/skills"; \
		if [[ ! -d "$$root" ]]; then \
			echo "skills-check: missing $$root"; exit 1; \
		fi; \
		if find "$$root" -maxdepth 1 -type f | grep -q .; then \
			echo "skills-check: unexpected files in $$root"; \
			find "$$root" -maxdepth 1 -type f -print; \
			exit 1; \
		fi; \
		for dir in "$$root"/*; do \
			[[ -d "$$dir" ]] || continue; \
			name="$${dir##*/}"; \
			if [[ ! -f "$$dir/SKILL.md" ]]; then \
				echo "skills-check: $$name missing SKILL.md"; exit 1; \
			fi; \
			if find "$$dir" -mindepth 1 -maxdepth 1 -type f ! -name SKILL.md | grep -q .; then \
				echo "skills-check: $$name has extra files"; \
				find "$$dir" -mindepth 1 -maxdepth 1 -type f ! -name SKILL.md -print; \
				exit 1; \
			fi; \
			if find "$$dir" -mindepth 1 -maxdepth 1 -type d ! \( -name agents -o -name scripts -o -name references -o -name assets \) | grep -q .; then \
				echo "skills-check: $$name has unexpected subdirectories"; \
				find "$$dir" -mindepth 1 -maxdepth 1 -type d ! \( -name agents -o -name scripts -o -name references -o -name assets \) -print; \
				exit 1; \
			fi; \
			if [[ -d "$$dir/agents" ]]; then \
				if [[ ! -f "$$dir/agents/openai.yaml" ]]; then \
					echo "skills-check: $$name missing agents/openai.yaml"; \
					exit 1; \
				fi; \
				if find "$$dir/agents" -mindepth 1 -maxdepth 1 -type f ! -name openai.yaml | grep -q .; then \
					echo "skills-check: $$name has unexpected files in agents"; \
					find "$$dir/agents" -mindepth 1 -maxdepth 1 -type f ! -name openai.yaml -print; \
					exit 1; \
				fi; \
				if find "$$dir/agents" -mindepth 1 -maxdepth 1 -type d | grep -q .; then \
					echo "skills-check: $$name has unexpected subdirectories in agents"; \
					find "$$dir/agents" -mindepth 1 -maxdepth 1 -type d -print; \
					exit 1; \
				fi; \
			fi; \
			if [[ -f "$$dir/openai.yaml" ]]; then \
				echo "skills-check: $$name openai.yaml must be under agents/"; \
				exit 1; \
			fi; \
			if [[ "$$(sed -n "1p" "$$dir/SKILL.md")" != "---" ]]; then \
				echo "skills-check: $$name SKILL.md missing frontmatter start"; exit 1; \
			fi; \
			if [[ "$$(sed -n "2p" "$$dir/SKILL.md")" != name:\ * ]]; then \
				echo "skills-check: $$name SKILL.md missing name in line 2"; exit 1; \
			fi; \
			if [[ "$$(sed -n "3p" "$$dir/SKILL.md")" != description:\ * ]]; then \
				echo "skills-check: $$name SKILL.md missing description in line 3"; exit 1; \
			fi; \
			if [[ "$$(sed -n "4p" "$$dir/SKILL.md")" != "---" ]]; then \
				echo "skills-check: $$name SKILL.md missing frontmatter end on line 4"; exit 1; \
			fi; \
			skill_name="$$(sed -n "2s/^name:[[:space:]]*//p" "$$dir/SKILL.md")"; \
			if [[ "$$skill_name" != "$$name" ]]; then \
				echo "skills-check: $$name SKILL.md name mismatch ($$skill_name)"; exit 1; \
			fi; \
			skill_desc="$$(sed -n "3s/^description:[[:space:]]*//p" "$$dir/SKILL.md")"; \
			if [[ -z "$$skill_desc" || "$$skill_desc" == *TODO* ]]; then \
				echo "skills-check: $$name SKILL.md description missing or TODO"; exit 1; \
			fi; \
		done; \
		echo "skills-check: ok"'

skills-metadata-check:
	@python3 -S tools/pc-skills-metadata-check

docs-check:
	@tools/pc-devtasks-schema-check

check: lint test

ci: check
