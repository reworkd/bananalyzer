#!/usr/bin/make -f

# Makefile for bananalyzer

CONFIG_FILE = config.ini
ifeq ($(OS),Windows_NT)
    CWD ?= "$(shell echo %CD%)"
    DOCKER ?= docker
else
    CWD ?= "$(shell pwd)"
    DOCKER ?= $(if $(shell docker -v 2>/dev/null),docker,podman)
endif
DOCKER_IMAGE_TAG ?= reworkd/bananalyzer
PORT ?= 8000

.DEFAULT_GOAL := help

help: ## Show this helpful message
	@for ML in $(MAKEFILE_LIST); do \
		grep -E '^[a-zA-Z_-]+:.*?## .*$$' $$ML | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'; \
	done
.PHONY: help

build_dev: ## Build development container
	@$(DOCKER) build -t $(DOCKER_IMAGE_TAG) .
PHONY: .build_dev

DEPS_INSTALL: ## Install required dependencies
	@poetry lock
	@poetry install --no-root
	@poetry run playwright install chromium
	@playwright install-deps
.PHONY: DEPS_INSTALL

dev: build_dev ## Run web server in a container
	@$(DOCKER) run \
		-it \
		--rm \
		-v "$(CWD)/bananalyzer:/src/$(DOCKER_IMAGE_TAG)/bananalyzer" \
		-v "$(CWD)/server:/src/$(DOCKER_IMAGE_TAG)/server" \
		-v "$(CWD)/static:/root/.bananalyzer_data" \
		-v "$(CWD)/tests:/src/$(DOCKER_IMAGE_TAG)/tests" \
		-p $(PORT):$(PORT) \
		$(DOCKER_IMAGE_TAG)
.PHONY: dev

DEV: ## Run web server
	@cd ./server/ && poetry lock
	@cd ./server/ && poetry install --no-root
	@cd ./server/ && uvicorn server:app --host 0.0.0.0
.PHONY: DEV

format_fix: build_dev ## Fix code formatting using Docker
	@$(DOCKER) run \
		-it \
		--rm \
		-v "$(CWD)/bananalyzer:/src/$(DOCKER_IMAGE_TAG)/bananalyzer" \
		-v "$(CWD)/server:/src/$(DOCKER_IMAGE_TAG)/server" \
		-v "$(CWD)/tests:/src/$(DOCKER_IMAGE_TAG)/tests" \
		$(DOCKER_IMAGE_TAG) \
		make FORMAT_FIX
.PHONY: format_fix

FORMAT_FIX: ## Fix code formatting
	@echo "Formatting code 🧹"
	@poetry run ruff check --fix
	@poetry run ruff format
.PHONY: FORMAT_FIX

format_check: build_dev ## Check code formatting using Docker
	@$(DOCKER) run \
		-it \
		--rm \
		-v "$(CWD)/bananalyzer:/src/$(DOCKER_IMAGE_TAG)/bananalyzer" \
		-v "$(CWD)/server:/src/$(DOCKER_IMAGE_TAG)/server" \
		-v "$(CWD)/tests:/src/$(DOCKER_IMAGE_TAG)/tests" \
		$(DOCKER_IMAGE_TAG) \
		make FORMAT_CHECK
.PHONY: format_check

FORMAT_CHECK: ## Check code formatting
	@echo "Checking code 🧹"
	@poetry run ruff check
	@poetry run ruff format --check
.PHONY: FORMAT_CHECK

run: build_dev ## Run in a container
	@$(DOCKER) run \
		-it \
		--rm \
		-v "$(CWD)/.git:/src/$(DOCKER_IMAGE_TAG)/.git" \
		-v "$(CWD)/bananalyzer:/src/$(DOCKER_IMAGE_TAG)/bananalyzer" \
		-v "$(CWD)/server:/src/$(DOCKER_IMAGE_TAG)/server" \
		-v "$(CWD)/static:/src/$(DOCKER_IMAGE_TAG)/static" \
		-v "$(CWD)/tests:/src/$(DOCKER_IMAGE_TAG)/tests" \
		$(DOCKER_IMAGE_TAG) \
		make RUN
.PHONY: run

RUN: ## Run
	@poetry install
	@poetry run bananalyze --headless .
.PHONY: RUN

test: build_dev ## Run tests in a container
	@$(DOCKER) run \
		-it \
		--rm \
		-v "$(CWD)/.git:/src/$(DOCKER_IMAGE_TAG)/.git" \
		-v "$(CWD)/bananalyzer:/src/$(DOCKER_IMAGE_TAG)/bananalyzer" \
		-v "$(CWD)/server:/src/$(DOCKER_IMAGE_TAG)/server" \
		-v "$(CWD)/static:/src/$(DOCKER_IMAGE_TAG)/static" \
		-v "$(CWD)/tests:/src/$(DOCKER_IMAGE_TAG)/tests" \
		$(DOCKER_IMAGE_TAG) \
		make TEST
.PHONY: test

TEST: ## Run tests
	@poetry install --only main
	@poetry run mypy .
	@poetry run pytest -vv .
.PHONY: TEST

shell: ## Enter Docker container's shell
	@$(DOCKER) run \
		-it \
		--rm \
		-v "$(CWD)/bananalyzer:/src/$(DOCKER_IMAGE_TAG)/bananalyzer" \
		-v "$(CWD)/server:/src/$(DOCKER_IMAGE_TAG)/server" \
		$(DOCKER_IMAGE_TAG) \
		bash || true
.PHONY: shell

update_lock_file: ## Update lock file(s)
	@$(DOCKER) run -it --rm $(DOCKER_IMAGE_TAG) base64 -w0 ./poetry.lock | base64 -d - > poetry.lock
	@$(DOCKER) run -it --rm $(DOCKER_IMAGE_TAG) base64 -w0 ./server/poetry.lock | base64 -d - > server/poetry.lock
.PHONY: update_lock_file
