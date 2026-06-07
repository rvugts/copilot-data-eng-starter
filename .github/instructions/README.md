# GitHub Copilot Custom Instructions

This directory contains path-specific custom instructions for GitHub Copilot. These instructions guide Copilot's responses and code generation to follow your project's conventions and best practices.

## What Are Custom Instructions?

Custom instructions are files that provide Copilot with additional context and guidance on how to work with your codebase. They use GitHub's custom instructions format with glob patterns via YAML frontmatter.

**Copilot automatically applies relevant instructions based on the file you're working on.**

## Directory Structure

```
.github/instructions/
├── python/
│   └── python-general.instructions.md       # TDD, SSD, quality, tooling, data-eng conventions
├── databricks/
│   └── databricks.instructions.md           # PySpark, Delta Lake, Unity Catalog standards
├── dbt/
│   └── dbt-sql.instructions.md              # dbt & SQL development standards
└── workflows/
    └── tdd.instructions.md                  # Test-Driven Development workflow
```

## How It Works

Each `.instructions.md` file contains:

1. **YAML Frontmatter:** Specifies which files the instructions apply to using glob patterns
   ```yaml
   ---
   applyTo: "**/*.py"
   excludeAgent: "code-review"  # Optional: exclude from specific agents
   ---
   ```

2. **Markdown Content:** Natural language guidelines and best practices

### Pattern Matching Examples

| Pattern | Matches |
|---------|---------|
| `**/*.py` | All Python files in all directories |
| `**/*.sql` | All SQL files (e.g. dbt models) |
| `**/schema.yml` | dbt schema files |
| `models/**/*.yml` | YAML files inside dbt model directories |

## Available Instructions

### Python Instructions

#### [python-general.instructions.md](python/python-general.instructions.md)
Applies to: All `.py` files

Covers:
- Test-Driven Development (TDD) with pytest
- Spec-Driven Development (SDD)
- Type hints, Pydantic validation, and pydantic-settings
- Code structure, naming, imports, and formatting
- Error handling, logging, and secrets management
- Data engineering conventions (pathlib, pure transforms, reproducibility)
- Tooling alignment (black, flake8, pylint, pyright, pytest)
- Security best practices
- Verification checklist

### Databricks Instructions

#### [databricks.instructions.md](databricks/databricks.instructions.md)
Applies to: Python files (`**/*.py`), notebooks, job scripts, pipeline source files

Covers:
- PySpark DataFrame API (always use `F.col()`, never RDDs)
- Performance anti-patterns (never `.collect()` on large data, no `.toPandas()` at scale)
- Delta Lake write patterns (overwrite, append, MERGE/UPSERT)
- Secrets management (`dbutils.secrets.get()` — never hardcode credentials)
- Databricks widgets for job parameters
- Unity Catalog three-part naming (`catalog.schema.table`)
- Partitioning, Z-ORDER, and OPTIMIZE patterns
- PySpark testing with `chispa`

### dbt & SQL Instructions

#### [dbt-sql.instructions.md](dbt/dbt-sql.instructions.md)
Applies to: All `.sql` files; `schema.yml`, `sources.yml`, `dbt_project.yml`; YAML files inside `models/`, `macros/`, `seeds/`, `snapshots/`, and `analyses/` directories.

> **Note on YAML scope:** The `applyTo` pattern deliberately excludes `**/*.yml` to avoid applying dbt rules to unrelated YAML files (GitHub Actions workflows, Docker Compose, etc.). Only well-known dbt filenames and YAML files nested inside standard dbt directories are targeted.

Covers:
- SQL style (lowercase keywords, trailing commas, CTEs over subqueries)
- dbt model naming conventions (`stg_<source>__<entity>`, `int_`, `fct_`, `dim_`, `rpt_`)
- Standard model structure (import CTEs → transformation CTEs → `final`)
- dbt testing standards (`not_null`, `unique`, `relationships`, `accepted_values`)
- Column-level documentation in `schema.yml`
- Macros and packages (`dbt_utils`, `dbt_expectations`, `codegen`)
- Materialization strategy per layer
- Data types and precision (no `float` for money)
- PII security and source freshness configuration
- Anti-patterns to avoid

### Workflow Instructions

#### [tdd.instructions.md](workflows/tdd.instructions.md)
Applies to: All `.py` files (workflow approach)

Covers:
- Red-Green-Refactor cycle
- Test structure (Arrange-Act-Assert)
- Testing tools (pytest)
- Test coverage
- Continuous Integration practices

## Using Custom Instructions

### Automatic Application

Copilot automatically applies matching instructions when you:
- Work in a file that matches the `applyTo` pattern
- Ask Copilot Chat questions with the file as context
- Use Copilot code suggestions in matching files

### In Copilot Chat

When using Copilot Chat, relevant instructions are automatically included in your requests. You'll see them referenced in the response (check the References section).

### Enabling/Disabling

Custom instructions are **enabled by default** for Copilot code generation, Copilot Chat, and Copilot code review.

## Creating/Modifying Instructions

### Adding a New Instruction File

1. Create a new `.instructions.md` file in the appropriate subdirectory
2. Add YAML frontmatter with `applyTo` pattern:
   ```yaml
   ---
   applyTo: "**/*.ext"
   ---
   ```
3. Write your instructions in Markdown
4. Commit and push to your repository

### Best Practices for Instructions

- **Conciseness:** Keep instructions focused and actionable
- **Specificity:** Be specific about expectations and patterns
- **Examples:** Include code examples when helpful
- **Avoid Conflicts:** Don't have conflicting instructions for the same file type

## Instruction Priorities

When multiple instruction files apply, they're all used together:
1. **Path-specific instructions** (most specific pattern)
2. **Repository-wide instructions** (`.github/copilot-instructions.md`)
3. **Organization-wide instructions** (if configured)

## Examples in Action

### Example 1: Python Utility

When working on `src/utils/transform.py`, Copilot applies:
- ✅ `python/python-general.instructions.md` (matches `**/*.py`)
- ✅ `workflows/tdd.instructions.md` (matches `**/*.py`)

### Example 2: dbt Staging Model

When working on `models/staging/stg_raw__orders.sql`, Copilot applies:
- ✅ `dbt/dbt-sql.instructions.md` (matches `**/*.sql`)

When working on `models/staging/schema.yml`, Copilot applies:
- ✅ `dbt/dbt-sql.instructions.md` (matches `**/schema.yml`)

### Example 3: PySpark Job Script

When working on `jobs/ingest_orders.py`, Copilot applies:
- ✅ `python/python-general.instructions.md` (matches `**/*.py`)
- ✅ `databricks/databricks.instructions.md` (matches `**/*.py`)
- ✅ `workflows/tdd.instructions.md` (matches `**/*.py`)

## Agent Skills

For multi-step workflows (building dbt models, deploying Databricks jobs, creating specs), use **Agent Skills** in `.agents/skills/`. Skills are invoked on demand with `/skill-name` in Copilot Chat. See `.agents/skills/README.md`.

## Troubleshooting

### Instructions Not Being Used

**Problem:** Custom instructions aren't showing in Copilot Chat references

**Solutions:**
1. Ensure the `.instructions.md` file exists in `.github/instructions/`
2. Check that the `applyTo` glob pattern matches your file
3. File must be in context (attached to chat or open in editor)
4. Reload VS Code if changes don't appear

### Conflicting Instructions

**Problem:** Different instructions give conflicting guidance

**Solutions:**
1. Review both instruction files for conflicts
2. Use more specific `applyTo` patterns
3. Consider merging related instructions

## Further Resources

- [GitHub Docs: Custom Instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills in this repo](../../.agents/skills/README.md)
