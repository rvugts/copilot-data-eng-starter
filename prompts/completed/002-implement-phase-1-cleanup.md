<objective>
Implement **Phase 1** of the repository cleanup defined in `@analyses/repo-template-audit.md`: remove misleading backend/JS content left over from the old multi-language starter, and update documentation so the repo accurately reflects a **Copilot/VS Code data engineering starter** (Python, dbt, Databricks, SDD/TDD).

This phase is **content removal and doc updates only**. Do not yet create the Makefile, pre-commit config, or delete `enable-python.sh` — those belong to Phase 2. However, **stop presenting `enable-python.sh` as the primary onboarding path** in docs you touch; use language that anticipates `make install` (Phase 2).

Explain WHY each change matters in commit-ready terms: template adopters and Copilot must not receive FastAPI, async-I/O, or React/Node guidance in a data-eng starter.
</objective>

<context>
**Source of truth:** `@analyses/repo-template-audit.md` — Phase 1 section and "Remove" / "Keep but Modify" tables.

**Maintainer decisions (locked in):**
- **Skills:** `.agents/skills/` is the **only** skills location (Agent Skills spec). `.github/skills/` does not exist and must not be recreated or referenced.
- **`enable-python.sh`:** Will be **removed in Phase 2** — Python is the default for this audience. In Phase 1 docs, de-emphasize or remove "run enable-python.sh first" without deleting the script yet.
- **dbt/Databricks scaffolds:** Minimal placeholder READMEs only — **Phase 3**, not this prompt.

**Repo purpose:** Starter template for data engineering teams using VS Code + GitHub Copilot with Python, dbt, Databricks, SDD, and TDD.

**Read before editing:**
@analyses/repo-template-audit.md
@README.md
@docs/DEVELOPMENT.md
@docs/TROUBLESHOOTING.md
@docs/adr/README.md
@docs/VIBE_CODING_GUIDE.md
@.github/copilot-instructions.md
@.github/instructions/README.md
@docs/spec.template.md
@.agents/skills/create-spec/SKILL.md
</context>

<requirements>

## 1. Delete obsolete ADRs

Delete these files entirely:
- `./docs/adr/ADR-001-monolithic-backend-architecture.md`
- `./docs/adr/ADR-002-async-io-by-default.md`

## 2. Delete obsolete instruction files and JS/Node artifacts

Delete:
- `./.github/instructions/javascript/` (entire directory: `react.instructions.md`, `nodejs.instructions.md`)
- `./.github/instructions/python/python-fastapi.instructions.md`
- `./.github/instructions/python/python-django.instructions.md`
- `./.github/ci-templates/ci-nodejs.template.yml`

Do **not** delete `python-general.instructions.md`, dbt, Databricks, or TDD instructions.

## 3. Rewrite `docs/adr/README.md`

- Remove all ADR-001 and ADR-002 entries, cross-references, and FastAPI/async code examples
- Retain ADR template usage guidance (`adr.template.md`)
- Replace "querying ADRs" examples with **data engineering topics** (e.g., medallion naming, dbt as transformation layer, Unity Catalog conventions)
- Add a **"Suggested first ADRs"** section with titles only (do not write full ADRs):
  - Medallion architecture layer naming
  - dbt as transformation layer of record
  - Unity Catalog as single source of truth for table references

## 4. Update `docs/DEVELOPMENT.md`

- Remove references to ADR-001, ADR-002, FastAPI, Django, React, and Node.js instructions
- Update directory tree to reflect current structure (no `.github/skills/`, no javascript instructions)
- Replace `enable-python.sh` as primary setup with: "Python tooling ships with the template; run `make install` (coming in Phase 2) or `pip install -r requirements.txt` and `pytest` for now" — honest about current state if Makefile doesn't exist yet
- Point skills readers to `.agents/skills/` only
- Keep SDD/TDD philosophy intact

## 5. Rewrite `docs/TROUBLESHOOTING.md`

Remove or replace these misaligned sections:
- ADR-002 async I/O enforcement (including FastAPI endpoint examples)
- FastAPI async testing guidance
- "Should I violate ADR-001/002?" sections
- Database connection pooling / FastAPI async driver advice

Add **2–3 new data-eng troubleshooting entries**, e.g.:
- Copilot suggests hardcoded table names instead of `{{ ref() }}` / `{{ source() }}`
- dbt MCP server not connecting (point to `docs/AI_SETUP.md`)
- Databricks auth / `dbutils.secrets` patterns

Keep generic Copilot/SDD/TDD troubleshooting where still valid.

## 6. Update `.github/instructions/README.md`

- Remove JavaScript, FastAPI, and Django sections and directory-tree entries
- Remove examples referencing React components and FastAPI routes
- Add/replace examples with dbt model and Databricks/PySpark file scenarios
- Ensure skills reference points to `.agents/skills/` not `.github/skills/`

## 7. Update `.github/copilot-instructions.md`

- Remove JavaScript/TypeScript from language/framework list (line ~140 area)
- Replace Django OAuth2 example with a data-eng example (e.g., dbt staging model or PySpark job following `@docs/specs/spec.md`)
- Verify Data Engineering Stack section remains intact

## 8. Update root and ancillary docs

**`README.md`:**
- Remove or soften "Run `bash scripts/enable-python.sh`" as step 2; describe Python as included by default
- Ensure skills path is `.agents/skills/` only
- Remove JS/Node from key files or stack descriptions if present

**`docs/VIBE_CODING_GUIDE.md`:**
- Replace `enable-python.sh` references with current/future onboarding (`pip install -r requirements.txt` or forthcoming `make install`)

**`docs/spec.template.md`:**
- Change stack example from FastAPI to dbt model / Databricks job / Python utility

**`.agents/skills/create-spec/SKILL.md`:**
- De-emphasize FastAPI/Django/Express as default stack options; lead with Databricks-PySpark-SQL / dbt / Python data-eng stacks

**`scripts/README.md`:**
- Add a note that `enable-python.sh` and merge scripts are **deprecated, scheduled for Phase 2 removal** — do not recommend for new adopters

**`analyses/repo-template-audit.md`:**
- Fix the stale claim about `.github/skills/` duplication (skills live only in `.agents/skills/`)
- Record maintainer decisions in Open Questions section (enable-python removal, minimal dbt README, skills location)

**`.vscode/README.md`:**
- Remove or update references to `enable-python.sh` if present; note Python extensions will be merged into base config in Phase 2

</requirements>

<constraints>
- **Phase 1 scope only** — no Makefile, no `.pre-commit-config.yaml`, no deletion of `enable-python.sh` / merge scripts yet
- Do **not** create `dbt/README.md` or `databricks/README.md` (Phase 3)
- Do **not** recreate `.github/skills/`
- Minimize scope: only edit files required by the changes above
- Match existing doc tone and formatting
- When removing content, grep the repo for orphaned references and fix them in the same pass
- Do **not** create git commits unless explicitly asked
</constraints>

<implementation>
Work in this order:

1. Run ripgrep for `ADR-001`, `ADR-002`, `ADR-00`, `FastAPI`, `enable-python`, `javascript/`, `react.instructions`, `nodejs.instructions`, `python-fastapi`, `python-django`, `.github/skills` — build a checklist
2. Delete obsolete files (section 1–2)
3. Update docs in dependency order: `docs/adr/README.md` → `DEVELOPMENT.md` → `TROUBLESHOOTING.md` → instructions README → copilot-instructions → README → ancillary
4. Re-run ripgrep to catch missed references
5. Fix audit doc stale content

For maximum efficiency, batch independent file reads and greps in parallel.
</implementation>

<verification>
Before declaring complete:

1. `rg "ADR-00[12]" --glob '!analyses/*' --glob '!prompts/completed/*'` returns **no matches** (or only the audit's historical mention if you choose to keep a changelog note — prefer zero)
2. `rg "FastAPI|python-fastapi|python-django|react\.instructions|nodejs\.instructions" docs/ .github/` returns **no matches** in active guidance (skills may mention FastAPI in stack tables only if updated to de-emphasize)
3. `rg "\.github/skills"` returns **no matches** outside audit/history
4. `docs/adr/` contains only `README.md` and `adr.template.md` (no ADR-001/002)
5. `.github/instructions/javascript/` does not exist
6. `docs/TROUBLESHOOTING.md` has no ADR-002 async enforcement content
7. Read lints not required for markdown-only changes
</verification>

<success_criteria>
- Backend ADRs and all references removed
- JS/Node/FastAPI/Django instruction files deleted; docs no longer point to them
- ADR README rewritten for data-eng starter with suggested first ADR titles
- TROUBLESHOOTING aligned with dbt/Databricks/Python workflows
- Copilot instructions and README describe `.agents/skills/` as sole skills location
- Audit doc corrected for skills migration and maintainer decisions
- No Phase 2/3 work accidentally included
</success_criteria>
