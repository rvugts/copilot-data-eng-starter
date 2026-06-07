---
name: example-stg-orders-models
---

# Specification: Staging Models for Raw Orders

**Version:** 1.0.0  
**Date:** 2026-06-07  
**Status:** Example (not active — for reference only)  
**Owner:** Data Platform Team

> Example spec demonstrating SDD for a dbt feature. Copy structure to `spec.md` when starting real work.

---

## 1. Context

### 1.1 Problem Statement

Analysts need a cleaned, tested staging layer for the `raw.orders` source before building marts.

### 1.2 Business Value

- Single source of truth for order attributes used downstream
- Data quality gates (not_null, unique on `order_id`) before marts

---

## 2. Scope

### 2.1 In Scope

- One staging model: `stg_orders` from `{{ source('raw', 'orders') }}`
- Column renaming to snake_case, type casting for `order_id` and `order_timestamp`
- `schema.yml` with `not_null` + `unique` on `order_id`

### 2.2 Out of Scope

- Fact/dimension marts
- Incremental logic (full refresh staging only for v1)
- PII masking

---

## 3. Requirements

| ID | Requirement | Acceptance Criteria | Priority |
|----|-------------|---------------------|----------|
| FR-1 | Staging model exists | `models/staging/stg_orders.sql` compiles with `dbt parse` | Must Have |
| FR-2 | Source reference | Uses `{{ source('raw', 'orders') }}` — no hardcoded table names | Must Have |
| FR-3 | Primary key tests | `order_id` has `not_null` and `unique` in `schema.yml` | Must Have |
| FR-4 | Unit test (TDD) | `/adding-dbt-unit-test` defines expected output for cancelled-order exclusion before SQL | Should Have |

---

## 4. Technical Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Transform | dbt | 1.8+ |
| Warehouse | Databricks SQL | — |
| Adapter | dbt-databricks | latest stable |

---

## 5. Success Criteria

- [ ] `dbt build --select stg_orders` passes in dev
- [ ] All FR-* acceptance criteria met
- [ ] Spec requirements traceable to dbt tests in `schema.yml`

---

## 6. Open Questions

- Should cancelled orders be filtered in staging or intermediate layer?
