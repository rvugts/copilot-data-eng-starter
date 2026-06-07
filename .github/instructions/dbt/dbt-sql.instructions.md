---
applyTo: >-
  **/*.sql,
  **/schema.yml,
  **/sources.yml,
  **/models/**/*.yml,
  **/macros/**/*.yml,
  **/seeds/**/*.yml,
  **/snapshots/**/*.yml,
  **/analyses/**/*.yml,
  **/dbt_project.yml
---

# dbt & SQL Development Standards

## SQL Style

- Write all SQL keywords in lowercase: `select`, `from`, `where`, `join`, `group by`, `order by`, `case when`, `union all`
- Use trailing commas in select lists for cleaner diffs
- One column per line in select statements
- Use explicit column references — never `select *`
- Use explicit `inner join`, `left join` — never bare `join`
- Use `coalesce()` instead of `ifnull()` or `nvl()` for portability
- Use `union all` unless deduplication is explicitly required — never bare `union`
- Indent joins and where clauses consistently (2 or 4 spaces, be consistent)
- Use CTEs (`with` blocks) instead of subqueries for readability
- Name CTEs descriptively: `filtered_claims`, `aggregated_revenue` — not `t1`, `cte1`, `tmp`
- Place `where` filters as early as possible in the query to reduce data volume
- Always qualify column names with the table/CTE alias in joins: `claims.claim_id`, not just `claim_id`
- Use `is not null` instead of `!= null` or `<> null`

## dbt Model Naming Conventions

Follow the standard dbt layering pattern:

- `stg_<source>__<entity>` — Staging models: one-to-one with source tables, light renaming and type casting only. Example: `stg_raw__orders` from `{{ source('raw', 'orders') }}`
- `int_` — Intermediate models: business logic, joins, transformations between staging and final
- `fct_` — Fact models: event-based, grain is one row per event/transaction
- `dim_` — Dimension models: descriptive attributes, slowly changing dimensions
- `rpt_` — Report models: pre-aggregated for specific dashboards or consumers (optional layer)

Official dbt skill examples may use shortened names (e.g. `stg_orders`) for readability. In this project, always use `stg_<source>__<entity>` for staging models.

Source naming: define sources in `sources.yml` with explicit `loaded_at_field` for freshness checks.

## dbt Model Structure

Every model should follow this structure:

```sql
-- 1. CTEs for imports (ref/source calls)
with

source_claims as (
    select * from {{ ref('stg_raw__claims') }}
),

source_providers as (
    select * from {{ ref('stg_raw__providers') }}
),

-- 2. CTEs for transformations
joined as (
    select
        source_claims.claim_id
        , source_claims.claim_date
        , source_providers.provider_name
    from source_claims
    left join source_providers
        on source_claims.provider_id = source_providers.provider_id
),

-- 3. Final select
final as (
    select
        claim_id
        , claim_date
        , provider_name
    from joined
)

select * from final
```

Key rules:
- Always end with a `final` CTE and `select * from final`
- Import CTEs at the top — one per `ref()` or `source()` call
- Keep transformation logic in the middle CTEs
- Only `select *` is allowed in the very last line from the `final` CTE

## dbt Testing Standards

Every model MUST have in `schema.yml`:

- `not_null` test on the primary key column
- `unique` test on the primary key column
- `not_null` test on critical business columns (amounts, dates, foreign keys)
- `accepted_values` test on status/type/category columns where the domain is known
- `relationships` test on foreign key columns to verify referential integrity

For financial or critical models, add:

- `dbt_utils.expression_is_true` for business rule validation (e.g., `amount > 0`)
- `dbt_utils.accepted_range` for numeric boundaries
- Custom singular tests for complex business logic

Test naming: singular test files go in `tests/` with descriptive names: `assert_no_orphaned_claims.sql`, not `test1.sql`.

## dbt Documentation

Every model MUST have in `schema.yml`:

- A model-level `description` explaining what the model represents and its grain
- A `description` for every column — written in business language, not technical jargon
- Units for numeric columns: `"Claim amount in EUR, excluding VAT"`
- Allowed values for categorical columns: `"Status: 'open', 'closed', 'pending'"`

Use `doc` blocks in `docs/` for shared definitions that appear in multiple models.

Generate documentation with `dbt docs generate` and verify completeness in CI.

## dbt Macros and Packages

- Use `dbt_utils` for common patterns: `surrogate_key`, `pivot`, `union_relations`, `star`
- Use `dbt_expectations` for advanced data quality tests
- Use `codegen` to generate base models and schema YAML from sources
- Write custom macros for team-specific patterns — don't repeat SQL across models
- Place macros in `macros/` with one file per macro, named after the macro

## Performance

- Materialize staging models as `view` (unless performance requires otherwise)
- Materialize intermediate models as `ephemeral` when they are only used once
- Materialize fact and dimension models as `table` or `incremental`
- For incremental models, always define `unique_key` and use `is_incremental()` correctly
- Avoid `order by` in models unless the consumer explicitly requires sorted output
- Use `where` filters before joins, not after
- Avoid `distinct` — if you need it, the upstream model probably has a grain problem

## Data Types and Precision

- Financial amounts: always `decimal` or `numeric` with explicit precision — never `float` or `double`
- Dates: use `date` type, not `string` — parse strings to dates in staging models
- Timestamps: use `timestamp` with timezone awareness where applicable
- IDs: use `string`/`varchar` for external identifiers — never assume numeric
- Booleans: use `boolean` type, not integer 0/1 — cast in staging if needed

## Security

- Never store personally identifiable information (PII) in plaintext — hash or encrypt
- Never include real production data in test fixtures, seeds, or examples
- Never hardcode credentials, connection strings, or API keys
- Use `{{ var() }}` or environment variables for environment-specific configuration
- Filter sensitive columns in staging models — don't propagate PII downstream unless required
- Log and document which models contain or process PII

## Source Freshness

Define `loaded_at_field` and freshness thresholds for all sources:

```yaml
sources:
  - name: raw_claims
    loaded_at_field: _loaded_at
    freshness:
      warn_after: {count: 24, period: hour}
      error_after: {count: 48, period: hour}
```

Run `dbt source freshness` in CI to detect stale data before it reaches dashboards.

## Version Control and Workflow

- One model per file — file name matches model name exactly
- One logical change per commit — keep commits small and reviewable
- Write descriptive commit messages: "Add claim status validation to fct_claims", not "update model"
- Create a spec before building complex models — define inputs, outputs, grain, and business rules
- Archived or deprecated models: prefix with `_deprecated_` and add a deprecation notice in the description
- Use `dbt_project.yml` to set default materializations per directory — don't override in every model

## Anti-Patterns — Never Do This

- Never use `select *` in any CTE except the final select from `final`
- Never use bare `join` — always specify `inner join`, `left join`, etc.
- Never use `float` for money — always `decimal`/`numeric`
- Never put business logic in staging models — staging is for renaming and type casting only
- Never use `order by` in a CTE unless windowing requires it
- Never hardcode dates, thresholds, or magic numbers — use `var()` or a reference table
- Never build models that depend on other models' materialization strategy
- Never ignore test failures — fix the data issue or fix the test, but don't remove it
