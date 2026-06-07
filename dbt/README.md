# dbt Project

This starter does **not** include a dbt project by default. Add one when you are ready to build your transformation layer.

## Recommended layout

Initialize at the **repository root** (keeps Makefile `dbt-*` targets working without changes):

```bash
# From repo root, with your dbt adapter installed (e.g. dbt-databricks)
dbt init
```

Or create a `dbt/` subfolder and run `dbt init` inside it — Makefile detects both `dbt_project.yml` and `dbt/dbt_project.yml`.

## After init

```bash
make dbt-deps      # Install package dependencies
make dbt-parse     # Validate project parses
make dbt-run       # Run models (dev target)
make dbt-test      # Run tests
```

Configure connection profiles in `~/.dbt/profiles.yml` (never commit credentials). See [dbt profiles documentation](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml).

## Copilot guidance

- SQL style and tests: `.github/instructions/dbt/dbt-sql.instructions.md`
- Build models: `/using-dbt-for-analytics-engineering` skill
- TDD for SQL: `/adding-dbt-unit-test` skill
- MCP live access: configure `.vscode/mcp.json` and `DBT_PROJECT_DIR` — see `docs/AI_SETUP.md`

## Conventions (when you start)

| Layer | Prefix | Example | Materialization |
|-------|--------|---------|-----------------|
| Staging | `stg_<source>__<entity>` | `stg_raw__orders` | view |
| Intermediate | `int_` | `int_orders_enriched` | view |
| Marts | `fct_`, `dim_`, `rpt_` | `fct_orders`, `dim_customers` | table |

You can document team-specific decisions in `docs/adr/` (see suggested titles in `docs/adr/README.md`).
