# Getting Started

This is the Day 1 path for using this starter in **VS Code with GitHub Copilot**.
The repo may be maintained from Cursor, but the template is intended for Copilot
agent mode, `.github/instructions/`, `.agents/skills/`, and `.vscode/mcp.json`.

## 1. Create Your Project

Use the GitHub **Use this template** button, download the repository archive, or
clone and reinitialize git for a local-only start:

```bash
git clone https://github.com/<owner>/copilot-data-eng-starter.git my-new-project
cd my-new-project
rm -rf .git
git init
```

## 2. Set Up Python

Install the development environment and run the starter tests:

```bash
make install
make test
```

This validates the Python tooling, pre-commit setup, and example TDD patterns in
`src/` and `tests/`.

## 3. Open in VS Code

Install the recommended extensions when VS Code prompts you. The important ones
for this template are GitHub Copilot, Copilot Chat, Python, dbt Power User, and
Databricks.

Before using Copilot agent mode, review:

- `.github/copilot-instructions.md` for repo-wide guidance
- `.github/instructions/` for dbt, Databricks, Python, and TDD rules
- `.agents/skills/README.md` for what each skill does, when to use it, and how to invoke it

## 4. Configure AI Access

Copy `.env.example` to `.env` and configure only the services you need.

For live Databricks and dbt context in Copilot, use `.vscode/mcp.json` and follow
`docs/AI_SETUP.md`.

At minimum:

- Databricks MCP needs a workspace URL and PAT or OAuth flow.
- dbt MCP needs `uv`, a dbt project, and `DBT_PROJECT_DIR` pointing at the folder
  containing `dbt_project.yml`.

## 5. Add Your Data Project

This starter intentionally does not ship a full dbt project or Databricks Asset
Bundle. Add them when your project needs them.

For dbt:

```bash
dbt init
make dbt-parse
```

For Databricks:

```bash
databricks auth login
databricks bundle init
make databricks-validate
```

See `dbt/README.md` and `databricks/README.md` for the expected layout and
Makefile behavior.

## 6. Start Work With a Spec

For meaningful changes, start with Specification-Driven Development:

1. Use `/create-spec` to write `docs/specs/spec.md`.
2. Use `/create-tasks` to break the spec into executable tasks.
3. Work task by task with TDD.
4. Use dbt, Databricks, and Python skills as needed.

Saved prompt files are local workflow artifacts. The `prompts/` folder exists so
agents have a stable place to write them, but prompt files are ignored by git and
are not part of the starter template.

## 7. Where to Go Next

- `docs/AI_SETUP.md` — detailed MCP and skill setup
- `docs/DEVELOPMENT.md` — development workflow and quality standards
- `docs/VIBE_CODING_GUIDE.md` — deeper Copilot collaboration patterns
- `docs/TROUBLESHOOTING.md` — common setup and runtime issues
- `docs/specs/example-stg-orders-models.spec.md` — example dbt model spec

