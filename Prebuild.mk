#!/usr/bin/make -f

DEPS_INSTALL: ## Install required dependencies
	@poetry lock
	@poetry install --no-root
	@poetry run playwright install chromium
	@playwright install-deps
.PHONY: DEPS_INSTALL
