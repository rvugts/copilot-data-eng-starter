# GitHub template repository setup

Guidance for maintainers of this template on GitHub.com.

## Enable template repository

1. **Settings → General → Template repository** — check **Template repository**
2. Confirm **Use this template** appears on the repo home page

## Recommended topics

Add these topics under **Settings → General → Topics** (or via CLI):

```bash
gh repo edit --add-topic dbt --add-topic databricks --add-topic data-engineering \
  --add-topic github-copilot --add-topic python --add-topic pyspark \
  --add-topic analytics-engineering --add-topic template
```

| Topic | Why |
|-------|-----|
| `dbt` | Primary transformation layer |
| `databricks` | Lakehouse platform |
| `data-engineering` | Audience |
| `github-copilot` | AI-assisted workflow |
| `python` | Utility/orchestration code |
| `pyspark` | Spark transforms |
| `analytics-engineering` | dbt-centric analytics |
| `template` | Discoverability as a starter |

## Social preview image

A ready-made banner lives at **`docs/assets/social-preview.png`** (1280×640, under 1 MB).

GitHub does **not** expose a public REST API for uploading social preview images — use the web UI:

1. Open repo **Settings → General → Social preview → Edit → Upload an image…**
2. Select `docs/assets/social-preview.png` from your local clone

Shortcuts from the repo root:

```bash
# Open the image in Preview (macOS)
open docs/assets/social-preview.png

# Open repo settings in the browser
gh browse --settings
```

Or open directly: `https://github.com/rvugts/copilot-data-eng-starter/settings`

The banner includes the repo name, stack badges (dbt · Databricks · Python · Copilot), and tagline *SDD + TDD starter for data teams*.

## Template description

The file `.github/TEMPLATE.md` is shown when someone clicks **Use this template**. Keep it focused on first steps after repo creation.

## Demo and presentation repos

Do **not** add a runnable dbt project, sample warehouse config, or other stack-specific scaffolding to this template repo. Adopters need a blank slate they can `dbt init` into.

For live demos (conferences, internal workshops, Copilot walkthroughs), use a **separate demo repository**:

1. Click **Use this template** to create e.g. `copilot-data-eng-demo`
2. Add a minimal dbt project, `profiles.yml.example`, and any MCP/CI wiring for your Databricks (or other) stack
3. Implement the example spec so Copilot, MCP, and CI have real models to reference during the talk
4. Periodically pull starter improvements (docs, skills, instructions) into the demo repo

The starter remains the reusable product; the demo repo is the opinionated, runnable instance for a specific audience and presentation.
