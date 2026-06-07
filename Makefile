.PHONY: help install install-hooks test test-watch lint format type-check pre-commit clean all \
        dbt-deps dbt-parse dbt-compile dbt-run dbt-test dbt-build \
        databricks-validate databricks-deploy databricks-run

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PRE_COMMIT := $(VENV)/bin/pre-commit

DBT_PROJECT := $(wildcard dbt_project.yml dbt/dbt_project.yml)
DATABRICKS_BUNDLE := $(wildcard databricks.yml)

# ── Setup ─────────────────────────────────────────────────────────────────────

help:
	@echo "Copilot Data Engineering Starter"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Create venv, install deps, install pre-commit hooks"
	@echo "  make install-hooks  Install pre-commit hooks only"
	@echo ""
	@echo "Python:"
	@echo "  make test           Run tests with coverage (≥80%)"
	@echo "  make test-watch     Run tests in watch mode"
	@echo "  make lint           Run pylint and flake8"
	@echo "  make format         Format with black"
	@echo "  make type-check     Run pyright"
	@echo "  make pre-commit     Run all pre-commit checks"
	@echo "  make all            lint → format → type-check → test"
	@echo "  make clean          Remove caches and build artifacts"
ifneq ($(DBT_PROJECT),)
	@echo ""
	@echo "dbt (project detected):"
	@echo "  make dbt-deps       Install dbt package dependencies"
	@echo "  make dbt-parse      Parse dbt project"
	@echo "  make dbt-compile    Compile dbt models"
	@echo "  make dbt-run        Run dbt models"
	@echo "  make dbt-test       Run dbt tests"
	@echo "  make dbt-build      Run dbt build"
else
	@echo ""
	@echo "dbt (no dbt_project.yml — targets skip gracefully):"
	@echo "  make dbt-parse      Run after: dbt init"
endif
ifneq ($(DATABRICKS_BUNDLE),)
	@echo ""
	@echo "Databricks (bundle detected):"
	@echo "  make databricks-validate   Validate Asset Bundle"
	@echo "  make databricks-deploy     Deploy bundle"
	@echo "  make databricks-run        Run job (set JOB=name)"
else
	@echo ""
	@echo "Databricks (no databricks.yml — targets skip gracefully):"
	@echo "  make databricks-validate   Run after adding databricks.yml"
endif
	@echo ""

install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "📦 Creating virtual environment..."; \
		python3 -m venv $(VENV); \
	fi
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	$(PRE_COMMIT) install
	@echo ""
	@echo "✅ Install complete. Activate the environment:"
	@echo "   source $(VENV)/bin/activate"

install-hooks:
	$(PRE_COMMIT) install

# ── Python ────────────────────────────────────────────────────────────────────

test:
	$(VENV)/bin/pytest --cov=src --cov-fail-under=80 --cov-report=html tests/
	@echo ""
	@echo "✅ Coverage report: open htmlcov/index.html"

test-watch:
	$(VENV)/bin/pytest-watch tests/ -- --maxfail=1 -v

lint:
	@echo "🎨 Linting with pylint..."
	-$(VENV)/bin/pylint src/ --disable=fixme --exit-zero
	@echo "🎨 Linting with flake8..."
	-$(VENV)/bin/flake8 src/ tests/

format:
	@echo "🖌️  Formatting with black..."
	$(VENV)/bin/black src/ tests/ scripts/
	@echo "✅ Code formatted"

type-check:
	@echo "🔎 Type checking with pyright..."
	$(VENV)/bin/pyright src/
	@echo "✅ Type checking passed"

pre-commit:
	$(PRE_COMMIT) run --all-files

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.py[cod]" -delete
	rm -rf .pytest_cache/ .coverage .mypy_cache/ .ruff_cache/ htmlcov/
	@echo "✅ Cleaned up cache files"

all: lint format type-check test
	@echo "✅ All checks passed!"

dbt-deps:
	@if [ -z "$(DBT_PROJECT)" ]; then \
		echo "⏭️  Skipping: no dbt_project.yml found. Run 'dbt init' to add a dbt project."; \
	else \
		dbt deps; \
	fi

dbt-parse:
	@if [ -z "$(DBT_PROJECT)" ]; then \
		echo "⏭️  Skipping: no dbt_project.yml found. Run 'dbt init' to add a dbt project."; \
	else \
		dbt parse; \
	fi

dbt-compile:
	@if [ -z "$(DBT_PROJECT)" ]; then \
		echo "⏭️  Skipping: no dbt_project.yml found. Run 'dbt init' to add a dbt project."; \
	else \
		dbt compile; \
	fi

dbt-run:
	@if [ -z "$(DBT_PROJECT)" ]; then \
		echo "⏭️  Skipping: no dbt_project.yml found. Run 'dbt init' to add a dbt project."; \
	else \
		dbt run; \
	fi

dbt-test:
	@if [ -z "$(DBT_PROJECT)" ]; then \
		echo "⏭️  Skipping: no dbt_project.yml found. Run 'dbt init' to add a dbt project."; \
	else \
		dbt test; \
	fi

dbt-build:
	@if [ -z "$(DBT_PROJECT)" ]; then \
		echo "⏭️  Skipping: no dbt_project.yml found. Run 'dbt init' to add a dbt project."; \
	else \
		dbt build; \
	fi

# ── Databricks (opt-in) ───────────────────────────────────────────────────────

databricks-validate:
	@if [ -z "$(DATABRICKS_BUNDLE)" ]; then \
		echo "⏭️  Skipping: no databricks.yml found. Add a Databricks Asset Bundle to enable these targets."; \
	else \
		databricks bundle validate; \
	fi

databricks-deploy:
	@if [ -z "$(DATABRICKS_BUNDLE)" ]; then \
		echo "⏭️  Skipping: no databricks.yml found. Add a Databricks Asset Bundle to enable these targets."; \
	else \
		databricks bundle deploy; \
	fi

databricks-run:
	@if [ -z "$(DATABRICKS_BUNDLE)" ]; then \
		echo "⏭️  Skipping: no databricks.yml found. Add a Databricks Asset Bundle to enable these targets."; \
	else \
		databricks bundle run $(JOB); \
	fi
