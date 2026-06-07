<objective>
Implement **Phase 2** of the repository cleanup defined in `@analyses/repo-template-audit.md`: replace the legacy template/merge toolchain with committed, ready-to-use development tooling for a **Copilot/VS Code data engineering starter** (Python default, optional dbt/Databricks).

Phase 1 (doc cleanup, ADR/JS removal) is complete. This phase delivers what adopters expect on clone: `make install`, `make test`, pre-commit hooks, and CI — without running obscure setup scripts.

Explain WHY each change matters for template adopters who will use this as a GitHub template in VS Code with Copilot.
</objective>

<context>
**Source of truth:** `@analyses/repo-template-audit.md` — Phase 2 section, Makefile Recommendation, Pre-commit Recommendation, Scripts & CI Recommendation.

**Maintainer decisions (locked in):**
- **Python is the default stack** — remove `enable-python.sh` and merge scripts entirely; no opt-in bootstrap
- **Skills:** `.agents/skills/` only — do not create `.github/skills/`
- **dbt/Databricks Makefile targets:** optional/opt-in — skip gracefully with helpful message when `dbt_project.yml` / `databricks.yml` absent
- **Pre-commit:** use `pre-commit` Python framework (`.pre-commit-config.yaml`), not bash hook merge scripts
- **VS Code:** merge Python + dbt + Databricks extensions into base `extensions.json` (and Python settings into base `settings.json` where appropriate)
- **`.gitignore`:** remove Terraform exceptions; **un-ignore `prompts/`** (SDD workflow)
- **Phase 3 is out of scope** — do not create `dbt/README.md`, `databricks/README.md`, or example specs

**Phase 1 already done:** ADRs removed, JS/FastAPI/Django instructions removed, `python-quality.instructions.md` added alongside `python-general.instructions.md`.

**Key files to read:**
@analyses/repo-template-audit.md
@Makefile.python.template
@scripts/enable-python.sh
@scripts/append-makefile.py
@scripts/append-precommit.py
@.github/hooks/pre-commit.template
@.github/ci-templates/ci-python.template.yml
@.vscode/merge-configs.py
@.vscode/extensions.json
@.vscode/extensions.python.json
@.vscode/settings.json
@.vscode/settings.python.json
@requirements.txt
@README.md
@docs/DEVELOPMENT.md
@scripts/README.md
@.gitignore
</context>

<requirements>

## 1. Create committed `Makefile`

Replace `Makefile.python.template` + `append-makefile.py` with a single `./Makefile`.

**Python targets (always available):**

| Target | Behavior |
|--------|----------|
| `help` | Grouped output: Setup, Python, dbt (if detected), Databricks (if detected) |
| `install` | Create `venv/` if missing, activate via recipe hint, `pip install -r requirements.txt`, run `pre-commit install` |
| `install-hooks` | `pre-commit install` only |
| `test` | `pytest --cov=src --cov-fail-under=80 --cov-report=html tests/` |
| `test-watch` | `pytest-watch` if available |
| `lint` | pylint + flake8 on `src/` and `tests/` |
| `format` | black on `src/`, `tests/`, `scripts/` |
| `type-check` | pyright on `src/` |
| `pre-commit` | Run all local checks (or `pre-commit run --all-files`) |
| `clean` | Remove caches, `htmlcov/`, etc. |
| `all` | lint → format → type-check → test |

**Detection variables (top of Makefile):**
```makefile
DBT_PROJECT := $(wildcard dbt_project.yml dbt/dbt_project.yml)
DATABRICKS_BUNDLE := $(wildcard databricks.yml)
```

**dbt targets (opt-in — exit 0 with skip message if no project):**

| Target | CLI |
|--------|-----|
| `dbt-deps` | `dbt deps` |
| `dbt-parse` | `dbt parse` |
| `dbt-compile` | `dbt compile` |
| `dbt-run` | `dbt run` |
| `dbt-test` | `dbt test` |
| `dbt-build` | `dbt build` |

**Databricks targets (opt-in — same skip pattern):**

| Target | CLI |
|--------|-----|
| `databricks-validate` | `databricks bundle validate` |
| `databricks-deploy` | `databricks bundle deploy` |
| `databricks-run` | `databricks bundle run` (document `JOB=` variable in help) |

Use a `require_dbt` / `require_databricks` make macro that prints guidance and exits 0 when config is absent — do not fail.

**`install` target:** Use `python3 -m venv venv` and `./venv/bin/pip` (not assume activated shell). Print reminder to `source venv/bin/activate` after install.

## 2. Create `.pre-commit-config.yaml`

Replace `.github/hooks/pre-commit.template` + `append-precommit.py`.

Minimum hooks:
- `black` — `src/`, `tests/`, `scripts/`
- `flake8`
- `pyright` (or local hook running `pyright src/`)
- `pytest` with `--cov=src --cov-fail-under=80` (local hook)
- Secret detection — prefer `detect-secrets` or documented alternative

Add `pre-commit>=3.0.0` to `requirements.txt`.

Do **not** add dbt/sqlfluff hooks yet (Phase 3 / optional follow-up) unless trivial to include as commented-out examples.

## 3. Delete legacy tooling

Remove these files entirely:
- `Makefile.python.template`
- `scripts/enable-python.sh`
- `scripts/append-makefile.py`
- `scripts/append-precommit.py`
- `.github/hooks/pre-commit.template`

Keep `scripts/README.md` but rewrite as brief pointer to `make install` (no legacy section).

## 4. Promote CI workflow

Copy/adapt `.github/ci-templates/ci-python.template.yml` → `.github/workflows/ci.yml`.

Enhancements:
- Run on push/PR to main
- Use `actions/setup-python@v5` with Python 3.11
- Install from `requirements.txt`, run pytest + black --check + flake8
- Optional **dbt job** with `if: hashFiles('dbt_project.yml', 'dbt/dbt_project.yml') != ''` running `dbt deps && dbt parse` (install dbt in that job only)

Decide whether to keep `.github/ci-templates/ci-python.template.yml` as reference or remove after promotion — prefer remove if redundant.

## 5. Merge VS Code configuration

Merge into base tracked files (adopters should not run merge scripts):

**`.vscode/extensions.json`** — combine current universal extensions with:
- From `extensions.python.json`: Python, Pylance, Black, flake8, pylint, pytest
- Add: `innoverio.vscode-dbt-power-user` (dbt Power User)
- Add: `databricks.databricks` (Databricks)

**`.vscode/settings.json`** — merge relevant Python settings from `settings.python.json` (interpreter path hint, format on save, pytest config, etc.)

Update `.vscode/README.md` to describe the merged setup. Mark `merge-configs.py` as deprecated or remove if no longer needed.

Optional: keep `settings.python.json` / `extensions.python.json` as reference overlays documented in README, or delete if fully merged — prefer merge and delete overlays to reduce confusion.

## 6. Clean `.gitignore`

- Remove Terraform exceptions (lines referencing `settings.terraform.json`, `extensions.terraform.json`, Terraform block)
- Remove `prompts/` from gitignore so `./prompts/` is tracked for SDD workflow
- Keep Node section (harmless)

## 7. Update documentation

Update onboarding to use `make install` everywhere:

| File | Change |
|------|--------|
| `README.md` | Step 2: `make install` then `make test`; remove enable-python references |
| `docs/DEVELOPMENT.md` | Replace manual venv instructions with `make install`; document all Makefile targets |
| `docs/VIBE_CODING_GUIDE.md` | Same |
| `scripts/README.md` | Short doc: "use `make install`" — no legacy scripts |
| `.vscode/README.md` | Extensions pre-merged; no merge script required |

Remove "(coming in Phase 2)" placeholders added during Phase 1.

## 8. Rename project metadata (optional but recommended)

In `pyproject.toml`, rename project from `copilot-dev-starter` to `copilot-data-eng-starter` if not already done.

</requirements>

<constraints>
- **Phase 2 scope only** — no `dbt/README.md`, no example specs, no new ADRs
- Do not recreate deleted instruction files (FastAPI, Django, JS)
- Do not create `.github/skills/`
- Makefile dbt/Databricks targets must **never fail** when tools/config absent — skip with message
- `make install` must work on fresh clone (macOS/Linux; document Windows limitation if venv path differs)
- Match existing tool configs in `pyproject.toml` (black line length 100, pyright strict)
- Do **not** create git commits unless explicitly asked
- Minimize scope — focused diff, no unrelated refactors
</constraints>

<implementation>
Suggested order:

1. Add `pre-commit` to requirements.txt; create `.pre-commit-config.yaml`
2. Create `Makefile` from template + dbt/Databricks sections
3. Create `.github/workflows/ci.yml`
4. Merge VS Code configs
5. Update `.gitignore`
6. Delete legacy files (Makefile template, scripts, pre-commit template)
7. Update docs
8. Verify: `make install && make test && make dbt-parse` (dbt should skip gracefully)

For `make install` on systems without pre-commit in PATH before venv install: install requirements first, then run `./venv/bin/pre-commit install`.
</implementation>

<verification>
Before declaring complete:

1. `./Makefile` exists; `make help` runs without error
2. `make install` creates venv and installs deps (run in sandbox or verify recipe syntax)
3. `make test` passes with existing `tests/test_example.py`
4. `make dbt-parse` prints skip message (no dbt project in repo)
5. `make databricks-validate` prints skip message (no databricks.yml)
6. Legacy files deleted: `enable-python.sh`, `append-*.py`, `Makefile.python.template`, `pre-commit.template`
7. `.github/workflows/ci.yml` exists
8. `.pre-commit-config.yaml` exists
9. `rg "enable-python|append-makefile|append-precommit|Makefile.python.template" --glob '!analyses/*' --glob '!prompts/completed/*'` returns no active references (scripts/README and audit historical mentions OK if updated)
10. `prompts/` is not in `.gitignore`
</verification>

<success_criteria>
- Single committed Makefile with Python + opt-in dbt/Databricks targets
- pre-commit framework replaces bash hook merge pattern
- Legacy setup scripts removed
- CI workflow committed and runnable
- VS Code extensions include Python, dbt, and Databricks recommendations out of the box
- README and DEVELOPMENT guide onboarding is `make install` → `make test`
- All verification checks pass
</success_criteria>
