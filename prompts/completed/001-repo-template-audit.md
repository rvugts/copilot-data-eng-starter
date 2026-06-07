<objective>
Perform a thorough audit of this repository to determine what should be removed, kept, or added now that it has pivoted from a Terraform/Python starter template to a **Copilot/VS Code starter for data engineering teams**.

The repo's intended focus is **Python**, **dbt**, and **Databricks**, with **Specification-Driven Development (SDD)** and **Test-Driven Development (TDD)** as first-class workflows (instructions + skills).

This is an **analysis-only** task. Do not implement changes. Produce a prioritized, actionable audit document that a follow-up implementation prompt can execute against.

Explain WHY each recommendation matters for teams adopting this as a GitHub template — not just what to change.
</objective>

<context>
**Development context:** This repo is developed in Cursor but is intended for use in VS Code with GitHub Copilot. Treat `.github/copilot-instructions.md`, `.github/instructions/`, `.agents/skills/`, and `.github/skills/` as the primary AI guidance surfaces.

**Known issues the maintainer has already identified:**
- `docs/adr/ADR-001-monolithic-backend-architecture.md` and `docs/adr/ADR-002-async-io-by-default.md` are backend/FastAPI decisions that do not fit a data engineering starter — flag for removal along with all references
- `Makefile.python.template` and scripts like `scripts/append-makefile.py` / `scripts/enable-python.sh` reflect an old multi-template Makefile merge system (previously Python + Terraform). The maintainer believes a **single Makefile** without the template/merge concept is preferable
- `.github/hooks/pre-commit.template` and `scripts/append-precommit.py` may need rework for this repo's actual stack
- JavaScript/Node artifacts may or may not belong — evaluate rather than assume

**Stack the template should optimize for:**

| Tool | Role |
|------|------|
| dbt | SQL transformations, tests, docs |
| Databricks | Jobs, notebooks, workflows, Unity Catalog |
| Python / PySpark | Orchestration, utilities, transforms |
| SDD/TDD | Spec and task skills, TDD instructions |

**Key areas to examine:**

@README.md
@CONTRIBUTING.md
@docs/DEVELOPMENT.md
@docs/AI_SETUP.md
@docs/VIBE_CODING_GUIDE.md
@docs/TROUBLESHOOTING.md
@docs/adr/
@docs/spec.template.md
@Makefile.python.template
@scripts/
@.github/hooks/pre-commit.template
@.github/ci-templates/
@.github/instructions/
@.github/copilot-instructions.md
@.vscode/
@pyproject.toml
@requirements.txt

Search the entire repo for stale references to: `terraform`, `FastAPI`, `monolith`, `async I/O`, `enable-python`, `append-makefile`, `append-precommit`, `ci-nodejs`, and any other remnants of the old starter identity.
</context>

<analysis_requirements>

## 1. Inventory and classification

Thoroughly analyze the repository and classify every significant file/directory into one of:

- **Keep as-is** — aligned with data-eng + Copilot + SDD/TDD purpose
- **Keep but modify** — right idea, wrong content or outdated patterns
- **Remove** — obsolete, misleading, or harmful for the target audience
- **Add (gap)** — missing capability teams would expect from this starter

Group findings by category:
- Documentation (`docs/`, root markdown)
- ADRs (`docs/adr/`)
- Copilot instructions and skills (`.github/instructions/`, `.github/skills/`, `.agents/skills/`)
- Build/dev tooling (Makefile, scripts, pre-commit, CI templates)
- VS Code config (`.vscode/`)
- Python project config (`pyproject.toml`, `requirements.txt`, `tests/`)
- JavaScript/Node artifacts (instructions, CI templates, any other Node-related files)

For each item flagged **Remove** or **Keep but modify**, cite the specific file path and explain the impact on template adopters if left unchanged.

## 2. ADR cleanup

- Confirm ADR-001 and ADR-002 are inappropriate for this repo and should be removed
- Find **every reference** to these ADRs across the repo (docs, instructions, skills, comments, README, etc.)
- Recommend whether `docs/adr/` should remain as an empty scaffold (template + README only) or include **new starter ADRs** relevant to data engineering (e.g., dbt project layout, medallion architecture, testing strategy). If recommending new ADRs, suggest titles only — do not write them.

## 3. Makefile consolidation

Analyze the current template/merge approach:

@Makefile.python.template
@scripts/append-makefile.py
@scripts/enable-python.sh

Recommend a **single Makefile** design that:

- Replaces the template + `append-makefile.py` merge pattern entirely
- Keeps existing Python targets (`test`, `lint`, `format`, `type-check`, `all`, etc.) where still appropriate
- Adds **optional/opt-in** dbt and Databricks targets that gracefully skip or print helpful guidance when tooling or project files are absent (e.g., no `dbt_project.yml`, no `databricks.yml`)
- Avoids a cluttered `make help` — propose grouping or conditional sections
- Considers what happens to `scripts/enable-python.sh` if Makefile is no longer merged via script

Propose specific target names and behaviors (e.g., `dbt-run`, `dbt-test`, `dbt-build`, `databricks-deploy`, `databricks-validate`) with rationale. Do not implement — recommend only.

## 4. Pre-commit suitability

Analyze:

@.github/hooks/pre-commit.template
@scripts/append-precommit.py

Evaluate whether the current pre-commit approach fits this repo:

- Is a bash hook template + merge script the right pattern, or should the repo use the `pre-commit` Python framework, or a committed hook at `.git/hooks/` installed via `make install-hooks`?
- Are the current checks appropriate for a data-eng starter (pytest coverage on `src/`, black, pylint, pyright)?
- Should dbt checks be included (e.g., `dbt parse`, `dbt compile`, sqlfluff)? If so, should they be opt-in?
- Identify bugs or inconsistencies (e.g., `git staged-files` is not a standard git command)
- Recommend a pre-commit strategy that matches the simplified Makefile approach

## 5. JavaScript/Node evaluation

Analyze all JavaScript/Node-related artifacts:

@.github/instructions/javascript/
@.github/ci-templates/ci-nodejs.template.yml

And search for any other Node/JS/npm references.

Provide a clear **recommendation: keep, remove, or relocate** with pros/cons for data engineering teams using this template. Consider:
- Does keeping them confuse Copilot or pollute instruction context?
- Are any JS files referenced by active workflows?
- Could they serve a legitimate purpose (e.g., dbt docs site, frontend for metrics)?

## 6. Scripts and CI templates

Review:

@scripts/README.md
@scripts/enable-python.sh
@scripts/append-precommit.py
@scripts/append-makefile.py
@.vscode/merge-configs.py
@.github/ci-templates/ci-python.template.yml
@.github/ci-templates/ci-nodejs.template.yml

Recommend which scripts to keep, simplify, or remove now that the repo is no longer a multi-language/multi-tool template chooser. Consider whether `enable-python.sh` should remain as an onboarding step or whether the starter should ship with Python/dbt/Databricks tooling pre-wired.

## 7. Gap analysis — what to add

Identify missing content teams would expect from a **Copilot data engineering starter** supporting SDD/TDD:

- Example dbt project skeleton or placeholder?
- Databricks bundle scaffold (`databricks.yml`)?
- Sample spec in `docs/specs/`?
- dbt-specific pre-commit or CI steps?
- ADRs or instructions for medallion/lakehouse patterns?
- Gaps in `@docs/AI_SETUP.md` or skill coverage?
- Anything in `@.github/instructions/python/python-fastapi.instructions.md` or `@.github/instructions/python/python-django.instructions.md` that misleads Copilot for data-eng use cases?

Prioritize additions as **P0 (essential)**, **P1 (recommended)**, **P2 (nice-to-have)**.

## 8. Copilot instruction coherence

Verify that Copilot guidance is internally consistent after the pivot:

- Does `@.github/copilot-instructions.md` reflect dbt/Databricks/data-eng focus?
- Are instruction files scoped correctly (path-based activation in VS Code/Copilot)?
- Are there conflicting instructions (backend API patterns vs data pipeline patterns)?
- Should FastAPI/Django/React/Node instructions be removed, archived, or kept dormant?

</analysis_requirements>

<constraints>
- **Analysis only** — do not delete files, edit code, or create commits
- Be thorough: search the full repo, not just the files listed above
- Every removal recommendation must include a list of files to delete AND references to update
- Every "add" recommendation must explain what problem it solves for template adopters
- Recommendations must respect that adopters clone/use this as a **GitHub template** — avoid designs that require running obscure setup scripts unless clearly justified
- Makefile dbt/Databricks targets must be **optional/opt-in** (graceful degradation when tools or config are absent)
- Consider maintainability: fewer moving parts (no template merge scripts) is preferred unless a script clearly earns its keep
</constraints>

<output_format>
Save the audit to: `./analyses/repo-template-audit.md`

Structure the document as:

```markdown
# Copilot Data Engineering Starter — Repository Audit

## Executive Summary
(3–5 bullet points: top findings and recommended direction)

## Repository Purpose Alignment
(Brief assessment: how well current state matches intended purpose)

## Remove
| Item | Path(s) | Reason | References to update |
...

## Keep (no changes)
...

## Keep but Modify
| Item | Path(s) | Recommended change | Priority |
...

## Add (gaps)
| Item | Priority (P0/P1/P2) | Rationale | Suggested location |
...

## Makefile Recommendation
(Current state → proposed single Makefile design, target list, migration from template system)

## Pre-commit Recommendation
(Current state → proposed approach, checks list, opt-in strategy)

## JavaScript/Node Recommendation
(Keep / remove / relocate with reasoning)

## Scripts & CI Recommendation
...

## ADR Strategy
...

## Copilot Instruction Coherence
...

## Implementation Roadmap
(Ordered phases: Phase 1 quick wins, Phase 2 structural changes, Phase 3 enhancements — each with estimated scope and dependencies)

## Open Questions
(Anything requiring maintainer decision that the audit cannot resolve)
```

Use tables where they improve scannability. Be specific with file paths. Include line references or grep evidence where helpful.
</output_format>

<verification>
Before declaring complete, verify:

1. `./analyses/repo-template-audit.md` exists and follows the structure above
2. ADR-001 and ADR-002 are addressed with a complete reference inventory (run ripgrep for `ADR-001`, `ADR-002`, `monolithic`, `async-io`, `FastAPI` across the repo and confirm findings appear in the audit)
3. Makefile, pre-commit, and JavaScript sections contain concrete recommendations (not vague "consider reviewing")
4. The Implementation Roadmap has at least 3 ordered phases with clear dependencies
5. No source files were modified — only the analysis output file was created
</verification>

<success_criteria>
- Comprehensive inventory with keep/remove/modify/add classifications across all major repo areas
- Actionable Makefile consolidation plan with optional dbt/Databricks targets specified by name and behavior
- Pre-commit strategy recommendation suited to Python + dbt + Databricks workflows
- JavaScript/Node keep/remove decision with explicit reasoning
- Gap analysis with P0/P1/P2 prioritized additions
- Implementation roadmap a maintainer can hand to a follow-up prompt without re-auditing
</success_criteria>
