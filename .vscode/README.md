# VS Code Configuration

This directory contains shared and language-specific VS Code settings and extension recommendations.

## Structure

- **settings.json** — Universal settings (formatting, Git, Copilot)
- **extensions.json** — Universal extension recommendations (Copilot, GitLens, Remote containers, etc)
- **settings.python.json** — Python-specific settings (linting, testing, type checking)
- **extensions.python.json** — Python-specific extensions (Pylance, pytest, Black formatter, etc)
- **merge-configs.py** — Helper script to merge language-specific configs into main settings.json/extensions.json

## How It Works

### For Template Users (No Python)

By default, you get a clean VS Code setup:
- **settings.json** contains only universal formatting and Copilot settings
- **extensions.json** recommends only universal extensions (Copilot, GitLens, etc)
- No language-specific extensions or settings pollution

### When You Enable Python

Run `bash scripts/enable-python.sh`, which:
1. Creates virtual environment
2. Installs dependencies
3. **Calls** `python .vscode/merge-configs.py python`

This merge script:
- Reads `settings.python.json` and merges into `settings.json`
- Reads `extensions.python.json` and merges into `extensions.json`
- VS Code automatically loads the updated configs

**Result:** Your settings.json and extensions.json are now extended with Python-specific configuration. You'll see a prompt to install recommended extensions.

## Language Extensibility

To add another language (e.g., dbt):

1. Create `.vscode/settings.dbt.json`:
   ```json
   {
     "editor.defaultFormatter": "...",
     "dbt.projectsDir": "."
   }
   ```

2. Create `.vscode/extensions.dbt.json`:
   ```json
   {
     "recommendations": [
       "innoverio.vscode-dbt-power-user"
     ]
   }
   ```

3. Update or create a setup script to call:
   ```bash
   python .vscode/merge-configs.py dbt
   ```

## Notes

- Language-specific config files are **always in git** so they're available for documentation and merge
- Main settings.json/extensions.json are **modified locally** (added to git tracked files, but their merged state is not tracked separately)
- The merge is idempotent: running it multiple times is safe
