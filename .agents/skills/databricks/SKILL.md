---
name: databricks
description: >-
  Databricks workspace operations: CLI authentication, Unity Catalog exploration,
  job creation, Lakeflow Pipelines, bundle deployment, and PySpark development.
  Use when working with any Databricks resource — jobs, notebooks, catalogs, schemas,
  tables, pipelines, or compute.
metadata:
  source: https://github.com/databricks/databricks-agent-skills
  version: "1.0.0"
---

# Databricks Development

> **Keep this skill current:** The official Databricks skills are maintained at
> [databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills).
> Install via: `databricks aitools install` (requires Databricks CLI v1.0.0+)

## Prerequisites

1. **Databricks CLI installed** (v1.0.0+):
   ```bash
   databricks --version
   # Install if missing:
   brew tap databricks/tap && brew install databricks   # macOS
   ```

2. **Authenticated**:
   ```bash
   databricks auth profiles          # list existing profiles
   databricks auth login --host https://<workspace>.azuredatabricks.net --profile my-workspace
   ```

3. **Always use `--profile`** on every command — never rely on defaults.

## Unity Catalog Exploration

**Prefer the AI tools over manual navigation:**

```bash
# Discover table structure (columns, types, sample data)
databricks experimental aitools tools discover-schema catalog.schema.table --profile <PROFILE>

# Run ad-hoc SQL
databricks experimental aitools tools query "SELECT * FROM catalog.schema.table LIMIT 10" --profile <PROFILE>

# Find the default SQL warehouse
databricks experimental aitools tools get-default-warehouse --profile <PROFILE>
```

**Manual catalog navigation** (use exact positional argument syntax):

```bash
databricks catalogs list --profile <PROFILE>
databricks schemas list <CATALOG> --profile <PROFILE>                    # positional arg!
databricks tables list <CATALOG> <SCHEMA> --profile <PROFILE>           # positional args!
databricks tables get <CATALOG>.<SCHEMA>.<TABLE> --profile <PROFILE>
```

> **Common mistake:** Do NOT use `--catalog-name` or `--catalog` flags — these don't exist. Always use positional arguments.

## MCP Server (Recommended for AI Development)

Configure the Databricks Managed MCP Server in `.vscode/mcp.json` for live workspace access
from GitHub Copilot agent mode. See `.vscode/mcp.json` in this repo for the full configuration.

With the MCP server active, Copilot can:
- Query Unity Catalog tables directly
- Execute SQL and return results
- Browse Genie spaces
- Explore table schemas without leaving the editor

## PySpark Development Standards

```python
# ✅ Always import types explicitly
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, LongType

# ✅ Use DataFrame API — avoid RDD operations
result = (
    df
    .filter(F.col("status") == "active")
    .groupBy("region")
    .agg(F.sum("revenue").alias("total_revenue"))
    .orderBy(F.desc("total_revenue"))
)

# ✅ Use F.col() instead of string column references
df.filter(F.col("amount") > 0)         # correct
df.filter("amount > 0")                 # avoid — no type safety

# ❌ Never .collect() on large datasets
# ❌ Never use pandas UDFs when native Spark functions exist
# ❌ Never use RDDs unless absolutely unavoidable
```

## Delta Lake Patterns

```python
# Read Delta table via Unity Catalog
df = spark.read.table("catalog.schema.table")

# Write as Delta (default on Databricks)
(
    df.write
    .format("delta")
    .mode("overwrite")        # or "append", "merge"
    .option("overwriteSchema", "true")
    .saveAsTable("catalog.schema.new_table")
)

# Incremental merge (UPSERT)
from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, "catalog.schema.target_table")
(
    delta_table.alias("target")
    .merge(
        updates_df.alias("source"),
        "target.id = source.id"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# Optimize and Z-ORDER for query performance
spark.sql("OPTIMIZE catalog.schema.table ZORDER BY (date, region)")

# Table history and time travel
spark.sql("DESCRIBE HISTORY catalog.schema.table")
df_yesterday = spark.read.option("timestampAsOf", "2024-01-14").table("catalog.schema.table")
```

## Databricks Asset Bundles (DABs)

Prefer DABs for deploying jobs and pipelines to production:

```bash
# Scaffold a new bundle project
databricks bundle init default-python --profile <PROFILE>

# Validate configuration
databricks bundle validate --profile <PROFILE>

# Deploy to dev
databricks bundle deploy -t dev --profile <PROFILE>

# Run a specific job
databricks bundle run <job_name> -t dev --profile <PROFILE>
```

**Bundle structure:**
```
my-project/
├── databricks.yml          # Bundle root config
├── resources/
│   ├── my_job.job.yml      # Job definition
│   └── my_pipeline.yml     # Pipeline definition
└── src/
    └── notebooks/          # Notebook source files
```

**Example job definition:**
```yaml
# resources/daily_transform.job.yml
resources:
  jobs:
    daily_transform:
      name: "[${bundle.target}] Daily Transform"
      schedule:
        quartz_cron_expression: "0 0 6 * * ?"
        timezone_id: "UTC"
      tasks:
        - task_key: run_notebook
          notebook_task:
            notebook_path: ../src/notebooks/transform.py
          # Omit cluster config for serverless
```

## Job Operations (CLI)

```bash
databricks jobs list --profile <PROFILE>
databricks jobs get --job-id <ID> --profile <PROFILE>
databricks jobs run-now <JOB_ID> --profile <PROFILE>
databricks jobs run-now --json '{"job_id": <ID>, "job_parameters": {"env": "prod"}}' --profile <PROFILE>
```

## Common Troubleshooting

| Error | Solution |
|-------|----------|
| `cannot configure default credentials` | Add `--profile` flag to every command |
| `PERMISSION_DENIED` | Check Unity Catalog grants: `GRANT SELECT ON TABLE ... TO ...` |
| `RESOURCE_DOES_NOT_EXIST` | Verify catalog/schema/table names with `databricks tables list` |
| Schema drift on write | Add `.option("mergeSchema", "true")` or `.option("overwriteSchema", "true")` |
| Slow query | Run `ANALYZE TABLE ... COMPUTE STATISTICS` and check for partition pruning |

## Further Resources

- [Databricks Documentation](https://docs.databricks.com/)
- [databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills) — official skills
- [Databricks CLI reference](https://docs.databricks.com/dev-tools/cli/index.html)
- [Delta Lake documentation](https://docs.delta.io/)
- [Unity Catalog best practices](https://docs.databricks.com/data-governance/unity-catalog/index.html)
