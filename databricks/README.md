# Databricks

This starter does **not** include a Databricks Asset Bundle by default. Add one when you deploy jobs, pipelines, or notebooks to Databricks.

## Getting started

1. **Authenticate:** `databricks auth login` (see `/databricks` skill or `docs/AI_SETUP.md`)
2. **Scaffold a bundle** (in repo root or a subfolder):
   ```bash
   databricks bundle init
   ```
3. **Validate and deploy:**
   ```bash
   make databricks-validate
   make databricks-deploy
   ```

Makefile targets skip gracefully until `databricks.yml` exists at the repo root.

## Typical structure (after `bundle init`)

```
databricks.yml          # Bundle config (triggers Makefile targets at repo root)
resources/
  jobs/
  pipelines/
src/                    # PySpark notebooks or Python entrypoints (may overlap with repo src/)
```

## Copilot guidance

- PySpark standards: `.github/instructions/databricks/databricks.instructions.md`
- CLI, bundles, Unity Catalog: `/databricks` skill
- Live workspace queries: Databricks MCP in `.vscode/mcp.json` — see `docs/AI_SETUP.md`

## Conventions

- Use Unity Catalog three-part names: `catalog.schema.table`
- Secrets via `dbutils.secrets.get()` — never hardcode tokens in source
- Prefer Databricks Asset Bundles for dev/staging/prod deployment

Document deployment and naming decisions in `docs/adr/` when your team settles on patterns.
