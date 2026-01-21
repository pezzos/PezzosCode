.PHONY: fmt lint test check docs-check skills-check ticket-check ticket ticket-ci ticket-verify ci

fmt:
	@echo "TODO: define formatting command (language/tooling TBD)"

lint:
	@tools/markdown-lint

test:
	@$(MAKE) skills-check
	@$(MAKE) docs-check
	@$(MAKE) ticket-check

ticket-check:
	@bash -euo pipefail -c '\
		root="docs/02-features"; \
		found=0; \
		while IFS= read -r -d "" file; do \
			found=1; \
			if ! rg -q "^## Risk Classification" "$$file"; then \
				echo "ticket-check: missing Risk Classification in $$file"; exit 1; \
			fi; \
			if ! rg -q "^- Risk level:" "$$file"; then \
				echo "ticket-check: missing Risk level in $$file"; exit 1; \
			fi; \
			if ! rg -q "^## Docs Updated" "$$file"; then \
				echo "ticket-check: missing Docs Updated section in $$file"; exit 1; \
			fi; \
		done < <(find "$$root" -type f -name "ticket-TASK-*.md" -print0); \
		if [[ "$$found" -eq 0 ]]; then \
			echo "ticket-check: no tickets found (ok)"; \
		else \
			echo "ticket-check: ok"; \
		fi'

ticket:
	@tools/ticket-bootstrap T=$(T)

ticket-verify:
	@tools/ticket-bootstrap T=$(T) --verify

ticket-ci:
	@tools/ticket-bootstrap T=$(T)
	@$(MAKE) ci

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
			if find "$$dir" -mindepth 1 -maxdepth 1 -type d | grep -q .; then \
				echo "skills-check: $$name has unexpected subdirectories"; \
				find "$$dir" -mindepth 1 -maxdepth 1 -type d -print; \
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

docs-check:
	@echo "docs-check covered by markdown lint"

check: fmt lint test
	@echo "TODO: replace with real checks once tooling is chosen"

ci: check
	@echo "ci: ok"
