---
applyTo: "**/*.py,**/notebooks/**,**/src/**/*.py,**/jobs/**/*.py,**/pipelines/**/*.py"
---

# Databricks & PySpark Development Standards

Always-on coding standards for PySpark, Delta Lake, and Databricks Workflows in Python files.

## PySpark: DataFrame API Only

- Always use the DataFrame API. Never use RDD operations unless there is no DataFrame equivalent.
- Import `pyspark.sql.functions as F` and use `F.col()`, `F.lit()`, `F.when()`, etc.
- Never reference columns as bare strings in transformations — use `F.col("column_name")`.
- Chain transformations using parenthesized multi-line expressions for readability.

```python
# ✅ Correct
from pyspark.sql import functions as F

result = (
    df
    .filter(F.col("status").isin(["active", "pending"]))
    .withColumn("amount_usd", F.col("amount") * F.lit(1.1))
    .groupBy("region", "category")
    .agg(
        F.sum("amount_usd").alias("total_revenue"),
        F.countDistinct("customer_id").alias("unique_customers"),
    )
)

# ❌ Wrong
result = df.filter("status in ('active', 'pending')").groupBy("region").sum("amount")
```

## Performance: Never Block the Driver

- Never call `.collect()` on a DataFrame that could be large. Only use `.collect()` on small,
  pre-filtered or aggregated DataFrames (e.g., fewer than a few thousand rows).
- Never call `.toPandas()` on large DataFrames. Use `pandas on Spark` (`df.to_pandas_on_spark()`)
  or process in batches.
- Avoid `.count()` in loops — it triggers a full scan each time.
- Always apply filters as early as possible in the transformation chain.

```python
# ❌ Wrong — will OOM on large data
rows = df.collect()
for row in rows:
    process(row)

# ✅ Correct — process at scale
(
    df
    .filter(F.col("needs_processing") == True)
    .write.mode("append").saveAsTable("catalog.schema.output")
)
```

## Delta Lake: Standard Write Patterns

- Always use Unity Catalog three-part naming: `catalog.schema.table`
- Default format is Delta on Databricks — no need to specify `.format("delta")` explicitly
  when using `saveAsTable`, but always specify when using `save(path)`.
- Use `mergeSchema` or `overwriteSchema` intentionally — never silently suppress schema errors.

```python
# Standard overwrite
(
    result_df
    .write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("catalog.schema.my_table")
)

# Append (schema must match)
(
    new_rows_df
    .write
    .mode("append")
    .saveAsTable("catalog.schema.my_table")
)

# MERGE / UPSERT
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "catalog.schema.target")
(
    target.alias("t")
    .merge(updates_df.alias("s"), "t.id = s.id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)
```

## Secrets: Never Hardcode Credentials

- Never hardcode tokens, passwords, connection strings, or API keys in notebooks or scripts.
- Use Databricks Secrets:

```python
# ✅ Correct
token = dbutils.secrets.get(scope="my-scope", key="my-token")
jdbc_url = dbutils.secrets.get(scope="connections", key="postgres-url")

# ❌ Wrong
token = "dapi1234567890abcdef"
```

## Notebook Widgets for Parameterisation

Use `dbutils.widgets` for all runtime parameters passed to jobs:

```python
# Define widget with default value
dbutils.widgets.text("env", "dev", "Environment")
dbutils.widgets.dropdown("run_date", "today", ["today", "yesterday"])

# Read widget value
env = dbutils.widgets.get("env")
run_date = dbutils.widgets.get("run_date")
```

## Type Hints and Docstrings

All Python functions must have type hints and docstrings. Use Sphinx format:

```python
from pyspark.sql import DataFrame

def filter_active_customers(df: DataFrame, min_orders: int = 1) -> DataFrame:
    """Filter customers who placed at least `min_orders` orders.

    :param df: Input DataFrame with columns customer_id, order_count, status.
    :param min_orders: Minimum number of orders to include. Defaults to 1.
    :return: Filtered DataFrame.
    """
    return df.filter(
        (F.col("status") == "active") & (F.col("order_count") >= min_orders)
    )
```

## Partitioning and Optimisation

- Always partition large Delta tables by a high-cardinality time column (`date`, `year`/`month`).
- Use Z-ORDER on columns frequently used in filters or joins:

```python
spark.sql("""
    OPTIMIZE catalog.schema.events
    ZORDER BY (event_date, user_id)
""")
```

- Run `ANALYZE TABLE ... COMPUTE STATISTICS` after large writes to improve query planning.
- Enable Auto Optimize in table properties for frequently written tables:

```python
spark.sql("""
    ALTER TABLE catalog.schema.my_table
    SET TBLPROPERTIES (
        delta.autoOptimize.optimizeWrite = true,
        delta.autoOptimize.autoCompact = true
    )
""")
```

## Unity Catalog Governance

- Always specify the full three-part name: `catalog.schema.table`
- Grant minimum necessary privileges — prefer role-based grants over user-level grants:

```sql
GRANT SELECT ON TABLE catalog.schema.my_table TO ROLE data_analyst_role;
GRANT USE SCHEMA ON SCHEMA catalog.schema TO ROLE data_engineer_role;
```

## Error Handling

```python
from pyspark.sql.utils import AnalysisException, ParseException

try:
    df = spark.read.table("catalog.schema.my_table")
except AnalysisException as e:
    # Table doesn't exist or schema mismatch
    raise RuntimeError(f"Failed to read table: {e}") from e
```

## Testing PySpark Code

- Use `chispa` for DataFrame equality assertions in pytest:

```python
from chispa.dataframe_comparer import assert_df_equality

def test_filter_active_customers(spark):
    input_df = spark.createDataFrame([
        ("C1", "active", 5),
        ("C2", "inactive", 2),
    ], ["customer_id", "status", "order_count"])

    result = filter_active_customers(input_df, min_orders=3)
    expected = spark.createDataFrame([
        ("C1", "active", 5),
    ], ["customer_id", "status", "order_count"])

    assert_df_equality(result, expected, ignore_row_order=True)
```
