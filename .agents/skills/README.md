# Agent Skills

Skills are **on-demand playbooks** for GitHub Copilot, Cursor, Claude, and other
[Agent Skills](https://agentskills.io)-compatible assistants. Each skill is a folder with a
`SKILL.md` file that tells the agent *how* to run a multi-step workflow — not just style rules,
but procedures, checklists, and references.

This repo ships skills at `.agents/skills/` (project scope). Copilot also reads personal skills
from `~/.agents/skills/` or `~/.copilot/skills/`.

## What skills add (vs instructions and MCP)

If you have not used Agent Skills before, think of three layers working together:

| Layer | When it runs | What it adds |
|-------|--------------|--------------|
| **Instruction files** (`.github/instructions/`) | Always on while you edit matching files | Coding style — SQL formatting, PySpark patterns, TDD habits |
| **Skills** (this directory) | When you or Copilot invoke them | Multi-step workflows — plan a model, write unit tests first, deploy a bundle, diagnose a failed job |
| **MCP servers** (`.vscode/mcp.json`) | Agent mode, when connected | Live access — query Unity Catalog, run `dbt show`, browse lineage |

**Example:** Building a staging model

1. Instructions enforce `stg_<source>__<entity>` naming and CTE structure as you type.
2. `/using-dbt-for-analytics-engineering` plans the model, writes SQL + `schema.yml`, and uses `dbt show` to validate.
3. The dbt MCP server lets Copilot preview results without leaving VS Code.

See `docs/AI_SETUP.md` for MCP setup and worked examples.

## How to invoke a skill

In **GitHub Copilot Chat** (VS Code, agent mode):

- Type `/` and pick a skill from the list, **or**
- Ask in plain language: *"Use the adding-dbt-unit-test skill to …"*

Many official dbt skills are marked **`user-invocable: false`** in their metadata — they may not
appear in the `/` menu, but Copilot still discovers and applies them automatically when your
request matches. You can always name them explicitly in chat.

Each skill directory contains the full procedure in `SKILL.md`. Read that file when you want
details beyond this guide.

---

## Quick picker — "I want to…"

| I want to… | Use this skill |
|------------|----------------|
| Build or change a dbt model, debug local errors, explore sources | `using-dbt-for-analytics-engineering` |
| Write dbt unit tests **before** the SQL (TDD) | `adding-dbt-unit-test` |
| Define metrics, dimensions, or a semantic layer | `building-dbt-semantic-layer` |
| Answer a business question ("total sales last quarter?") | `answering-natural-language-questions-with-dbt` |
| Set up contracts, groups, or cross-project refs (dbt Mesh) | `working-with-dbt-mesh` |
| Investigate a **dbt Cloud / platform job** failure | `troubleshooting-dbt-job-errors` |
| Configure or fix the dbt MCP server in VS Code | `configuring-dbt-mcp-server` |
| Run the right `dbt build` / `dbt show` command with correct flags | `running-dbt-commands` |
| Look up current dbt documentation for a feature | `fetching-dbt-docs` |
| Authenticate CLI, explore Unity Catalog, deploy an Asset Bundle | `databricks` |
| Write a feature spec before coding (SDD) | `create-spec` |
| Break a spec into ordered tasks | `create-tasks` |

**Local vs platform errors:** Use `using-dbt-for-analytics-engineering` (debugging guide) for
`dbt parse` / `dbt build` failures on your machine. Use `troubleshooting-dbt-job-errors` only for
scheduled jobs in dbt Cloud or dbt platform.

---

## dbt skills (official — maintained by dbt Labs)

Source: [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills)

Update bundled copies:

```bash
npx skills add dbt-labs/dbt-agent-skills/skills/dbt
```

| Skill | What it adds | When to use |
|-------|--------------|-------------|
| **`using-dbt-for-analytics-engineering`** | Turns Copilot into a dbt-aware analytics engineer: plans models from desired output, writes SQL with `ref()`/`source()`, adds tests and docs, runs `dbt show` to validate data, debugs parse/compile/run errors, and evaluates downstream impact before you change a model. Includes reference guides for planning, discovery, testing, and debugging. | **Default dbt skill.** Any model building, refactoring, local debugging, or source exploration. |
| **`adding-dbt-unit-test`** | Guides test-driven development for dbt: writes `unit_tests:` YAML with mocked upstream inputs *before* you implement SQL, so you define expected output first. Covers warehouse-specific data types and edge cases (incremental, ephemeral deps). | Adding or extending unit tests; practicing Red → Green → Refactor on dbt SQL. |
| **`building-dbt-semantic-layer`** | Walks through MetricFlow setup: semantic models, entities, dimensions, measures/metrics, time spines, and validation. Supports both latest (dbt 1.12+) and legacy YAML specs. | Defining reusable business metrics and dimensions — not ad-hoc report SQL. |
| **`answering-natural-language-questions-with-dbt`** | Answers analytics questions by querying the semantic layer first, then ad-hoc SQL if needed. Executes against live data (via MCP when available). | *"How many orders last month?"* — consumption/analyst questions, **not** model development. |
| **`working-with-dbt-mesh`** | Implements governance across dbt projects: model contracts, access modifiers, groups, versioning, and `dependencies.yml` cross-project `ref()`. | Multi-repo dbt setups, published marts consumed by other projects, or enforcing stable public interfaces. |
| **`troubleshooting-dbt-job-errors`** | Systematic investigation of **dbt Cloud/platform job** failures: run logs, Admin API, git history, data regressions. Structured template so Copilot does not guess. | A scheduled/production dbt job failed — not local CLI errors. |
| **`configuring-dbt-mcp-server`** | Produces correct MCP config JSON, env vars, and auth setup for local (`uvx dbt-mcp`) or remote servers. Validates connectivity for VS Code, Cursor, or Claude. | First-time MCP setup or when the dbt MCP server will not start / authenticate. |
| **`running-dbt-commands`** | Formats CLI commands correctly: prefers `dbt build` over bare `dbt run`, proper `--select` syntax, `--quiet`, and MCP tools when available. | When you need the exact terminal command or Copilot is about to run dbt with wrong flags. |
| **`fetching-dbt-docs`** | Fetches dbt documentation as LLM-friendly markdown (`.md` URLs) instead of guessing from training data. | *"How does unit testing work in dbt 1.8?"* — factual dbt product questions. |

---

## Databricks skill

This template includes **one** bundled Databricks skill. Databricks publishes a **larger official
suite** (Jobs, Lakeflow Pipelines, Apps, Model Serving, etc.) installable separately.

| Skill | What it adds | When to use |
|-------|--------------|-------------|
| **`databricks`** | CLI authentication, Unity Catalog exploration, Asset Bundle scaffolding and deployment (`databricks bundle validate/deploy`), job and pipeline operations, and PySpark development patterns aligned with Databricks best practices. | Any Databricks workspace task — auth, bundles, jobs, notebooks, catalog/table discovery. |

**Full official suite:** [databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills)

```bash
databricks aitools install   # requires Databricks CLI v1.0.0+
```

Install the full suite when you need specialised skills beyond the bundled general-purpose
`databricks` skill (for example dedicated Lakeflow Pipelines or Apps workflows).

Pair with:

- **Instructions:** `.github/instructions/databricks/databricks.instructions.md` (always-on PySpark style)
- **MCP:** Databricks SQL server in `.vscode/mcp.json` (live schema queries and SQL)

---

## Workflow skills (project-maintained)

These support Specification-Driven Development and general engineering quality — not dbt/Databricks-specific.

| Skill | What it adds | When to use |
|-------|--------------|-------------|
| **`create-spec`** | Guided interview → production-grade `docs/specs/spec.md` aligned with `docs/spec.template.md`. | Before any non-trivial feature; defines the contract for Copilot and reviewers. |
| **`create-tasks`** | Breaks a spec into ordered, executable tasks at `docs/specs/tasks.md`. | After a spec is approved; feeds TDD implementation order. |
| **`audit-security`** | OWASP Top 10 2025 audit with findings and remediation. | Security review of Python or pipeline code. |
| **`refactor-python`** | Refactors Python with DRY, typing, and security improvements. | Cleaning up implementation after tests pass. |
| **`generate-prompt`** | Creates numbered, reusable prompt files under `./prompts/` for agent delegation. | Multi-step work you want to run in fresh Copilot contexts. |
| **`run-prompt`** | Executes saved prompts from `./prompts/` sequentially or in isolation. | Running generated prompt workflows. |

Saved prompt files are local artifacts — see `docs/GETTING_STARTED.md`. The `prompts/` folder
exists for convenience; prompt contents are gitignored.

---

## Skill locations and format

| Scope | Location |
|-------|----------|
| Project (this repo) | `.agents/skills/` ← you are here |
| Personal (all projects) | `~/.agents/skills/` or `~/.copilot/skills/` |

Each skill is a directory with `SKILL.md` (required frontmatter: `name`, `description`) and
optional `references/`, `scripts/`, `assets/`.

See [agentskills.io/specification](https://agentskills.io/specification) for the format reference.

**Optional — project-specific dbt context:** [atlasfutures/dbt-skillz](https://github.com/atlasfutures/dbt-skillz) compiles your actual dbt project DAG into a skill so Copilot knows your real model and column names.
