# Development Guide

Welcome to the project! This guide helps both humans and AI agents (like Copilot) understand our development practices and keep code quality high.

## Core Development Philosophy

We practice **Spec-Driven Development (SDD)** and **Test-Driven Development (TDD)** to keep AI agents on the rails and ensure features are correctly implemented from conception.

### Spec-Driven Development (SDD)

Before writing any code, features must have a specification:

1. **Create `docs/specs/spec.md`** using the `create-spec` skill or manually from `docs/spec.template.md`
2. Include: Context, Requirements, Edge Cases, Success Criteria
3. Get approval before starting implementation

**Why:** The spec is the contract. AI agents must reference `@docs/specs/spec.md` to validate their suggestions align with requirements. Previous specs are archived automatically in `docs/specs/` with descriptive names.

### Test-Driven Development (TDD)

All features use the **Red-Green-Refactor** workflow:

1. **Red:** Write a failing test that defines desired behavior
2. **Green:** Write minimal code to make the test pass
3. **Refactor:** Improve code quality while tests stay passing

**Why:** TDD ensures requirements are met and prevents "golden hammer" solutions by AI agents. For dbt models, use the `/adding-dbt-unit-test` skill before writing SQL.

## Getting Started

### 1. Set Up Python Environment

```bash
make install
source venv/bin/activate
make test
```

This creates a virtual environment, installs dependencies, and registers pre-commit hooks.

### 2. Makefile Targets

| Target | Purpose |
|--------|---------|
| `make help` | List all commands |
| `make install` | Create venv, install deps, install pre-commit hooks |
| `make test` | Run pytest with ≥80% coverage |
| `make lint` | pylint + flake8 |
| `make format` | black |
| `make type-check` | pyright |
| `make all` | lint → format → type-check → test |
| `make pre-commit` | Run pre-commit on all files |
| `make dbt-*` | dbt commands (skip gracefully if no project) |
| `make databricks-*` | Databricks bundle commands (skip if no bundle) |

### 3. Understand the Structure

```
project/
├── .github/
│   ├── copilot-instructions.md      # Repository-wide AI guidance
│   ├── instructions/                # Path-specific AI guidance (dbt, Databricks, Python)
│   ├── pull_request_template.md     # GitHub PR template
│   └── workflows/ci.yml             # GitHub Actions CI
├── .agents/
│   └── skills/                      # Invocable Agent Skills (dbt, Databricks, SDD, TDD)
├── .vscode/
│   ├── settings.json                # VS Code settings (Python, Copilot)
│   └── extensions.json              # Recommended extensions
├── Makefile                         # Development commands
├── .pre-commit-config.yaml          # Pre-commit hooks
├── scripts/README.md                # Pointer to Makefile commands
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Python project configuration
├── docs/
│   ├── DEVELOPMENT.md               # This file
│   ├── AI_SETUP.md                  # MCP servers and skills setup
│   ├── TROUBLESHOOTING.md           # Common issues & solutions
│   ├── spec.template.md             # Template for feature specs
│   ├── specs/                       # Feature specifications
│   │   ├── spec.md                  # Current active spec
│   │   └── *.md                     # Archived previous specs
│   └── adr/                         # Architecture Decision Records
├── tests/
│   ├── test_example.py              # Reference TDD pattern
│   └── conftest.py                  # Shared pytest fixtures (create if needed)
└── src/                             # Python utilities and orchestration code
```

### 4. Review Relevant Guidelines

**For all developers:**
- Read `.github/copilot-instructions.md` (repository-wide rules)
- Read `docs/AI_SETUP.md` (MCP servers and skills)
- Read `docs/adr/` (architectural decisions — create your own as the project grows)
- Check `.vscode/settings.json` and `.vscode/extensions.json`

**For your stack:**

| Role | Read |
|------|------|
| **Python utilities / orchestration** | `.github/instructions/python/python-general.instructions.md` |
| **dbt models & tests** | `.github/instructions/dbt/dbt-sql.instructions.md` |
| **Databricks / PySpark** | `.github/instructions/databricks/databricks.instructions.md` |
| **TDD workflow** | `.github/instructions/workflows/tdd.instructions.md` |
| **Invocable skills** | `.agents/skills/README.md` |

## Development Workflow

### Creating a New Feature

```bash
# 1. Create specification (use create-spec skill or copy template)
cp docs/spec.template.md docs/specs/spec.md
# Edit with requirements, edge cases, success criteria

# 2. Get approval (team review)
# [ ] Spec reviewed and approved

# 3. Create feature branch
git checkout -b feature/your-feature-name

# 4. Write test first (Red phase)
# Python: see tests/test_example.py
# dbt: use /adding-dbt-unit-test skill
pytest tests/test_your_feature.py -v

# 5. Implement to pass test (Green phase)
# Follow instructions in .github/instructions/

# 6. Refactor for quality (Refactor phase)
# Use /refactor-python skill for Python code

# 7. Verify spec alignment
# Manual check: Does code match docs/specs/spec.md exactly?

# 8. Commit with clear message
git add .
git commit -m "feat: description following conventional commits"

# 9. Push and create PR
git push origin feature/your-feature-name
# See .github/pull_request_template.md for PR checklist
```

### Using Copilot Effectively

**Copilot Skills** (invoke with `/` in Copilot Chat):

| Skill | Purpose |
|-------|---------|
| `/create-spec` | Generate feature specifications (SDD) |
| `/create-tasks` | Break a spec into executable tasks |
| `/using-dbt-for-analytics-engineering` | Build and debug dbt models |
| `/adding-dbt-unit-test` | TDD for dbt SQL |
| `/databricks` | CLI auth, jobs, Asset Bundles |
| `/audit-security` | Security audit |
| `/refactor-python` | Refactor Python code |
| `/generate-prompt` | Generate reusable prompts |
| `/run-prompt` | Execute saved prompts |

See `.agents/skills/README.md` for the full list.

**Requesting Features from Copilot:**

```
✅ GOOD:
Create a dbt staging model for the orders source per @docs/specs/spec.md section 2.1.
Use /adding-dbt-unit-test first (TDD). Follow dbt-sql.instructions.md.

❌ BAD:
Write a SQL query for orders.
```

**Keeping Copilot on Rails:**

Always include:
1. Reference to `@docs/specs/spec.md` (if applicable)
2. Expected stack (dbt, Databricks/PySpark, Python)
3. TDD requirement (write tests first)
4. Acceptance criteria

## Code Quality Standards

### Type Hints (Python)
- **Required for all public functions and methods**
- Use `typing` module for complex types

### Testing
- **Minimum coverage: 80%** for Python code in `src/` (configured in `pyproject.toml`)
- Use `pytest` for Python; dbt tests in `schema.yml` for SQL models
- Follow test pattern in `tests/test_example.py`

### Line Length
- **Python and SQL:** Maximum 100 characters

### Documentation
- **Docstrings required** for Python modules, classes, and public functions
- **Column and model docs** required in dbt `schema.yml`

### Security
- **No hardcoded secrets** — use environment variables or `dbutils.secrets.get()`
- **Parameterized queries only** — never string concatenation for SQL
- **No eval() or exec()**
- **Use `{{ ref() }}` and `{{ source() }}`** in dbt — never hardcode table names

## Running Tests

```bash
# Python tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test
pytest tests/test_specific.py::test_function

# dbt tests (when dbt project exists)
dbt test
```

## Pre-commit Hooks

Pre-commit hooks are configured in `.pre-commit-config.yaml` and installed by `make install`.

```bash
make pre-commit          # Run all hooks manually
make install-hooks       # Re-install hooks after cloning
```

## Code Review Checklist

Before submitting a PR, ensure:
- [ ] Tests written first (Red phase complete)
- [ ] All tests passing
- [ ] Code follows instructions in `.github/instructions/`
- [ ] `docs/specs/spec.md` alignment verified (if feature-related)
- [ ] Type hints on Python functions
- [ ] No hardcoded secrets or credentials
- [ ] dbt models have schema tests (if applicable)
- [ ] Commits follow conventional commits format

See `.github/pull_request_template.md` for the full PR checklist.

## Architecture Decisions

Major architecture decisions are recorded in `docs/adr/` using ADR format.

When making significant technical decisions:
1. Check existing ADRs to understand context
2. Create a new ADR following `docs/adr/adr.template.md`
3. Reference relevant ADRs in your implementation

Suggested first ADRs for data engineering projects are listed in `docs/adr/README.md`.

## Troubleshooting

Having issues with Copilot guidance? See `docs/TROUBLESHOOTING.md` for common problems and solutions.

## Additional Resources

- **Agent Skills:** `.agents/skills/README.md`
- **Custom Instructions:** `.github/instructions/README.md`
- **AI Setup (MCP):** `docs/AI_SETUP.md`
- **Architecture Decisions:** `docs/adr/`
- **Spec Template:** `docs/spec.template.md`
- **Test Example:** `tests/test_example.py`

---

**Questions?** Check the relevant guide above or open an issue for clarification.
