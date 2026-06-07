# Agent Skills

Skills for GitHub Copilot, Cursor, Claude, and any other [Agent Skills](https://agentskills.io)-compatible AI assistant.

This is the standard cross-platform location for project-level skills per the
[Agent Skills specification](https://agentskills.io/specification). All skills here work in
agent/chat mode across GitHub Copilot (VS Code, CLI, coding agent), Cursor, Claude Code, and more.

## Keeping dbt skills up to date

The dbt skills are maintained by dbt Labs. Update them at any time:

```bash
npx skills add dbt-labs/dbt-agent-skills/skills/dbt
```

## Available Skills

### dbt (official — maintained by dbt Labs)

| Skill | Description |
|-------|-------------|
| `using-dbt-for-analytics-engineering` | Build/modify models, debug, explore sources, write tests |
| `adding-dbt-unit-test` | TDD for dbt models — write unit tests before implementing SQL |
| `building-dbt-semantic-layer` | MetricFlow metrics and dimensions |
| `answering-natural-language-questions-with-dbt` | Answer business questions via the semantic layer |
| `working-with-dbt-mesh` | Contracts, access, groups, cross-project refs |
| `troubleshooting-dbt-job-errors` | Diagnose and fix dbt platform job failures |
| `configuring-dbt-mcp-server` | Set up the dbt MCP server for VS Code, Cursor, or Claude |
| `running-dbt-commands` | Correct CLI flags, selectors, and parameter formats |
| `fetching-dbt-docs` | Look up dbt documentation efficiently |

Source: [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills)

### Databricks

| Skill | Description |
|-------|-------------|
| `databricks` | CLI auth, Unity Catalog, job/pipeline deployment, Asset Bundles, PySpark patterns |

Source: [databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills) for the full official suite

### Workflow

| Skill | Description |
|-------|-------------|
| `create-spec` | Spec-Driven Development — write a production-grade feature specification |
| `create-tasks` | Break a spec into atomic, ordered, executable tasks |
| `audit-security` | OWASP Top 10 2025 security audit with remediation report |
| `refactor-python` | Python refactoring with DRY, type hints, security, and performance improvements |
| `generate-prompt` | Generate reusable multi-step prompts for agent delegation |
| `run-prompt` | Execute saved prompts from `./prompts/` as isolated sub-tasks |

## Skill locations

Per the [Agent Skills spec](https://agentskills.io/specification), GitHub Copilot reads skills from:

| Scope | Location |
|-------|---------|
| Project (this repo) | `.agents/skills/` ← you are here |
| Personal (all projects) | `~/.agents/skills/` or `~/.copilot/skills/` |

## Format

Each skill is a directory containing a `SKILL.md` file with YAML frontmatter (`name` + `description` required) and Markdown instructions. Optional subdirectories: `references/`, `scripts/`, `assets/`.

See [agentskills.io/specification](https://agentskills.io/specification) for the full format reference.
