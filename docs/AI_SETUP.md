# AI Setup Guide for Data Engineers

This guide covers setting up skills and MCP servers that supercharge AI-assisted development
for dbt, Databricks, and Python data engineering work.

> **Recommended watch:** [AI-Powered Data Engineering with dbt and MCP](https://www.youtube.com/watch?v=34RkoSPfpV4)
> — walks through the dbt Skills and dbt MCP Server setup covered in this guide.

---

## Overview: Skills vs. MCP Servers

These two things work differently and complement each other:

| | Instruction file | Skill | MCP Server |
|---|---|---|---|
| **When active** | Always-on for matching file types | Invoked on demand | Always available in agent mode |
| **Purpose** | Coding style and conventions | Multi-step workflows | Live data and tool access |
| **dbt example** | "Use trailing commas, CTEs over subqueries" | "Build staging models from this source" | Query Unity Catalog, run SQL |
| **Databricks example** | "Use F.col(), never .collect() on large sets" | "Set up an Asset Bundle, deploy a job" | Browse catalogs, execute queries |

**Use all three together** for the best experience.

---

## Skills

### Included in This Template

The following skills are included in `.agents/skills/` and available immediately in Copilot Chat
and other AI agents:

| Skill | Invoke | Purpose |
|-------|--------|---------|
| `using-dbt-for-analytics-engineering` | `/using-dbt-for-analytics-engineering` | Build/modify models, write SQL, debug, write tests |
| `adding-dbt-unit-test` | `/adding-dbt-unit-test` | TDD for dbt — write unit tests before implementing |
| `building-dbt-semantic-layer` | `/building-dbt-semantic-layer` | Create metrics, semantic models, dimensions, and entities |
| `answering-natural-language-questions-with-dbt` | `/answering-natural-language-questions-with-dbt` | Answer analytics questions with dbt Semantic Layer or SQL |
| `working-with-dbt-mesh` | `/working-with-dbt-mesh` | Model contracts, access, groups, versioning, and cross-project refs |
| `troubleshooting-dbt-job-errors` | `/troubleshooting-dbt-job-errors` | Diagnose dbt Cloud/platform job failures |
| `configuring-dbt-mcp-server` | `/configuring-dbt-mcp-server` | Configure and troubleshoot the dbt MCP server |
| `running-dbt-commands` | `/running-dbt-commands` | Format dbt CLI commands, selectors, and parameters |
| `fetching-dbt-docs` | `/fetching-dbt-docs` | Retrieve dbt documentation for current features and APIs |
| `databricks` | `/databricks` | CLI auth, Unity Catalog exploration, job/pipeline deployment |
| `create-spec` | `/create-spec` | Spec-Driven Development — write a feature spec |
| `create-tasks` | `/create-tasks` | Break a spec into executable tasks |
| `audit-security` | `/audit-security` | Security audit of the codebase |
| `refactor-python` | `/refactor-python` | Refactor Python with engineering best practices |
| `generate-prompt` | `/generate-prompt` | Generate reusable multi-step prompts |
| `run-prompt` | `/run-prompt` | Execute saved prompts from `./prompts/` as isolated sub-tasks |

See `.agents/skills/README.md` for skill descriptions, when-to-use guidance, update commands, and personal skill locations.

### Keeping Skills Up to Date

The dbt and Databricks skills in this repo are seeded from the official maintained packages.
Keep them current using the [Vercel Skills CLI](https://github.com/vercel-labs/skills):

```bash
# Install or update the official dbt skills (overwrites local copies)
npx skills add dbt-labs/dbt-agent-skills/skills/dbt

# Install or update the official Databricks skills
# Via the Databricks CLI (v1.0.0+)
databricks aitools install
```

### Official Skill Sources

Both dbt Labs and Databricks publish and maintain their own official skill packages:

- **[dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills)** — analytics
  engineering, unit testing, semantic layer, dbt Mesh, MCP setup, troubleshooting, and more.
  Install via `npx skills add dbt-labs/dbt-agent-skills`.

- **[databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills)**
  — core CLI, Jobs (Lakeflow), Pipelines (formerly DLT), Apps, Model Serving, and more.
  Install via `databricks aitools install`.

- **[atlasfutures/dbt-skillz](https://github.com/atlasfutures/dbt-skillz)** — compiles your
  *actual* dbt project (real model names, column names, DAG structure) into a `SKILL.md`.
  Gives the agent project-specific context rather than generic guidance.

---

## MCP Servers

### Databricks Managed MCP Server

The Databricks Managed MCP Server gives Copilot agent mode **live access to your workspace**:
query Unity Catalog tables, execute SQL, browse Genie spaces, and explore table schemas —
all without leaving the editor.

**Requires:** VS Code 1.101+ with GitHub Copilot agent mode enabled.

**Setup:**

1. Open `.vscode/mcp.json` in this repo (already included as a template)
2. Replace `<workspace-url>` with your Databricks workspace URL
3. Generate a Personal Access Token (PAT):
   - In Databricks: **User Settings → Developer → Access Tokens → Generate new token**
4. Set the token as an environment variable (never commit it):
   ```bash
   export DATABRICKS_PAT=dapi...
   ```
   Or add to your shell profile (`~/.zshrc`, `~/.bashrc`).
5. In VS Code: open **Command Palette** → **MCP: List Servers** — `databricks` should appear.

**OAuth (VS Code 1.101+):** VS Code natively supports OAuth for the Databricks MCP server,
so you can avoid PATs entirely. Remove the `headers` block from `mcp.json` and authenticate
interactively when prompted.

**What you can do once connected:**

- "Show me the schema of `catalog.schema.orders`"
- "Run `SELECT count(*) FROM catalog.schema.events WHERE date = '2024-01-15'`"
- "What tables are in the `analytics` schema?"

### dbt MCP Server (local)

The dbt MCP Server connects Copilot to the dbt CLI, Discovery API, and dbt Cloud platform APIs.

**Requires:** `uv` package manager and a dbt project.

**Install `uv`:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Configure environment variables** (add to `.env` or shell profile):
```bash
export DBT_PROJECT_DIR=/path/to/your/dbt/project   # folder containing dbt_project.yml
export DBT_PATH=$(which dbt)

# Optional: dbt Cloud platform access (Discovery API, Admin API)
export DBT_HOST=https://your-subdomain.us1.dbt.com
export DBT_TOKEN=dbt_...
export DBT_ACCOUNT_ID=12345
export DBT_PROD_ENV_ID=67890
```

**Verify the server starts:**
```bash
uvx dbt-mcp   # should start without errors
```

The `.vscode/mcp.json` in this repo is pre-configured — once your environment variables are set,
VS Code will start the dbt MCP server automatically.

**In VS Code:**
1. Open **Command Palette** → **MCP: List Servers** — `dbt` should appear
2. Ask Copilot: "What dbt tools do you have access to?" to verify connectivity

**What you can do once connected:**

- "List my dbt models and their descriptions"
- "Show the lineage upstream of `fct_orders`"
- "Run `dbt show --select stg_raw__customers --limit 10` and show me the results"
- "What metrics are defined in the semantic layer?"

---

## Instruction Files (Always-On)

Instruction files apply automatically based on the file you're working on — no invocation needed.
They enforce coding style and conventions as you edit.

| File | Applies To | Covers |
|------|-----------|--------|
| `.github/instructions/dbt/dbt-sql.instructions.md` | All `.sql` files; `schema.yml`, `dbt_project.yml` | SQL style, model naming, tests, materialization |
| `.github/instructions/databricks/databricks.instructions.md` | Python files | PySpark DataFrame API, Delta Lake patterns, secrets, type hints |
| `.github/instructions/python/python-general.instructions.md` | All `.py` files | Python style, TDD, type hints, error handling |

---

## Recommended Workflow

### For a new dbt model

```
1. Open a .sql file in models/
   → dbt-sql.instructions.md activates automatically (style enforcement)

2. Use /using-dbt-for-analytics-engineering skill:
   "Build a staging model for the raw.orders source"
   → Skill discovers schema, plans CTEs, writes SQL + schema.yml tests

3. Use /adding-dbt-unit-test skill (TDD):
   "Add a unit test for the cancelled-orders-excluded logic"
   → Writes unit_tests: block in schema.yml before implementing the SQL

4. Iterate with the dbt MCP server:
   "Run dbt show --select stg_raw__orders --limit 20"
   → Live preview without switching to terminal
```

### For a new Databricks job

```
1. Use /databricks skill:
   "Scaffold a new Databricks Asset Bundle job that runs a daily PySpark notebook"
   → Creates bundle structure, resources YAML, and AGENTS.md

2. databricks.instructions.md activates automatically in .py files
   → Enforces DataFrame API, no .collect(), type hints, Delta write patterns

3. Deploy:
   "Validate and deploy the bundle to dev"
   → Skill runs: databricks bundle validate && databricks bundle deploy -t dev
```

### For a data quality investigation

```
1. Use the Databricks MCP server directly:
   "How many rows in catalog.analytics.fct_orders have a null customer_id?"
   → Copilot queries your live workspace and returns results inline

2. Cross-reference with dbt:
   "Show me the dbt test coverage for fct_orders"
   → dbt MCP server looks up schema.yml tests
```

---

## Troubleshooting

### MCP server not appearing in VS Code

1. Check VS Code version: must be 1.101+
2. Open **Settings → Features → Chat → Enable MCP** — ensure it's on
3. Run **MCP: Reload Servers** from Command Palette
4. Check environment variables are set in the shell that launched VS Code:
   ```bash
   echo $DATABRICKS_PAT
   echo $DBT_PROJECT_DIR
   ```

### dbt MCP server fails to start

```bash
# Test manually
DBT_PROJECT_DIR=/path/to/project DBT_PATH=$(which dbt) uvx dbt-mcp
```

Common issues:
- `uv` not installed → `curl -LsSf https://astral.sh/uv/install.sh | sh`
- `dbt` not on PATH → set `DBT_PATH` explicitly
- `DBT_PROJECT_DIR` doesn't contain `dbt_project.yml` → check the path

### Databricks MCP returns 401

- Regenerate your PAT (they expire)
- Verify the workspace URL includes the full path (no trailing slash)
- Try: `curl -H "Authorization: Bearer $DATABRICKS_PAT" https://<workspace>/api/2.0/sql/config/warehouses`

---

## Further Reading

- [GitHub Copilot MCP documentation](https://docs.github.com/en/copilot/using-github-copilot/using-model-context-protocol-with-github-copilot)
- [dbt MCP Server docs](https://docs.getdbt.com/docs/dbt-cloud/cloud-configuring-dbt-cloud/mcp)
- [Databricks Copilot integration](https://docs.databricks.com/integrations/github-copilot.html)
- [Agent Skills specification](https://agentskills.io/specification)
- [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills)
- [databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills)
