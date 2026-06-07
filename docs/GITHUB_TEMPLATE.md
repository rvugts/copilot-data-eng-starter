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
