.PHONY: fmt lint test check docs-check

fmt:
	@echo "TODO: define formatting command (language/tooling TBD)"

lint:
	@tools/markdown-lint

test:
	@echo "TODO: define test command (language/tooling TBD)"

docs-check:
	@echo "docs-check covered by markdown lint"

check: fmt lint test docs-check
	@echo "TODO: replace with real checks once tooling is chosen"
