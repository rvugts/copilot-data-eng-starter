# Specifications (SDD)

This folder holds **Specification-Driven Development (SDD)** documents — the contract between requirements and implementation.

## Active spec

| File | Purpose |
|------|---------|
| `spec.md` | **Current active spec** — Copilot and developers reference `@docs/specs/spec.md` during implementation |

Create a new active spec with the `/create-spec` skill or by copying `docs/spec.template.md` to `spec.md`.

When a new spec replaces the current one, the skill archives the old `spec.md` to `{name}.md` using the frontmatter `name` field (see `docs/spec.template.md`).

## Example

| File | Purpose |
|------|---------|
| [example-stg-orders-models.spec.md](./example-stg-orders-models.spec.md) | Worked example — staging models for a raw orders source (not the active spec) |

Use it as a reference for structure and level of detail. Do not treat it as the live contract unless you copy it to `spec.md`.

## Workflow

1. Write spec → get review → status **Approved**
2. `/create-tasks` → `docs/specs/tasks.md`
3. TDD: tests first (pytest for Python, `/adding-dbt-unit-test` for dbt)
4. Implement against the spec; verify every FR has a test

See `docs/DEVELOPMENT.md` and `docs/VIBE_CODING_GUIDE.md` for the full workflow.
