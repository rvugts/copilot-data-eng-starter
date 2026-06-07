# Copilot Data Engineering Starter — Repository Audit

**Date:** 2026-06-07  
**Scope:** Analysis after pivot from Terraform/Python multi-template starter to Copilot/VS Code data engineering starter (Python, dbt, Databricks, SDD/TDD).

> **Implementation status (2026-06-07):** Phases 1–3 complete. Backend/JS cruft removed; committed Makefile, pre-commit, CI, merged VS Code config; `dbt/README.md`, `databricks/README.md`, example spec, and `.vscode/mcp.json` template added. See git history for details.

---

## Executive Summary (original audit — 2026-06-07)

Historical findings that drove the cleanup (all addressed unless noted):

- Removed ADR-001/002, FastAPI/Django/React/Node instructions, `enable-python.sh`, template merge scripts
- Added single `Makefile`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`
- Merged Python + dbt + Databricks VS Code extensions into base config
- Added `docs/specs/` example, `dbt/` and `databricks/` README placeholders, `.vscode/mcp.json` template

**Remaining optional polish:** Retarget tests, pyright in CI, GitHub template docs — **done (2026-06-07)**. Future: designed social preview PNG, Dev Container.

---

## Repository Purpose Alignment

| Area | Alignment | Notes |
|------|-----------|-------|
| Copilot instructions (dbt, Databricks, SDD/TDD) | ✅ Strong | `copilot-instructions.md` lines 109–127 correctly describe data-eng stack |
| Skills (`.agents/skills/`) | ✅ Strong | Official dbt/Databricks skills seeded; SDD/TDD skills present; sole skills location per Agent Skills spec |
| ADRs | ❌ Misaligned | ADR-001/002 are FastAPI backend decisions |
| Dev tooling (Makefile, scripts) | ❌ Misaligned | Opt-in merge pattern from multi-language template era |
| Pre-commit | ⚠️ Partial | Python checks OK; bash hook has bugs; no dbt awareness |
| Documentation | ⚠️ Partial | README/DEVELOPMENT still center `enable-python.sh`; TROUBLESHOOTING is FastAPI-heavy |
| JavaScript/Node | ❌ Orphaned | No `package.json`, no JS source; instructions remain from old template |
| Terraform remnants | ⚠️ Minor | `.gitignore` only; no Terraform files or docs |

**Overall:** ~60% aligned. The AI guidance layer is ahead of the scaffolding layer. Template adopters get excellent Copilot rules but confusing setup scripts and contradictory ADRs.

---

## Remove

| Item | Path(s) | Reason | References to update |
|------|---------|--------|----------------------|
| Backend ADR: Monolithic architecture | `docs/adr/ADR-001-monolithic-backend-architecture.md` | FastAPI monolith decision irrelevant to data-eng starter; Copilot may cite it | `docs/adr/README.md` (lines 20–22, 103, 85–96), `docs/DEVELOPMENT.md` (line 283), `docs/adr/ADR-002` (lines 153, 226 cross-ref) |
| Backend ADR: Async I/O | `docs/adr/ADR-002-async-io-by-default.md` | FastAPI async patterns irrelevant; actively harmful in TROUBLESHOOTING | `docs/adr/README.md` (lines 24–26, 85–96, 106), `docs/DEVELOPMENT.md` (line 284), `docs/TROUBLESHOOTING.md` (lines 11–31, 238–275, 351–376), `docs/adr/ADR-001` (line 190 cross-ref) |
| Makefile template | `Makefile.python.template` | Template merge pattern being retired | `scripts/README.md`, `scripts/enable-python.sh`, `scripts/append-makefile.py`, `docs/DEVELOPMENT.md` (lines 76, 105) |
| Makefile merge script | `scripts/append-makefile.py` | No longer needed with single Makefile | `scripts/README.md` (lines 97–98), `scripts/enable-python.sh` (line 89), `docs/DEVELOPMENT.md` (line 76) |
| Pre-commit merge script | `scripts/append-precommit.py` | Replace with `pre-commit` framework or `make install-hooks` | `scripts/README.md` (lines 98), `scripts/enable-python.sh` (line 67), `docs/DEVELOPMENT.md` (line 77) |
| Node.js CI template | `.github/ci-templates/ci-nodejs.template.yml` | No Node projects in template; not referenced by any script | `scripts/README.md` (if mentioned), `.github/instructions/README.md` |
| React instructions | `.github/instructions/javascript/react.instructions.md` | No frontend in data-eng starter; examples in README mislead | `.github/instructions/README.md` (lines 23–25, 96–107, 229–232), `.github/copilot-instructions.md` (line 140), `docs/DEVELOPMENT.md` (line 112) |
| Node.js instructions | `.github/instructions/javascript/nodejs.instructions.md` | Same as above; `applyTo: "**/*.js,**/*.ts"` is overly broad | `.github/instructions/README.md` (lines 109–119), `.github/copilot-instructions.md` (line 140), `docs/DEVELOPMENT.md` (line 113) |
| Terraform gitignore exceptions (optional) | `.gitignore` lines 16–17, 108–117 | Files `settings.terraform.json` / `extensions.terraform.json` do not exist; Terraform section is dead weight | None critical — cleanup only |

---

## Keep (no changes)

| Category | Path(s) | Rationale |
|----------|---------|-----------|
| Core docs | `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE.md` | Foundation; need content updates elsewhere, not removal |
| AI setup | `docs/AI_SETUP.md` | Well-aligned with dbt/Databricks/MCP/skills |
| Vibe guide | `docs/VIBE_CODING_GUIDE.md` | Copilot workflow guide (needs minor script reference updates) |
| Spec template | `docs/spec.template.md` | SDD scaffold (FastAPI example in stack table should be updated separately) |
| ADR scaffold | `docs/adr/adr.template.md` | Keep for teams to write data-eng ADRs |
| Copilot root instructions | `.github/copilot-instructions.md` | Data-eng section is good; JS line can be removed with JS files |
| dbt instructions | `.github/instructions/dbt/dbt-sql.instructions.md` | Core stack |
| Databricks instructions | `.github/instructions/databricks/databricks.instructions.md` | Core stack |
| Python general | `.github/instructions/python/python-general.instructions.md` | Applies to PySpark/orchestration Python |
| TDD workflow | `.github/instructions/workflows/tdd.instructions.md` | Core workflow |
| Skills | `.agents/skills/**` | Sole skills location (Agent Skills spec — Copilot and Cursor both read from here) |
| Python config | `pyproject.toml`, `requirements.txt`, `tests/test_example.py` | TDD scaffold for Python utilities |
| VS Code base | `.vscode/settings.json`, `.vscode/extensions.json`, `mcp.json` (if present) | Shared Copilot/VS Code config |
| Python VS Code overlays | `.vscode/settings.python.json`, `.vscode/extensions.python.json` | Valid config; merge strategy may simplify |
| CI Python template | `.github/ci-templates/ci-python.template.yml` | Useful base; may promote to `.github/workflows/ci.yml` |
| PR template | `.github/pull_request_template.md` | Standard |
| Prompts/skills meta | `.agents/skills/generate-prompt/`, `run-prompt/` | SDD workflow support |

---

## Keep but Modify

| Item | Path(s) | Recommended change | Priority |
|------|---------|-------------------|----------|
| ADR README | `docs/adr/README.md` | Remove ADR-001/002 entries; replace query examples with data-eng topics (medallion, dbt testing); update "Using ADRs as an AI Agent" example | P0 |
| Development guide | `docs/DEVELOPMENT.md` | Remove `enable-python.sh` as primary path; document single Makefile; remove FastAPI/Django/React/Node references (lines 109–113, 283–284); update directory tree | P0 |
| Troubleshooting | `docs/TROUBLESHOOTING.md` | Remove/replace FastAPI async sections (lines 11–31, 238–275, 351–376); add dbt compile failures, Databricks auth, MCP setup issues | P0 |
| README | `README.md` | Replace step 2 "Run enable-python.sh" with `make install` or similar; update key files list | P0 |
| Instructions README | `.github/instructions/README.md` | Remove JS/FastAPI/Django sections and examples; add dbt/Databricks-first examples | P1 |
| Copilot instructions | `.github/copilot-instructions.md` | Remove JS reference (line 140); fix OAuth2/Django example (lines 177–179) to data-eng example | P1 |
| enable-python.sh | `scripts/enable-python.sh` | **Either remove entirely** or reduce to thin wrapper calling `make install` + venv creation — drop Makefile/pre-commit merge steps | P0 |
| VS Code merge script | `.vscode/merge-configs.py` | Merge Python/dbt extensions into base `extensions.json` at template level; script becomes optional or removed | P1 |
| VS Code README | `.vscode/README.md` | Document dbt/Databricks extensions; remove "add another language" merge pattern if simplified | P2 |
| Scripts README | `scripts/README.md` | Rewrite for simplified toolchain | P0 |
| Pre-commit template | `.github/hooks/pre-commit.template` | Replace with `.pre-commit-config.yaml` or fix bugs (`git staged-files` → `git diff --cached --name-only`) | P0 |
| CI Python template | `.github/ci-templates/ci-python.template.yml` | Add optional dbt parse job (conditional on `dbt_project.yml`); promote to committed workflow | P1 |
| Spec template | `docs/spec.template.md` | Change stack example from FastAPI to dbt model / Databricks job | P2 |
| create-spec skill | `.agents/skills/create-spec/SKILL.md` | Update stack options — de-emphasize FastAPI/Django/Node defaults | P2 |
| pyproject.toml | `pyproject.toml` | Rename project from `copilot-dev-starter` to `copilot-data-eng-starter`; consider moving pytest-asyncio to optional unless needed | P2 |
| .gitignore | `.gitignore` | Remove Terraform exceptions; keep Node section (harmless); **remove `prompts/` from gitignore** — prompts are part of template workflow | P1 |
| VIBE_CODING_GUIDE | `docs/VIBE_CODING_GUIDE.md` | Update `enable-python.sh` references (lines 389, 445) | P1 |
| FastAPI instructions | `.github/instructions/python/python-fastapi.instructions.md` | **Remove or move to `docs/archive/`** — path `**/fastapi/**/*.py` won't trigger in data-eng repos but docs still reference it | P1 |
| Django instructions | `.github/instructions/python/python-django.instructions.md` | Same as FastAPI | P1 |

---

## Add (gaps)

| Item | Priority | Rationale | Suggested location |
|------|----------|-----------|-------------------|
| Single committed Makefile | P0 | Adopters expect `make test` immediately; no setup script required | `./Makefile` |
| `.pre-commit-config.yaml` | P0 | Standard, maintainable, supports dbt/sqlfluff hooks opt-in | `./.pre-commit-config.yaml` |
| Committed CI workflow | P0 | Template should ship working CI, not copy-from-template step | `.github/workflows/ci.yml` |
| Example spec | P0 | SDD workflow references `docs/specs/spec.md` but directory is empty | `docs/specs/example-dbt-staging-models.spec.md` + README in `docs/specs/` |
| dbt VS Code extensions | P0 | Teams expect dbt Power User or similar in recommendations | Merge into `.vscode/extensions.json` |
| Databricks VS Code extension | P1 | Databricks extension for notebook/job editing | `.vscode/extensions.json` |
| dbt project placeholder README | P1 | Teams need guidance on where dbt lives | `dbt/README.md` (placeholder, not full project) |
| Databricks bundle placeholder | P1 | Documents expected `databricks.yml` location | `databricks/README.md` or root comment in Makefile |
| Sample ADR titles (not content) | P1 | Scaffold data-eng decisions for teams to fill in | Document in `docs/adr/README.md` |
| `make install` target | P0 | One command: venv + deps + pre-commit install | `./Makefile` |
| CONTRIBUTING data-eng focus | P2 | Mention dbt/Databricks contribution patterns | `CONTRIBUTING.md` |

**Suggested starter ADR titles (do not write yet):**
- ADR-001: Medallion architecture layer naming (`stg_` / `int_` / `fct_` / `dim_`)
- ADR-002: dbt as transformation layer of record (vs notebook logic)
- ADR-003: Unity Catalog as single source of truth for table references

---

## Makefile Recommendation

### Current state

- `Makefile.python.template` — 62 lines, Python-only targets
- No committed `Makefile` in repo (generated locally by `enable-python.sh` → `append-makefile.py`)
- `append-makefile.py` parses and appends targets idempotently
- `enable-python.sh` orchestrates venv, CI copy, pre-commit merge, VS Code merge, Makefile merge

**Problems for template adopters:**
1. `make help` fails on fresh clone until obscure script runs
2. No dbt/Databricks commands despite being core stack
3. Two-step mental model (clone → enable-python → make) vs industry standard (clone → make install)

### Proposed single Makefile design

Replace template + merge with one committed `Makefile` organized in sections:

```makefile
# Sections: help | setup | python | dbt (opt-in) | databricks (opt-in) | ci
```

**Detection variables (top of file):**
```makefile
DBT_PROJECT := $(wildcard dbt_project.yml dbt/dbt_project.yml)
DATABRICKS_BUNDLE := $(wildcard databricks.yml)
```

**Core targets (always available):**

| Target | Behavior |
|--------|----------|
| `help` | Grouped output: Setup, Python, dbt (if detected), Databricks (if detected) |
| `install` | Create venv, `pip install -r requirements.txt`, `pre-commit install` |
| `test` | `pytest --cov=src --cov-fail-under=80` |
| `test-watch` | pytest-watch |
| `lint` | pylint + flake8 on `src/` `tests/` |
| `format` | black |
| `type-check` | pyright |
| `pre-commit` | Run all local checks |
| `clean` | Remove caches |
| `all` | lint → format → type-check → test |

**dbt targets (opt-in — skip with message if no project):**

| Target | Behavior when absent | Behavior when present |
|--------|---------------------|----------------------|
| `dbt-deps` | Print: "No dbt_project.yml found. See dbt/README.md" | `dbt deps` |
| `dbt-parse` | Same | `dbt parse` |
| `dbt-compile` | Same | `dbt compile` |
| `dbt-run` | Same | `dbt run` |
| `dbt-test` | Same | `dbt test` |
| `dbt-build` | Same | `dbt build` |
| `dbt-docs` | Same | `dbt docs generate && dbt docs serve` |

Implementation pattern:
```makefile
define require_dbt
	@if [ -z "$(DBT_PROJECT)" ]; then \
		echo "⏭️  Skipping: no dbt_project.yml found. Add a dbt project or see dbt/README.md"; \
		exit 0; \
	fi
endef
```

**Databricks targets (opt-in):**

| Target | Behavior when absent | Behavior when present |
|--------|---------------------|----------------------|
| `databricks-validate` | Print guidance | `databricks bundle validate` |
| `databricks-deploy` | Print guidance | `databricks bundle deploy` |
| `databricks-run` | Print guidance | `databricks bundle run` (with `JOB` var) |

**Migration from template system:**

1. Create `Makefile` from `Makefile.python.template` content + dbt/Databricks sections
2. Delete `Makefile.python.template`, `scripts/append-makefile.py`
3. Update `enable-python.sh` to only create venv (or delete script; `make install` replaces it)
4. Update all docs referencing `make` after `enable-python.sh`

---

## Pre-commit Recommendation

### Current state

- `.github/hooks/pre-commit.template` — bash script copied/merged into `.git/hooks/pre-commit`
- `scripts/append-precommit.py` — merge-by-language-section pattern
- Checks: pytest 80% coverage (blocking), pyright (warn), pylint (warn), black (warn), secret grep (interactive prompt)
- **Bug:** line 83 uses `git staged-files` — not a git subcommand; should be `git diff --cached --name-only`

### Recommended approach: `pre-commit` Python framework

**Why:** Industry standard; hook definitions in repo (`.pre-commit-config.yaml`); `make install` runs `pre-commit install`; no merge scripts; easy to add dbt/sqlfluff as optional local hooks; works in CI via `pre-commit run --all-files`.

**Proposed `.pre-commit-config.yaml`:**

| Hook | Stage | Blocking? | Notes |
|------|-------|-----------|-------|
| `black` | commit | yes | `src/`, `tests/`, `scripts/` |
| `flake8` | commit | yes | |
| `pyright` | commit | warn (or yes for strict teams) | |
| `pytest` with coverage | commit | yes | `--cov-fail-under=80` |
| `detect-secrets` or `gitleaks` | commit | yes | Replace fragile grep |
| `dbt-parse` | commit | opt-in | Local hook; only runs if `dbt_project.yml` exists |
| `sqlfluff-lint` | commit | opt-in | Only on `models/**/*.sql` if sqlfluff configured |

**dbt opt-in strategy:** Use `files:` pattern in pre-commit config targeting `dbt/` or root `dbt_project.yml`. Document in README that teams without dbt can delete those hook entries — or use a `pre-commit-config.dbt.yaml` overlay documented in `dbt/README.md`.

**Remove:** `.github/hooks/pre-commit.template`, `scripts/append-precommit.py`

**Add Makefile target:** `install-hooks` → `pre-commit install`

**Alternative (if avoiding pre-commit dependency):** Single committed `.github/hooks/pre-commit` installed via `make install-hooks` with fixed bash script — less flexible, but simpler dependency tree. Recommendation: prefer `pre-commit` framework given dbt hook ecosystem.

---

## JavaScript/Node Recommendation

### Recommendation: **Remove instruction files and CI template; keep .gitignore entries**

### Artifacts found

| Path | Status |
|------|--------|
| `.github/instructions/javascript/react.instructions.md` | Orphaned |
| `.github/instructions/javascript/nodejs.instructions.md` | Orphaned |
| `.github/ci-templates/ci-nodejs.template.yml` | Orphaned |
| `.gitignore` Node section (lines 56–73) | Keep — harmless if teams add JS tooling later |
| No `package.json`, no `.js`/`.tsx` source | Confirms no active JS stack |

### Pros of keeping

- Future-proofs for teams adding a dbt docs site (Next.js) or metrics frontend
- Zero runtime cost if files exist but aren't referenced

### Cons of keeping (decisive)

- **Copilot doc pollution:** `.github/instructions/README.md` dedicates ~40 lines to React/Node with worked examples; `docs/DEVELOPMENT.md` lists them as active guidelines
- **Misleading examples:** Copilot instructions example references `python-django.instructions.md` for OAuth2 (line 177–179 of `copilot-instructions.md`)
- **Broad applyTo on nodejs.instructions.md:** `**/*.ts` would activate on any TypeScript file if a team adds one unrelated file
- **No enable-nodejs.sh:** Asymmetric with Python — Node CI template has no setup path

### Could JS serve a legitimate purpose?

- dbt docs static site (dbt generates HTML, rarely needs Node in repo)
- Lightdash/Metabase embedding — out of scope for starter
- **Verdict:** Not worth keeping in primary template. Document in CONTRIBUTING: "Teams needing frontend can add `.github/instructions/javascript/` from git history or create fresh."

---

## Scripts & CI Recommendation

| Script/Template | Recommendation | Rationale |
|-----------------|----------------|-----------|
| `scripts/enable-python.sh` | **Remove or reduce to `make install` alias** | Template should ship ready; script's CI/pre-commit/Makefile merge steps obsolete |
| `scripts/append-makefile.py` | **Remove** | Single Makefile replaces |
| `scripts/append-precommit.py` | **Remove** | pre-commit framework replaces |
| `.vscode/merge-configs.py` | **Keep temporarily, then remove** | Merge Python+dbt extensions into base configs first |
| `.github/ci-templates/ci-python.template.yml` | **Promote to `.github/workflows/ci.yml`** | Adopters shouldn't copy templates manually |
| `.github/ci-templates/ci-nodejs.template.yml` | **Remove** | No Node stack |
| `.github/ci-templates/` directory | **Keep if other templates planned; else remove after CI promotion** | |

**Proposed CI workflow (`.github/workflows/ci.yml`):**

```yaml
jobs:
  python:
    # Current ci-python.template.yml content
  dbt:
    if: hashFiles('dbt_project.yml', 'dbt/dbt_project.yml') != ''
    steps:
      - run: dbt deps && dbt parse
```

**Should starter ship pre-wired?** **Yes.** Data-eng teams expect:
- Working Python test/lint on clone
- `make install` for venv
- CI that runs on first push
- Optional dbt CI when they add a project

The opt-in `enable-python.sh` pattern made sense for a multi-language chooser; it does not fit a focused data-eng starter.

---

## ADR Strategy

### ADR-001 and ADR-002: Confirm removal

Both are **inappropriate** for this repository:

| ADR | Topic | Why remove |
|-----|-------|------------|
| ADR-001 | FastAPI monolith vs microservices | Data-eng teams build pipelines, not REST monoliths |
| ADR-002 | Async I/O by default for FastAPI | Drives wrong Copilot behavior; TROUBLESHOOTING enforces it |

### Complete reference inventory

| File | References |
|------|------------|
| `docs/adr/ADR-001-monolithic-backend-architecture.md` | Self; cross-ref to ADR-002 (line 97, 153, 190) |
| `docs/adr/ADR-002-async-io-by-default.md` | Self; cross-ref to ADR-001 (line 153, 226) |
| `docs/adr/README.md` | ADR-001 (lines 20–22, 103), ADR-002 (lines 24–26, 85–96, 106), examples (lines 92–96) |
| `docs/DEVELOPMENT.md` | ADR-001 (line 283), ADR-002 (line 284) |
| `docs/TROUBLESHOOTING.md` | ADR-002 extensively (lines 11–31, 238–275, 351–376) |
| `.agents/skills/working-with-dbt-mesh/SKILL.md` | "monolithic dbt project" — **keep** (different meaning: monolithic dbt project vs mesh) |
| `.agents/skills/refactor-python/SKILL.md` | async guidance — **keep** (generic Python, not ADR reference) |
| `.agents/skills/create-spec/SKILL.md` | FastAPI in stack table — update, not ADR ref |
| `docs/spec.template.md` | FastAPI in example stack table — update |
| `.github/instructions/python/python-fastapi.instructions.md` | FastAPI patterns — remove file |
| `.github/copilot-instructions.md` | Django OAuth2 example — update |

No references in: `README.md`, `docs/AI_SETUP.md`, dbt/Databricks instructions, `.agents/skills/dbt*`, `.agents/skills/databricks/`.

### Post-removal ADR directory strategy

**Keep scaffold only:**
- `docs/adr/adr.template.md`
- `docs/adr/README.md` (rewritten for data-eng)

**Do not ship pre-written data-eng ADRs** in the template — teams should write their own. Document suggested first ADRs in README (titles only, listed in Add section above).

---

## Copilot Instruction Coherence

### What's working

- `copilot-instructions.md` Data Engineering Stack section (lines 109–132) is accurate and well-structured
- dbt `applyTo` patterns are carefully scoped (excludes random YAML)
- Databricks instructions cover PySpark, Unity Catalog, secrets
- Skills in `.agents/skills/` provide invocable workflows

### Conflicts and inconsistencies

| Issue | Location | Impact |
|-------|----------|--------|
| Django OAuth2 example | `copilot-instructions.md:177–179` | Copilot may suggest Django for auth in a dbt repo |
| JS listed as active stack | `copilot-instructions.md:140` | Implies JS is expected |
| FastAPI/Django in DEVELOPMENT | `docs/DEVELOPMENT.md:109–113` | Onboarding directs to wrong instructions |
| FastAPI path instructions exist | `python-fastapi.instructions.md` | Docs say to read it; file won't auto-apply without `fastapi/` dir |
| ADR async enforcement | `docs/TROUBLESHOOTING.md` | Copilot told to enforce async for all I/O |
| create-spec defaults | `create-spec/SKILL.md` | FastAPI/Django/Node as stack options |
| Duplicate skill locations | `.agents/skills/` vs `.github/skills/` | Maintenance burden; may drift |

### Recommendations

1. **Remove** FastAPI, Django, React, Node instruction files
2. **Update** all doc examples to reference dbt model, PySpark job, or Python utility
3. **Clarify skills location** in README: `.agents/skills/` is the sole location per Agent Skills spec
4. **Add** `python-pyspark.instructions.md` (optional P2) scoped to `**/notebooks/**`, `**/jobs/**` if teams want PySpark-specific rules separate from general Python

---

## Implementation Roadmap

### Phase 1: Quick wins (1–2 hours, no structural dependency)

Remove misleading content; update docs.

1. Delete `docs/adr/ADR-001-monolithic-backend-architecture.md` and `ADR-002-async-io-by-default.md`
2. Update `docs/adr/README.md` — remove entries and FastAPI examples
3. Update `docs/DEVELOPMENT.md` — remove ADR-001/002, FastAPI/Django/React/Node refs
4. Rewrite `docs/TROUBLESHOOTING.md` — remove async/FastAPI sections; add 2–3 data-eng troubleshooting entries
5. Delete `.github/instructions/javascript/` directory
6. Delete `.github/ci-templates/ci-nodejs.template.yml`
7. Remove FastAPI/Django instruction files (or move to archive)
8. Update `.github/instructions/README.md` and `.github/copilot-instructions.md`

**Dependencies:** None  
**Verification:** `rg "ADR-00[12]|FastAPI|enable-python" docs/` returns only historical/changelog mentions if any

### Phase 2: Structural tooling (half day)

Replace template merge system with committed tooling.

1. Create `Makefile` (Python + opt-in dbt/Databricks targets per spec above)
2. Create `.pre-commit-config.yaml`; add `pre-commit` to `requirements.txt`
3. Delete `Makefile.python.template`, `scripts/append-makefile.py`, `scripts/append-precommit.py`, `.github/hooks/pre-commit.template`
4. Promote `ci-python.template.yml` → `.github/workflows/ci.yml`; add conditional dbt job
5. Simplify or remove `scripts/enable-python.sh`
6. Merge Python + dbt + Databricks extensions into `.vscode/extensions.json`
7. Update `README.md`, `scripts/README.md`, `docs/VIBE_CODING_GUIDE.md`
8. Clean `.gitignore` (Terraform exceptions, un-ignore `prompts/`)

**Dependencies:** Phase 1 complete (docs won't reference deleted scripts)  
**Verification:** Fresh clone → `make install` → `make test` passes; `make dbt-parse` prints skip message

### Phase 3: Enhancements (1–2 days)

Fill gaps for full data-eng starter experience.

1. Add `docs/specs/README.md` + example spec file
2. Add `dbt/README.md` and `databricks/README.md` placeholders
3. Document suggested ADR titles in `docs/adr/README.md`
4. Update `create-spec` skill stack defaults
5. Rename `pyproject.toml` project to `copilot-data-eng-starter`
6. Update audit doc for skills migration and maintainer decisions
7. Optional: `python-pyspark.instructions.md`
8. Update `CONTRIBUTING.md` with data-eng contribution patterns

**Dependencies:** Phase 2 complete  
**Verification:** New adopter can follow README → AI_SETUP → create-spec → dbt skill without hitting stale references

---

## Open Questions

**Resolved (2026-06-07):**

1. **Skills location:** `.agents/skills/` only — migration complete; `.github/skills/` does not exist and must not be recreated.
2. **`enable-python.sh`:** Remove in Phase 2 — Python is the default; template should ship pre-wired with `make install`.
3. **dbt scaffold:** Minimal `dbt/README.md` placeholder only (Phase 3) — no `dbt_project.yml` in starter.

**Still open:**

4. **pre-commit blocking vs warning:** Should dbt parse block commits when a dbt project exists?
5. **pytest-asyncio in requirements:** Move to optional unless needed for data-eng utilities?
6. **CI dbt version:** Pin dbt version in CI or use team's adapter/packages?
7. **prompts/ in .gitignore:** Un-ignore in Phase 2 — conflicts with SDD prompt workflow.

---

*End of audit. Ready for implementation prompt targeting Phase 1 → Phase 2 → Phase 3.*
