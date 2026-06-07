# Contributing

Thank you for helping improve this **Copilot Data Engineering** starter template.
This repo provides a reusable foundation for Copilot-powered workflows with **dbt**, **Databricks**, **Python**, SDD, and TDD.

**Before contributing, read `docs/VIBE_CODING_GUIDE.md` and `docs/DEVELOPMENT.md`.**

## Ways to contribute

- Improve instructions in `.github/instructions/` (dbt, Databricks, Python)
- Add or update skills in `.agents/skills/` ([Agent Skills](https://agentskills.io) standard)
- Extend docs under `docs/` (specs, ADRs, troubleshooting)
- Improve Makefile targets, CI, or pre-commit hooks for data-eng workflows

## Data-eng PR checklist

When contributing dbt or pipeline changes to this template:

- [ ] SQL uses `{{ ref() }}` / `{{ source() }}` in examples
- [ ] Example specs live in `docs/specs/` (not as active `spec.md` unless intentional)
- [ ] No secrets in committed files — use `.env.example` for variable names only
- [ ] `make test` passes; run `make pre-commit` before opening PR

## Contributions process

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-change`
3. Make your changes.
4. Add tests or examples where appropriate.
5. Update documentation if needed.
6. Open a pull request.

## PR expectations

- Follow conventional commit messages
- Include a clear description of what changed and why
- Link to related docs or ADRs if the change affects project structure
- Ensure documentation remains accurate for Copilot users

## Documentation updates

When adding or modifying templates, update `README.md`, `docs/DEVELOPMENT.md`, or other relevant docs so new users can discover the change.

## Code of conduct

By contributing, you agree to follow the repository's standards for respectful collaboration.
See `CODE_OF_CONDUCT.md` for the full code of conduct.
