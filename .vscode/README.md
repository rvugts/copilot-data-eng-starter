# VS Code Configuration

This directory contains VS Code settings and extension recommendations — **pre-configured for Python, dbt, and Databricks**. No setup script required.

## Files

| File | Purpose |
|------|---------|
| `settings.json` | Editor, Python, pytest, Pylance, and Copilot settings |
| `extensions.json` | Recommended extensions (Python, dbt Power User, Databricks, Copilot) |
| `mcp.json` | MCP server config for dbt and Databricks (add your credentials) |

## Recommended extensions

Installed via VS Code prompt when you open the project:

- **Python** — Pylance, Black, flake8, pylint, pytest
- **dbt Power User** — model editing, lineage, compilation
- **Databricks** — workspace and notebook integration
- **GitHub Copilot** — AI-assisted development

## Python interpreter

Settings point to `${workspaceFolder}/venv/bin/python`. Run `make install` first to create the virtual environment.

## MCP servers

Configure `.vscode/mcp.json` with your Databricks workspace URL and dbt credentials. See `docs/AI_SETUP.md` for setup instructions.
