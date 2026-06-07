# Copilot Data Engineering Starter

A comprehensive starter template for data engineers using **dbt**, **Databricks**, and **Python** with AI-assisted development. Includes Copilot agent instructions, skills, MCP server configs, and workflows supporting Specification-Driven Development (SDD) and Test-Driven Development (TDD).

This repository provides:
- GitHub Copilot agent rules and instructions in `.github/` tuned for dbt, Databricks, and PySpark
- Copilot skills for secure coding, spec creation, task decomposition, refactoring, and testing
- Templates and docs supporting Specification-Driven Development (SDD) and Test-Driven Development (TDD)
- Architecture Decision Records in `docs/adr/`

## Key files

- `LICENSE.md` — project license
- `README.md` — project overview
- `CONTRIBUTING.md` — guidelines for extending the template
- `docs/GITHUB_TEMPLATE.md` — maintainer guide (GitHub topics, social preview, template settings)
- `CODE_OF_CONDUCT.md` — community standards
- `requirements.txt` — Python dependencies for development and testing
- `pyproject.toml` — Python project configuration and tool settings
- `docs/DEVELOPMENT.md` — development workflow and standards
- `docs/AI_SETUP.md` — **start here** — skills and MCP server setup for dbt and Databricks
- `docs/specs/` — SDD specs (`spec.md` when active); see `example-stg-orders-models.spec.md`
- `dbt/README.md` — where and how to add a dbt project
- `databricks/README.md` — where and how to add a Databricks Asset Bundle
- `.env.example` — environment variable template (copy to `.env`)
- `docs/TROUBLESHOOTING.md` — common issues and fixes
- `docs/VIBE_CODING_GUIDE.md` — contributor guide and Copilot best practices
- `.github/copilot-instructions.md` — repository-wide Copilot guidance
- `.github/instructions/` — always-on instruction files: dbt SQL style, Databricks/PySpark, Python
- `.agents/skills/` — invocable skills (Agent Skills standard): dbt analytics engineering, dbt unit tests, Databricks, spec/task workflows
- `Makefile` — development commands (`make install`, `make test`, optional dbt/Databricks targets)
- `.pre-commit-config.yaml` — pre-commit hook definitions
- `.github/workflows/ci.yml` — GitHub Actions CI
- `.vscode/mcp.json` — MCP server configuration for Databricks and dbt (template — fill in your credentials)
- `.vscode/settings.json` — shared VS Code settings
- `.vscode/extensions.json` — recommended VS Code extensions

## Getting started

### Install this template for a new project

For a new project, do not simply clone this repository and keep its `.git` history. That would link your project to the template repo and pollute your own commit history.

Use one of these approaches instead:

- **Create a new repo from this template on GitHub:** This repository is configured as a GitHub template, so use the **Use this template** button to create a fresh repo when your organization allows creating new repos on GitHub.
- **Download the repository archive:** Download the ZIP from GitHub, extract it into a new project folder, then initialize your own git repository.
- **Clone then reinitialize git:** If you need a local-only start, clone locally, delete the `.git` folder, and run `git init` inside the new project directory before making your first commit.

Example:

```bash
git clone https://github.com/<owner>/copilot-data-eng-starter.git my-new-project
cd my-new-project
rm -rf .git
git init
```

### Start using the template

1. **Read the AI Setup Guide:** Start with `docs/AI_SETUP.md` to configure MCP servers and skills for dbt and Databricks
2. **Set up Python:** `make install` then `make test`
3. **Configure MCP servers:** Copy `.env.example` to `.env`, edit `.vscode/mcp.json`, follow `docs/AI_SETUP.md`
4. Review `.github/copilot-instructions.md` — repository-wide Copilot guidance
5. Read `docs/DEVELOPMENT.md` for workflow and quality standards
6. Create a spec for your feature using the `/create-spec` skill
7. Use the dbt and Databricks skills in `.agents/skills/` as needed

## Stack

This template is purpose-built for data engineering teams working with:

| Tool | Purpose |
|------|---------|
| **dbt** | SQL transformation layer — models, tests, documentation |
| **Databricks** | Unified analytics platform — notebooks, jobs, workflows |
| **PySpark** | Distributed data processing in Python |
| **Python** | Orchestration, utilities, custom transforms |

## AI Tooling Included

### Skills (invocable workflows)

| Skill | Invoke | Purpose |
|-------|--------|---------|
| `using-dbt-for-analytics-engineering` | `/using-dbt-for-analytics-engineering` | Build models, write SQL, discover data, debug errors |
| `adding-dbt-unit-test` | `/adding-dbt-unit-test` | TDD for dbt — unit tests before SQL implementation |
| `databricks` | `/databricks` | CLI auth, Unity Catalog, job deployment, Asset Bundles |
| `create-spec` | `/create-spec` | Spec-Driven Development — write a feature specification |
| `create-tasks` | `/create-tasks` | Break a spec into ordered executable tasks |
| `audit-security` | `/audit-security` | Security audit of the codebase |
| `refactor-python` | `/refactor-python` | Python refactoring with engineering best practices |

### MCP Servers (live workspace access)

| Server | What it unlocks |
|--------|----------------|
| **Databricks Managed MCP** | Query Unity Catalog tables, execute SQL, browse schemas — live from the editor |
| **dbt MCP** (local) | Run dbt commands, explore lineage, query the Semantic Layer from Copilot Chat |

See `docs/AI_SETUP.md` for full configuration instructions.

### Instruction Files (always-on style enforcement)

| File | Applies to | Enforces |
|------|-----------|---------|
| `dbt-sql.instructions.md` | `.sql` files, `schema.yml` | SQL style, model naming, test conventions |
| `databricks.instructions.md` | Python files | PySpark DataFrame API, Delta patterns, secrets |
| `python-general.instructions.md` | All `.py` files | Type hints, TDD, security, docstrings |

## Specification-Driven Development

This template supports SDD — every feature starts with a specification that serves as the contract between requirements and implementation.

**Quick start:**
1. Ask Copilot to use the `create-spec` skill, or invoke `/create-spec`
2. Answer the guided questions about your feature
3. The skill writes `docs/specs/spec.md` (archiving any previous active spec using its frontmatter `name`), aligned with `docs/spec.template.md`
4. Use the `create-tasks` skill (or invoke `/create-tasks`) to decompose the spec into an ordered, executable task list at `docs/specs/tasks.md`
5. Work through the tasks in order — write tests first (TDD), then implement
6. Use `/generate-prompt` and `/run-prompt` to delegate individual tasks to Copilot agents

The `create-spec` and `create-tasks` skills support Python, Databricks/PySpark/SQL, dbt, and other stacks. See `.agents/skills/` for details.

## Contributing

This repository is intended as a starting point for Copilot-powered data engineering projects. If you want to extend the template:
- Add new `docs/` templates for your workflow
- Add new skills in `.agents/skills/`
- Keep the root docs and license up to date
