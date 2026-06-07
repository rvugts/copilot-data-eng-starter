# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the project. An ADR is a short document describing an important architectural decision and its context, consequences, and alternatives.

## What is an ADR?

An ADR captures a single significant technical decision that affects the codebase. It includes:
- **Context**: The problem or question that led to the decision
- **Decision**: What we decided to do
- **Rationale**: Why we made this decision
- **Consequences**: The implications of this decision (positive and negative)
- **Alternatives**: Other options we considered and why we rejected them

ADRs are permanent records that help team members (and AI agents like Copilot) understand the reasoning behind technical choices.

## Files in This Directory

This starter ships with a template only — no pre-written ADRs. Your team creates ADRs as you make architectural decisions.

- **[adr.template.md](./adr.template.md)** — Copy this to create a new ADR

## Suggested First ADRs

When bootstrapping a data engineering project from this template, consider documenting these decisions early (titles only — write full ADRs when your team is ready):

1. **Medallion architecture layer naming** — Conventions for `stg_`, `int_`, `fct_`, `dim_`, and `rpt_` prefixes across dbt and Databricks
2. **dbt as transformation layer of record** — What logic belongs in dbt models vs Databricks notebooks or PySpark jobs
3. **Unity Catalog as single source of truth** — How table references, schemas, and access control are standardized

## Creating a New ADR

### When to Create an ADR

Create an ADR when:
- Making a significant architectural decision that affects multiple team members
- Choosing between competing approaches (batch vs streaming, dbt vs notebook transforms, etc.)
- Establishing patterns that will be used repeatedly (testing strategy, naming conventions, deployment model)
- Documenting important constraints or limitations

**Don't** create an ADR for:
- Minor implementation decisions (library choices, function names)
- Tactical changes that don't affect architecture
- Bug fixes or performance tweaks

### How to Create an ADR

1. **Copy the template:**
   ```bash
   cp docs/adr/adr.template.md docs/adr/ADR-001-short-title.md
   ```

2. **Find the next ADR number:**
   - Look at existing ADRs in this directory
   - Use the next sequential number (e.g., ADR-002)

3. **Follow the format:**
   - MUST include: Context, Decision, Consequences, Alternatives
   - SHOULD include: Rationale, Implementation Notes, References
   - Use the template at `docs/adr/adr.template.md`

4. **Submit for review:**
   - Create PR with ADR file
   - Request feedback from team leads/architects
   - Update status from "Proposed" to "Accepted" after approval

5. **Update this README:**
   - Add entry to the "Files in This Directory" section
   - Link to the new ADR file

## ADR Status Transitions

```
Proposed  →  Accepted  →  Deprecated
             (Default)     (if replaced)
                           ↓
                      Superseded by ADR-X
```

- **Proposed**: Under discussion, not yet approved
- **Accepted**: Team decision is final; follow this approach
- **Deprecated**: No longer recommended; use alternative
- **Superseded**: Replaced by newer ADR; see `Superseded By`

## Using ADRs as an AI Agent

When working with Copilot:
- Reference ADRs in your requests: "Per ADR-001, use `stg_<source>__<entity>` for staging models"
- Check ADRs before violating architectural decisions
- If an ADR seems wrong, propose a new ADR (don't silently violate)
- Link ADRs in code comments for complex decisions

**Example in a dbt model:**
```sql
-- ADR-001: Medallion layer naming
-- Staging models use stg_<source>__<entity> per team convention
select ...
```

## Querying ADRs

Find decisions related to a topic:

**Data modeling:**
- Should transformation logic live in dbt or notebooks? → See your dbt-as-layer-of-record ADR

**Naming & organization:**
- What prefix should staging models use? → See your medallion naming ADR

**Platform & governance:**
- How do we reference tables across environments? → See your Unity Catalog ADR

**When adding new decisions:**
- Search existing ADRs first (don't duplicate)
- Update related ADRs (add cross-references)
- If a new ADR contradicts an old one, mark the old as "Superseded"

## References

- [Michael Nygard's ADR Template](https://github.com/joelparkerhenderson/architecture-decision-record)
- [ADRs in Practice - thoughtworks.com](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- [ADR GitHub Repository](https://github.com/adr/adr)

## Questions?

- Missing or unclear ADR? Open an issue
- Want to propose a new architecture decision? Create a PR with a new ADR (Proposed status)
- Disagree with an existing ADR? Discuss in a team meeting and propose a superseding ADR if needed

---

**Maintained By:** [Team Lead]

**Last Updated:** 2026-06-07
