---
name: create-tasks
description: >-
  Break down a specification into atomic, executable tasks optimized for
  AI-driven development workflows (SDD/TDD). Use when the user wants to create
  tasks from a spec, plan implementation steps, decompose a feature into work
  items, or mentions task breakdown, implementation plan, or work decomposition.
---

# Create Tasks

## Role

Act as a **senior software architect and delivery lead**. Your job is to transform a specification into a set of **atomic, executable tasks** that:

- Make **Spec-Driven Development (SDD)** and **Test-Driven Development (TDD)** non-negotiable and explicit.
- Are small enough for a Copilot agent to execute reliably in 1–3 prompts.
- Have clear **inputs, outputs, acceptance criteria**, and **file ownership**.
- Respect dependencies and logical sequencing.
- Are **organized for safe parallel execution** whenever possible (different agents, different files, no collisions).

Think in execution order, dependency graphs, file contention, risk isolation, and incremental delivery.

## Process

### Phase 1 — Locate the spec

Look for the active specification at `docs/specs/spec.md`. Attach it with `@docs/specs/spec.md` in Copilot Chat so the full spec is available to the model.

If it does not exist, ask:

> "No active spec found at `docs/specs/spec.md`. Please attach a spec with `@<path>` or describe what needs to be broken down into tasks."

If the user points to a different file (e.g. an archived spec in `docs/specs/`), use that instead.

Also ask (if not already stated):

> "Is there a target delivery window (e.g. 2 hours, 1 day)? And roughly how many agents can run in parallel? I will size waves accordingly."

If the user declines to specify, default to: **no fixed deadline, up to 4 parallel agents**.

### Phase 2 — Analyze

Read the spec and extract:

| Dimension | What to look for |
|-----------|-----------------|
| **Components** | Major modules, services, layers |
| **Functional areas** | Distinct capabilities / endpoints / commands |
| **Data model** | Entities, schemas, migrations |
| **Data flows** | How data moves through the system |
| **Interfaces** | APIs, CLI commands, UI screens, library exports |
| **Critical dependencies** | What must exist before other work can start |
| **Risk areas** | Complex logic, security-sensitive code, third-party integrations |
| **Infrastructure** | Setup, config, CI/CD, deployment (if in spec) |
| **Invariants** | Architectural rules the spec declares non-negotiable |
| **Test cases** | TC-IDs, scenarios, acceptance matrices |

### Phase 2b — Plan for parallel execution (MANDATORY)

Before decomposing, plan the concurrency model:

1. **List file/path ownership up front.** For each anticipated task, name the exact files it will create or modify. Two tasks that **write** the same file CANNOT run in parallel — split them.
2. **Split conflicting tasks.** If two pieces of work naturally target the same file, put them in **different files** so they can run in parallel (e.g. `github_client.py` vs. `mock_github_client.py`).
3. **Serialize on purpose.** If a file is genuinely a single concern (e.g. a router file), keep its tasks in a **single agent track** and mark them sequential.
4. **Minimise dependencies.** Question each dependency — would reading the spec alone be enough? Frontend and infra tasks often only need the spec contract, not the backend implementation.
5. **Size waves to the agent budget.** Group tasks into waves of ≤ N parallel agents (N from Phase 1). Each wave unblocks the next.

### Phase 3 — Decompose

Break the work into tasks using these principles:

**Atomicity**
- Each task has a single responsibility.
- Completable in 1–3 focused prompts.
- No multi-concern logic (e.g. "build the entire API" is not a task).

**Dependency awareness**
- Identify prerequisite tasks explicitly.
- Order tasks so each can be started when its dependencies are done.
- No circular dependencies.

**Testability (TDD)**
- For every functional task, there is a paired **RED test task** that runs first, followed by a **GREEN implementation task**. Refactor is implicit in the GREEN task's acceptance criteria (linter + type-checker clean).
- For architectural invariants, create a dedicated **fitness test task**.

**File ownership & parallelism**
- Each file has **one exclusive writer** at a time.
- Tasks that share an owned file belong to the same agent's **serialized track**.
- Where possible, split tasks so they own disjoint files and can run in parallel.

**AI suitability**
- Tasks are unambiguous — no "figure out the best approach".
- Each task can be executed with limited context (the spec section + prior outputs + owned files).

### Phase 4 — Confirm

Present a summary before generating. The summary MUST include:

> "I've analyzed the spec and identified **[N] tasks** across **[categories]**.
>
> **Critical path:** [brief chain, e.g. T1 → T2 → T7 → T13].
>
> **Parallel plan:** [W] waves sized for [N_agents] agents in parallel, target duration [if given].
>
> **Non-negotiables embedded:** SDD (spec is single source of truth, every commit cites spec section), TDD (RED → GREEN → REFACTOR, no skip/xfail, coverage floor).
>
> Ready to generate the task list?"

Options:
- **Proceed** — generate the task file.
- **Adjust** — user wants to add/remove/reorder tasks or change waves.
- **Ask questions** — clarify ambiguities in the spec first.

Do NOT generate the file until the user confirms.

### Phase 5 — Generate

State:

> "Generating [N] tasks in [W] waves for: [spec name]"

Then write the task file using the template in **Task File Structure** below.

**Do not generate implementation code.** Produce only the task breakdown as markdown. No application source, tests, or configs.

### Phase 6 — Optional prompt-pack generation

After `docs/specs/tasks.md` is generated, ask:

> "Generate execution prompt files now under `./prompts/`? (yes/no)"

If user says **yes**, generate one prompt file per task using the structure in **Prompt Pack Structure** below.

If user says **no**, stop after `tasks.md`.

## Output

Generate ONE file: `docs/specs/tasks.md`

This places the task breakdown next to the spec it decomposes (`docs/specs/spec.md`), keeping planning artifacts together.

### Archive Workflow

If `docs/specs/tasks.md` already exists:

1. Read the existing file.
2. Rename it to `docs/specs/tasks-{spec-name}.md` where `{spec-name}` is the `name` from the active spec's YAML frontmatter (if discoverable from the file content or the current `docs/specs/spec.md`).
3. If that archive name already exists, append a numeric suffix: `-2`, `-3`, etc.
4. If no spec name can be determined, use `docs/specs/tasks-archived-{YYYY-MM-DD}.md`.
5. Generate the new `docs/specs/tasks.md`.

If Phase 6 is approved, additionally generate prompt files under:

- `prompts/01-<task-id>-<short-name>.md`
- `prompts/02-<task-id>-<short-name>.md`
- ...

Use zero-padded numbering in **Section 2 execution order** from `tasks.md`. Include wave/parallel info inside each prompt body. If prompt files already exist for the same task IDs, overwrite them.

## Task File Structure

The generated file MUST include **all** sections below, in this order. Sections marked **MANDATORY** may not be omitted even for simple specs — tailor depth, not presence.

```markdown
# Implementation Tasks

**Spec:** docs/specs/spec.md
**Generated:** YYYY-MM-DD
**Total tasks:** [N]
**Target delivery:** [e.g. "2 hours wall-clock using parallel agents" — or "open-ended"]

---

## 0. Non-negotiable operating principles [MANDATORY]

These rules apply to every task. Agents MUST restate the relevant rule when it governs a change.

### 0.1 Spec-Driven Development (SDD) — non-negotiable

1. `docs/specs/spec.md` is the single source of truth. No behavior, schema, error code, version, or constraint is valid unless it can be cited to a section of that spec.
2. Never invent scope. Out-of-scope items and open questions MUST NOT be implemented. Stop and ask if reality diverges from the spec.
3. Trace everything. Each task has a Spec reference; each commit MUST cite at least one spec section (e.g. `refs spec §4.3, FR-6`). Tests MUST map to TC-IDs or to the functional/invariant ID they exercise.
4. Amend before drift. If a gap is discovered, stop, note it in the PR as a spec-change request, and continue only after the spec is updated.

### 0.2 Test-Driven Development (TDD) — non-negotiable

All functional / core-logic tasks MUST follow RED → GREEN → REFACTOR:

1. RED — write the failing test first (the test runner shows it fail for the right reason, not an import error).
2. GREEN — write the minimum implementation needed to pass the failing test.
3. REFACTOR — clean up while keeping tests green; linter and type-checker must remain clean.

Non-negotiable TDD rules:

- No production code without a failing test first.
- Fitness / architecture tests count as tests; invariants MUST have assertions.
- Don't silence tests (no `skip`/`xfail`/broad try/except in tests/commented-out assertions to make CI green).
- Coverage floor [X%] (enforced in CI). Coverage is a floor, not a ceiling.
- Determinism: no real network in tests; no time-of-day assertions; fixtures are stable.

Each task below declares a TDD step (RED / GREEN / REFACTOR / N/A).

### 0.3 Architectural invariants [if the spec declares any]

| ID | Rule | Owned by |
|----|------|----------|
| INV-xxx | ... | Task N, verified by Task M |

---

## 1. Parallel execution plan [MANDATORY]

### 1.1 Wave overview

| Wave | Duration | Agents in parallel | Tasks |
|------|----------|--------------------|-------|
| **Wave 0 — Foundation** | ~X min | 1 | T1 |
| **Wave 1 — …** | ~X min | up to N | T2, T3, ... |

### 1.2 File-ownership matrix (prevents parallel collisions) [MANDATORY]

Each path MUST be written by at most one agent at a time. Read-only access is unrestricted.

| Path | Exclusive owner tasks (in order) |
|------|----------------------------------|
| `path/to/file.py` | T2 |
| `path/to/shared_file.py` | T7 → T9 → T10 (same agent track) |

### 1.3 Dependency graph (summary)

ASCII or Mermaid diagram showing task dependencies at a glance.

---

## 2. Execution order (single-agent fallback)

1. T1: [Title]
2. T2: [Title]
...

---

## 3. Tasks

### Task N: [Title]

**Category:** [Setup | Data Model | Core Logic | Validation | API/Interface | Integration | Testing | Infrastructure | Documentation | Refactoring]
**Wave:** [0..W] · **Est.:** [minutes] · **TDD step:** [RED | GREEN | REFACTOR | RED then GREEN | N/A]

**Description:**
What needs to be done.

**Spec reference:**
Which section(s) of the spec this task implements (e.g. "§3.1 FR-1, §4.1 Scenario 1, INV-003").

**Inputs:**
- Prior task outputs or files this task reads.
- Spec sections to attach (e.g. `@docs/specs/spec.md §4`).

**Owns files:**
- Exact paths this task will create or modify. No other task in the same wave may write these.

**Reads files:**
- Paths this task reads but does not modify.

**Parallelizable with:**
- List of task IDs that can run at the same time (different owners, no dependency).

**Blocks:**
- List of task IDs that cannot start until this one is complete.

**Acceptance criteria:**
- [ ] Specific, testable condition 1 (cite TC-ID or spec requirement).
- [ ] Specific, testable condition 2.

**Dependencies:**
- None | Task N, Task M

**Prompt hint:**
One-line suggestion for what to ask the Copilot agent (or pass to `/create-prompt`). Include specific file references (e.g. `@docs/specs/spec.md`, `@src/…`) so the executing agent loads exact context.

---

## 4. Spec coverage cross-check [MANDATORY]

| Spec item | Covered by tasks |
|-----------|------------------|
| FR-1 … | T2, T13, T14 |
| ... | ... |
| INV-001 … | T7, T15 |
| TC-U-01 … | T6 |

Every FR, NFR, invariant, and TC in the spec MUST appear in at least one task. Orphaned items indicate incomplete coverage — revise before committing.
```

## Prompt Pack Structure (Phase 6)

When generating `./prompts/` files, each prompt MUST include these sections in order:

```markdown
# Wave [N] - Task [ID] ([TDD step] / [Category])

You are executing **Task [ID]** from `docs/specs/tasks.md`.

## Mission
[1-2 sentence objective aligned to task Description]

## Required context
Attach:
- `@docs/specs/spec.md`
- `@docs/specs/tasks.md`
- [task-specific paths from Owns files + Reads files]

## Scope (must do)
- [concrete checklist from Description + Acceptance criteria]

## Constraints
- Only edit the files listed in Owns files.
- [TDD mode: RED — write failing tests only, no production code | GREEN — implement minimum to pass | REFACTOR — clean up with tests green | N/A]
- No out-of-scope changes.

## Deliverable
- [exact files/outcomes expected]

## Definition of done
- [acceptance outcomes mapped from task Acceptance criteria]
- [verification commands relevant to the task]
```

### Prompt generation fidelity rules

1. Use task metadata directly from `tasks.md` (Category, Wave, Est., TDD step, Owns files, Reads files, Dependencies, Acceptance criteria).
2. Do not invent scope, files, or dependencies.
3. Preserve FR/NFR/INV/TC references where present.
4. For RED tasks: explicitly instruct "write failing tests first; do not write production code."
5. For GREEN tasks: explicitly instruct "implement minimum code to make failing tests pass."
6. For REFACTOR tasks: explicitly instruct "refactor only with tests green."
7. Include wave and parallel hints in prompt headers.

### Prompt generation strict mode (MANDATORY)

Before generating any prompt files, validate every task in Section 3 has:

- `Owns files`
- `Acceptance criteria`
- `TDD step`
- `Spec reference`

If any are missing or empty:

1. STOP prompt generation.
2. Report which Task IDs are incomplete and which required fields are missing.
3. Ask the user to fix `docs/specs/tasks.md` first.
4. Resume prompt generation only after validation passes.

### Prompt-pack completion report

After prompt generation, output:

- Total prompt files created
- Mapping table: Task ID → prompt filename
- Suggested execution plan by wave (parallel batches for `/fleet` or multiple VS Code agent sessions)

## Task Categories

| Category | Typical contents |
|----------|-----------------|
| **Setup** | Project scaffolding, dependency install, config files, CI/CD pipeline |
| **Data Model** | Entity definitions, schemas, migrations, seed data |
| **Core Logic** | Business rules, processing, algorithms |
| **Validation** | Input validation, business rule enforcement, constraints |
| **API / Interface** | Endpoints, CLI commands, library exports, UI components |
| **Integration** | External services, message queues, third-party APIs |
| **Testing** | Test suites, fixtures, test data, coverage verification, fitness tests |
| **Infrastructure** | Deployment, environment config, monitoring, secrets |
| **Documentation** | API docs, README updates, docstrings, architecture diagrams |
| **Refactoring** | Code cleanup after initial implementation |

## Sequencing Rules

1. **Setup first** — project scaffolding and config before any code.
2. **Data model before logic** — entities and schemas before business rules.
3. **Tests before implementation (TDD)** — every functional task is preceded by a RED test task, or carries its own explicit RED → GREEN split.
4. **Core before edge** — happy path first, then validation and error handling.
5. **Interface after logic** — API/CLI/UI tasks depend on the logic they expose, unless the interface is purely contract-driven (e.g. a frontend that only needs the spec's API schema — those can run earlier in parallel).
6. **Integration late** — external service integrations after core logic is stable.
7. **Documentation and refactoring last** — final polish after functionality is complete.
8. **Infrastructure as needed** — CI/CD and deployment tasks can be early (if blocking) or late (if non-blocking).
9. **File-ownership rule** — no two tasks in the same wave write the same file. If they must, split files or serialize the tasks.
10. **Minimise dependencies** — only add a dependency when the task genuinely cannot start without it. Question every "needs T-X" — maybe it only needs the spec.

## Complexity Scaling

| Spec complexity | Typical task count | Granularity |
|----------------|-------------------|-------------|
| **Simple** (3–5 requirements) | 5–10 tasks | One task per requirement + setup + tests. §0 may be brief but must be present. |
| **Moderate** (5–15 requirements) | 10–25 tasks | Requirements split into model/logic/interface + dedicated test tasks. Full §0 and §1. |
| **Complex** (15+ requirements) | 25–50 tasks | Fine-grained: separate tasks for schemas, migrations, individual endpoints, error handling, security, performance. Deep wave structure. |

## Intelligence Rules

1. **Smaller is better** — prefer more small tasks over fewer large ones; a task that needs "just one more thing" is two tasks.
2. **Respect dependencies** — incorrect ordering breaks the entire plan; when in doubt, add an explicit dependency.
3. **Design for failure isolation** — risky tasks (third-party integrations, complex algorithms) should be isolated so a failure doesn't block unrelated work.
4. **Optimize for AI execution** — each task should be completable by an agent given only the spec section, this task description, the task's owned files, and the outputs of dependency tasks.
5. **Avoid ambiguity** — every task must have concrete outputs and testable acceptance criteria; "improve performance" is not a task, "add database index on users.email and verify query time < 50ms" is.
6. **Map back to spec** — every spec requirement must appear in at least one task's spec reference; orphaned requirements mean incomplete coverage (see §4 cross-check).
7. **TDD by default** — for each functional task, either include a RED → GREEN split directly or create a paired RED test task that precedes the implementation task.
8. **Plan for parallelism** — the default plan is **parallel-first**; serialize only when file ownership or a genuine dependency forces it.
9. **Split conflicting tasks into disjoint files** — rename modules if needed (e.g. `client.py` → `mock_client.py` + `http_client.py`) to unlock parallelism.

## Anti-Patterns

Do NOT create tasks that:

- Span multiple unrelated concerns (e.g. "build and deploy the entire API").
- Have no concrete outputs or acceptance criteria.
- Require understanding the full system to complete.
- Cannot be tested independently.
- Duplicate work already covered by another task.
- Are vague directives ("make it production-ready", "handle all edge cases").
- Write the same file as another task in the same wave (file-ownership violation).
- Carry a false dependency that was copy-pasted rather than justified.

## Execution Checklist

Before delivering the task file, verify:

- [ ] No implementation code generated — only the task breakdown.
- [ ] §0 Non-negotiable SDD + TDD preamble is present and concrete (not hand-wavy).
- [ ] §1 Parallel execution plan is present with wave table, **file-ownership matrix**, and dependency graph.
- [ ] §4 Spec coverage cross-check maps every FR / NFR / invariant / TC-ID to at least one task.
- [ ] Every task has: category, wave, est., TDD step, description, spec reference, inputs, **owns files**, reads files, **parallelizable with**, **blocks**, acceptance criteria, dependencies, prompt hint.
- [ ] No two tasks in the same wave write the same owned file.
- [ ] No circular dependencies.
- [ ] Single-agent execution order (§2) is consistent with the parallel plan (§1).
- [ ] Test tasks exist (RED) before implementation tasks (GREEN) for all functional work.
- [ ] Setup tasks come first; documentation and refactoring come last.
- [ ] Prompt hints include specific file references so the executing agent loads exact context.
- [ ] Task count is proportional to spec complexity.
- [ ] Estimated durations sum, per wave, to fit the user's stated budget (if any), plus buffer.
- [ ] If user approved Phase 6, prompt files were generated under `./prompts/` using the required structure.
- [ ] Phase 6 strict mode validation passed before prompt files were written.

## Workflow Integration

This skill plugs into the full SDD workflow:

| Step | Skill / command |
|------|----------------|
| Draft the spec | `/create-spec` — writes `docs/specs/spec.md` |
| Decompose into tasks | `/create-tasks` — this skill; writes `docs/specs/tasks.md` |
| Author prompts per task | Phase 6 of this skill (auto-generate) or `/create-prompt` manually using each task's **Prompt hint** |
| Execute tasks | `/run-prompt` sequentially, or dispatch wave batches in parallel using `/fleet` (Copilot CLI) or multiple VS Code agent sessions |

Tips for best results:

- **Attach context with `@`.** Write prompt hints with concrete `@path` references (e.g. `@docs/specs/spec.md`, `@src/models.py`) so the executing agent loads exactly what it needs.
- **Use the wave plan for parallel dispatch.** Each wave in §1 is a ready-made batch for `/fleet` or for opening parallel VS Code agent sessions. Tasks within a wave have no file conflicts.
- **Keep artifacts co-located.** Both `spec.md` and `tasks.md` live under `docs/specs/` so they can be attached together via `@docs/specs/`.
- **After generation, recommend `/create-prompt`** for any task whose Prompt hint needs expansion into a full structured prompt.
