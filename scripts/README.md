# Scripts

This directory holds optional helper scripts. **Primary setup is via the Makefile at the repo root.**

## Quick start

```bash
make install          # Create venv, install deps, install pre-commit hooks
source venv/bin/activate
make test             # Run tests with ≥80% coverage
make help             # List all targets (including optional dbt/Databricks)
```

## Common commands

| Command | Purpose |
|---------|---------|
| `make install` | One-time environment setup |
| `make test` | pytest with coverage |
| `make lint` | pylint + flake8 |
| `make format` | black |
| `make type-check` | pyright |
| `make all` | lint → format → type-check → test |
| `make pre-commit` | Run all pre-commit hooks |
| `make dbt-parse` | Parse dbt project (skips if no `dbt_project.yml`) |
| `make databricks-validate` | Validate bundle (skips if no `databricks.yml`) |

See `Makefile` and `docs/DEVELOPMENT.md` for full details.
