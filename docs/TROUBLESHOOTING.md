# Troubleshooting Guide

Common issues when working with this repository and how to resolve them.

## Copilot Issues

### Copilot Hardcodes Table Names Instead of dbt Refs

**Problem:** Copilot writes SQL with literal table names like `analytics.raw.orders` instead of `{{ source() }}` or `{{ ref() }}`.

**Root Cause:** Copilot may not have dbt context or the dbt instructions aren't applied to the file.

**Solution:**
1. Ensure you're editing a `.sql` file under `models/` so `.github/instructions/dbt/dbt-sql.instructions.md` applies
2. Add an explicit prompt: "Use `{{ ref() }}` and `{{ source() }}` — never hardcode table names"
3. Reference the instruction file: "Follow dbt-sql.instructions.md"
4. Use the `/using-dbt-for-analytics-engineering` skill for model building

**Example — Before:**
```sql
select * from analytics.raw.orders  -- ❌ Hardcoded
```

**Example — After:**
```sql
select * from {{ source('raw', 'orders') }}  -- ✅ dbt lineage-aware
```

---

### Copilot Writes Code Without Tests

**Problem:** Copilot generates implementation code without writing tests first.

**Root Cause:** TDD isn't enforced in the request.

**Solution:**
1. Always start with: "Write a failing test first (TDD Red phase)"
2. Reference: `.github/instructions/workflows/tdd.instructions.md`
3. Example test in `tests/test_example.py`
4. For dbt models, use `/adding-dbt-unit-test` before writing SQL

**Correct Request Format:**
```
Write a failing test first for the staging model logic (Red phase).
Then implement minimal SQL to pass (Green phase).
Follow TDD pattern in .github/instructions/workflows/tdd.instructions.md
```

---

### Copilot Ignores Project Specifications

**Problem:** Copilot implements features that don't match `@docs/specs/spec.md`.

**Root Cause:** Spec not referenced in the request.

**Solution:**
1. Always reference `@docs/specs/spec.md`: "Implement per @docs/specs/spec.md section 2.1"
2. Paste spec requirements if not obvious
3. Ask Copilot to validate: "Verify this implementation matches @docs/specs/spec.md requirements exactly"

**Correct Request Format:**
```
Create staging models for the orders source per @docs/specs/spec.md section 2.1.
Requirements:
1. Use stg_<source>__<entity> naming
2. Add not_null and unique tests on primary key in schema.yml
3. Use {{ source() }} for raw tables
```

---

### Instructions Not Being Applied

**Problem:** Language-specific instructions (e.g., `dbt-sql.instructions.md`) aren't showing in Copilot Chat.

**Root Cause:** File not detected by Copilot or wrong file type open.

**Solution:**
1. Verify file exists under `.github/instructions/`
2. Check `applyTo` pattern matches your file (e.g., `**/*.sql` for dbt models)
3. Reload VS Code: `Cmd+Shift+P` → "Developer: Reload Window"
4. Wait up to 1 minute for changes to propagate
5. Attach file to chat: Right-click file → "Attach to Chat"

---

### dbt or Databricks MCP Server Not Connecting

**Problem:** Copilot agent mode can't query Unity Catalog or run dbt commands via MCP.

**Root Cause:** MCP server not configured or credentials missing.

**Solution:**
1. Follow `docs/AI_SETUP.md` — MCP setup section
2. Verify `.vscode/mcp.json` has your Databricks workspace URL and credentials filled in
3. For dbt MCP, ensure `DBT_PROJECT_DIR` and profiles are configured
4. Reload VS Code after editing MCP config
5. Check MCP server status in VS Code: Copilot Chat → agent mode → MCP tools panel

See also: `/configuring-dbt-mcp-server` skill in `.agents/skills/`

---

## Testing Issues

### Tests Not Running / Import Errors

**Problem:** `pytest` fails with import errors.

**Solution:**
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Verify `tests/` directory is in PYTHONPATH if needed:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   pytest
   ```

---

### Test Coverage Below 80%

**Problem:** Coverage report shows <80% (builds fail due to this).

**Solution:**
1. Check coverage report:
   ```bash
   pytest --cov=src --cov-report=html
   open htmlcov/index.html
   ```
2. Add tests for uncovered lines (shown in red)
3. Use fixtures from `tests/conftest.py` to reduce duplication

---

### Tests Failing After Refactoring

**Problem:** Tests break after refactoring code.

**Root Cause:** Tests are tightly coupled to implementation (not testing behavior).

**Solution:**
1. Verify tests test *behavior*, not *implementation*
2. Example — Bad test (too specific):
   ```python
   def test_transform_service():
       service = TransformService()
       assert service._cache == {}  # Testing internals ❌
   ```
3. Example — Good test (behavior):
   ```python
   def test_transform_normalizes_email():
       result = normalize_email("  User@Example.COM  ")
       assert result == "user@example.com"  # Testing behavior ✅
   ```

---

## Code Quality Issues

### Type Checker (Pyright) Complaining

**Problem:** `pyright` reports type errors.

**Solution:**
1. Add type hints to public functions
2. Run type checker: `pyright src/`
3. Fix errors or add `# pyright: ignore` if false positive

---

### Linter (Pylint) Complaints

**Problem:** `pylint` reports style or logic issues.

**Solution:**
1. Run linter: `pylint src/`
2. Fix issues: unused imports, line length (max 100 chars), missing docstrings
3. Ignore specific issues only when justified:
   ```python
   x = 5  # pylint: disable=unused-variable
   ```

---

### Black Formatter Conflicts

**Problem:** Black reformats code unexpectedly.

**Solution:**
1. Black is opinionated — let it reformat consistently
2. Configure in `pyproject.toml` if needed (`line-length = 100`)
3. Run before committing: `black src/ tests/`

---

## dbt Issues

### dbt compile / parse Failures

**Problem:** `dbt parse` or `dbt compile` fails with Jinja or ref errors.

**Solution:**
1. Run with debug output: `dbt compile --debug`
2. Verify `profiles.yml` points to the correct target
3. Ensure all `{{ ref() }}` and `{{ source() }}` targets exist
4. Check model file is in the correct directory for its layer (`staging/`, `intermediate/`, `marts/`)
5. Use `/using-dbt-for-analytics-engineering` or `/troubleshooting-dbt-job-errors` skills

---

### dbt Tests Failing in CI or Locally

**Problem:** `dbt test` reports failures on `not_null`, `unique`, or `relationships`.

**Solution:**
1. Run the failing test in isolation: `dbt test --select test_name`
2. Inspect the model SQL for nulls, duplicates, or broken foreign keys
3. Add tests incrementally — start with primary key `not_null` + `unique`
4. For TDD with dbt, use `/adding-dbt-unit-test` to define expected behavior before SQL

---

## Databricks Issues

### Authentication Failures

**Problem:** Databricks CLI or MCP server can't authenticate.

**Solution:**
1. Run `databricks auth login` and complete browser authentication
2. Verify workspace URL matches your organization's Databricks instance
3. For jobs/notebooks, use `dbutils.secrets.get()` — never hardcode tokens in source files
4. See `docs/AI_SETUP.md` and the `/databricks` skill for setup steps

---

### PySpark `.collect()` on Large DataFrames

**Problem:** Job runs out of memory or times out.

**Root Cause:** Copilot may suggest `.collect()` or `.toPandas()` on large datasets.

**Solution:**
1. Reference `.github/instructions/databricks/databricks.instructions.md`
2. Use `.show()`, `.limit()`, or write to Delta instead of collecting to driver
3. Prompt explicitly: "Never .collect() on large DataFrames — use DataFrame API with F.col()"

---

## Git / Commit Issues

### Commit Rejected: Test Coverage Below 80%

**Problem:** Pre-commit hook fails: "Tests must pass with 80% coverage"

**Solution:**
1. Run tests with coverage:
   ```bash
   pytest --cov=src --cov-fail-under=80
   ```
2. If it fails, add tests:
   ```bash
   pytest --cov=src --cov-report=html
   open htmlcov/index.html
   ```
3. Try commit again after fixing

---

### Unclear Commit Messages

**Problem:** PR rejected due to poor commit messages.

**Solution:**
Use Conventional Commits: `<type>: <description>`

**Valid types:** `feat`, `fix`, `docs`, `refactor`, `test`, `perf`, `chore`

**Examples:**
```bash
git commit -m "feat: add stg_raw__orders staging model"
git commit -m "fix: handle null order_id in int_orders"
git commit -m "docs: update dbt model naming ADR"
```

---

## Architecture Decision Issues

### Making a Decision That Contradicts an Existing ADR

**Problem:** You need to change an approach documented in an accepted ADR.

**Solution:**
1. Check existing ADRs in `docs/adr/`
2. Create a new ADR explaining why the change is needed
3. Mark the old ADR as **Superseded** with a link to the new one
4. Review with the team before implementing
5. Never silently violate architectural decisions

---

## Getting Help

**Still stuck?**

1. Check `docs/DEVELOPMENT.md` (development workflow)
2. Check `docs/AI_SETUP.md` (MCP and skills setup)
3. Check `.github/instructions/` (language-specific guidance)
4. Check `docs/adr/` (architectural decisions)
5. Review `tests/test_example.py` (Python testing patterns)
6. Browse skills in `.agents/skills/README.md`
7. Open an issue with reproduction steps

---

## Contributing to This Guide

Found a new issue? Add it here!

1. Add a section under the appropriate heading
2. Follow format: Problem → Root Cause → Solution
3. Include code examples where helpful
4. Reference relevant documents (ADRs, instructions, skills)
5. Submit a PR

---

**Last Updated:** 2026-06-07

**Maintained By:** [Team Lead]
