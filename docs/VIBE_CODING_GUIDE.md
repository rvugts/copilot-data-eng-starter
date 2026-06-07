# Vibe Coding Guide & Copilot Guardrails

## Overview

Welcome to the **Vibe Coding** approach! This guide outlines our development philosophy, best practices, and Copilot usage guidelines for the copilot-data-eng-starter repository. Vibe coding emphasizes intuitive, high-quality development that feels natural while maintaining rigorous standards.

## Core Philosophy

### What is Vibe Coding?

Vibe coding combines:
- **Intuitive Development**: Code that "feels right" and flows naturally
- **Rigorous Standards**: TDD, SDD, security-first, performance-conscious
- **Copilot Harmony**: Leveraging AI assistance while maintaining human oversight
- **Quality First**: Clean, maintainable, accessible code

### Why Vibe Coding?

Traditional coding can feel mechanical. Vibe coding makes development enjoyable and productive by:
- Following established patterns that work
- Using tools (like Copilot) to accelerate routine tasks
- Maintaining high standards without burnout
- Creating code that's both functional and beautiful

## Development Workflow

### 1. Specification-Driven Development (SDD)

**Always start with the spec!**

```markdown
# Before writing ANY code:
1. Read docs/specs/spec.md (if exists)
2. Understand requirements thoroughly
3. Ask clarifying questions if needed
4. Plan implementation aligned with spec
```

**Copilot Guardrail**: Never implement features beyond the specification. If spec contradicts approach, follow spec strictly.

### 2. Test-Driven Development (TDD)

**Mandatory workflow: Red → Green → Refactor**

```bash
# For new features:
1. Write failing test first (Red)
2. Implement minimal code to pass (Green)
3. Refactor for better structure (Refactor)
4. Repeat until feature complete
```

**Copilot Integration**:
- Ask Copilot to generate tests first
- Use Copilot to implement minimal solutions
- Have Copilot suggest refactorings

### 3. Code Quality Standards

#### Clean Code Principles
- **Meaningful Names**: Variables, functions, classes should be self-documenting
- **Single Responsibility**: Each function/method does one thing well
- **DRY (Don't Repeat Yourself)**: Eliminate code duplication
- **Consistent Style**: Follow project conventions

#### Performance Considerations
- Write efficient algorithms (consider Big O)
- Optimize hot paths, not prematurely
- Use caching where beneficial
- Profile before optimizing

#### Security First
- Validate all inputs
- Prevent common vulnerabilities (SQL injection, XSS, CSRF)
- Use parameterized queries
- Never hardcode secrets
- Implement proper auth/authz

#### Accessibility
- Semantic HTML for web interfaces
- ARIA labels where needed
- Keyboard navigation support
- Sufficient color contrast
- Alt text for images
- WCAG 2.1 AA compliance

## Copilot Usage Guidelines

This repository includes specialized Copilot skills for common development tasks. These skills are automatically invoked when relevant, or you can invoke them explicitly. See the **"Available Copilot Skills"** section below for detailed information.

### When to Use Copilot

✅ **Great for:**
- Writing tests (especially TDD)
- Implementing known patterns
- Code refactoring suggestions
- Documentation generation
- Routine tasks (boilerplate, getters/setters)
- Exploring APIs or libraries
- Debugging assistance

### When NOT to Use Copilot

❌ **Avoid for:**
- Security-critical code (review carefully)
- Complex business logic (understand first)
- When spec is unclear (clarify requirements)
- Performance-critical sections (human optimization)
- Code you don't understand (learn the concepts)

### Copilot Best Practices

#### 1. Context is King
```bash
# Good: Provide full context
"Create a Python function to validate email addresses following TDD.
Reference python-general.instructions.md and ensure alignment with docs/specs/spec.md section 2.1."

# Bad: Vague requests
"Write an email validator"
```

#### 2. Iterative Refinement
```bash
# Don't expect perfect code on first try
1. Ask for initial implementation
2. Review and provide feedback
3. Ask for refinements
4. Test thoroughly
```

#### 3. Security Review
```bash
# Always review Copilot-generated code for:
- Input validation
- SQL injection prevention
- XSS protection
- Proper error handling
- Secrets management
```

#### 4. Learning Opportunity
```bash
# Use Copilot to learn:
- New language features
- Design patterns
- Best practices
- Alternative approaches
```

### Copilot Prompts That Work

#### For TDD
```
"Write a failing test first for the user authentication feature (Red phase).
Then implement the minimal code to pass the test (Green phase).
Finally, refactor for better structure (Refactor phase)."
```

#### For SDD
```
"@docs/specs/spec.md requires staging models for the orders source with not_null
and unique tests on order_id. Create the dbt model and schema.yml following
dbt-sql.instructions.md."
```

#### For Refactoring
```
"Refactor this Python code applying sound engineering practices, DRY, and security without altering functionality."
```

## AI Setup

Before diving in, set up the MCP servers and keep your skills current:

- **[docs/AI_SETUP.md](AI_SETUP.md)** — step-by-step guide for configuring the Databricks Managed MCP Server and the dbt MCP Server, plus how to update skills from the official dbt Labs and Databricks packages.
- **Recommended watch:** [AI-Powered Data Engineering with dbt and MCP](https://www.youtube.com/watch?v=34RkoSPfpV4) — demonstrates the dbt skills and MCP server in action.

## Available Copilot Skills

This repository includes specialized Copilot skills to enhance your workflow. Skills are automatically invoked when relevant, or you can invoke them explicitly.

### dbt Skills

#### using-dbt-for-analytics-engineering
**Purpose:** Build and modify dbt models, write SQL using `ref()` and `source()`, explore data sources, write tests, and validate results.

**Best for:**
- Building new staging, intermediate, or mart models
- Debugging compilation or runtime errors
- Refactoring model structure (CTEs, naming, layer conventions)
- Writing schema.yml tests alongside new models

**How to invoke:**
```
Use the using-dbt-for-analytics-engineering skill to build a staging model for the raw.orders source.
```

**Key behaviours:**
- Always runs `dbt show` to preview source data before writing SQL
- Follows DAG layer conventions (stg_, int_, fct_, dim_)
- Writes schema.yml tests alongside every new model
- Asks "why a new model?" before adding one

#### adding-dbt-unit-test
**Purpose:** Write dbt unit tests (TDD) for model SQL logic — mock upstream inputs and assert expected outputs.

**Best for:**
- TDD workflow: write the test before implementing the SQL
- Testing business logic (discount calculations, status transitions)
- Testing edge cases: NULL handling, boundary conditions

**How to invoke:**
```
Use the adding-dbt-unit-test skill to add a test for the cancelled-orders-excluded logic.
```

**Output:** Writes a `unit_tests:` block in the model's `schema.yml` file.

---

### Databricks Skill

#### databricks
**Purpose:** Databricks CLI operations, Unity Catalog exploration, Lakeflow Jobs/Pipelines, and Asset Bundle deployment.

**Best for:**
- Authenticating and selecting workspace profiles
- Exploring Unity Catalog schemas and tables
- Creating and deploying jobs via Asset Bundles (DABs)
- Scaffolding new Databricks projects

**How to invoke:**
```
Use the databricks skill to scaffold a new Asset Bundle project with a daily PySpark job.
```

---

### 1. create-spec
**Purpose:** Produce a specification aligned with `docs/spec.template.md` using specification-driven development

**Best for:**
- New features or systems before implementation
- Capturing requirements, behavior, and acceptance criteria in one contract

**How to invoke:**
```
Use the create-spec skill to draft a spec for [feature].
```

**Output:** Writes `docs/specs/spec.md` and archives any prior active spec using its frontmatter `name` field.

### 2. create-tasks
**Purpose:** Decompose a spec into atomic, ordered tasks for AI-driven implementation

**Best for:**
- Planning implementation after a spec is written
- Creating work items an AI agent can execute one at a time
- Establishing correct execution order with explicit dependencies

**How to invoke:**
```
Use the create-tasks skill to break down docs/specs/spec.md into tasks.
```

**Output:** Writes `docs/specs/tasks.md` with task list, execution order, and prompt hints for each task.

### 3. audit-security
**Purpose**: Comprehensive security audit of your codebase

**Best for:**
- Identifying security vulnerabilities
- OWASP Top 10 2025 compliance checking
- Authentication and session security review
- Dependency vulnerability scanning
- Input validation and sanitization verification

**How to invoke:**
```
Perform a security audit on this codebase to identify vulnerabilities and compliance issues.
```

**Output**: Generates a detailed `SECURITY_AUDIT_REPORT.md` with findings and remediation strategies

**Key checks:**
- Authentication mechanisms
- Input validation and sanitization
- SQL injection prevention
- XSS and CSRF protection
- Secrets management
- Dependency supply chain security

### 4. refactor-python
**Purpose**: Refactor Python code applying engineering best practices

**Best for:**
- Improving code readability and maintainability
- Applying DRY principle
- Adding type hints and documentation
- Optimizing code structure
- Ensuring security best practices

**How to invoke:**
```
Use the refactor-python skill to improve this code while maintaining functionality.
```

**Optimizations performed:**
- Code structure optimization (line/function length)
- Import organization and cleanup
- Type hint addition
- Docstring generation
- DRY principle enforcement
- Security improvements
- Performance optimizations

### 5. generate-prompt
**Purpose**: Generate structured prompts for complex tasks

**Best for:**
- Creating reusable prompts for agents to execute
- Breaking down complex tasks into prompt workflows
- Designing multi-step assistant interactions
- Generating XML-structured prompts

**How to invoke:**
```
Use the generate-prompt skill to create a multi-step prompt for analyzing our database schema.
```

**Features:**
- Adaptive requirements gathering
- XML-structured output
- Support for sequential multi-prompt workflows
- Automatic prompt numbering and saving to `./prompts/`

Saved prompt files are local workflow artifacts. The `prompts/` folder is present
for convenience, but prompt files are ignored by git and are not part of the
starter template.

### 6. run-prompt
**Purpose**: Execute saved prompts as isolated sub-tasks

**Best for:**
- Running previously created prompts from `./prompts/` directory
- Parallel or sequential execution of complex workflows
- Delegating work to fresh agent contexts
- Automating multi-step development tasks

**How to invoke:**
```
Use the run-prompt skill to execute prompts/001-analyze-schema and prompts/002-generate-models sequentially.
```

**Features:**
- Single or sequential execution
- Automatic prompt resolution
- Fresh context for each execution
- Git integration (staging/committing results)
- Consolidated reporting

### Using Skills Together

You can combine skills for powerful workflows:

```bash
# Example 1: Audit → Refactor → Test
1. Use audit-security to identify issues
2. Use refactor-python to fix code quality problems
3. Write tests to verify fixes

# Example 2: Create → Run → Review
1. Use generate-prompt to design a multi-step workflow
2. Use run-prompt to execute the workflow
3. Review and iterate
```

### Skill Best Practices

- **Be specific**: Name the exact skills you want to use when it matters
- **Chain skills**: Let skills work together for complex tasks
- **Review outputs**: Always review skill-generated reports and code
- **Iterate**: Use skill outputs to refine and improve further
- **Document results**: Save important audit reports and refactoring decisions

## Language-Specific Guidelines

### Python Development

#### Setup
```bash
make install
source venv/bin/activate
make help
```

#### Standards
- **Type Hints**: Use for all public APIs
- **Docstrings**: Google/NumPy format
- **Testing**: pytest with >80% coverage
- **Linting**: black, flake8, pylint, pyright
- **Imports**: Absolute imports preferred

#### Copilot Python Tips
- Specify Python version (3.11+)
- Reference pyproject.toml settings
- Ask for type-annotated code
- Request comprehensive tests

### dbt Development

#### Setup
Install dbt and the appropriate adapter for your platform:
```bash
pip install dbt-databricks   # for Databricks
# or
pip install dbt-spark        # for Spark
```

#### Standards
- **Model Structure**: `models/staging/`, `models/intermediate/`, `models/marts/`
- **Naming**: `stg_<source>__<entity>.sql` for staging, `fct_`/`dim_`/`rpt_` for marts
- **Testing**: Add schema tests (`not_null`, `unique`, `accepted_values`) in `schema.yml`
- **Documentation**: Describe all models and columns in `schema.yml`

#### Copilot dbt Tips
- Reference `.github/instructions/dbt/dbt-sql.instructions.md`
- Ask for Jinja-templated SQL following dbt conventions
- Request schema tests alongside every new model
- Ask Copilot to generate `schema.yml` entries for new models

## Contributing Process

### 1. Fork and Clone
```bash
git clone https://github.com/your-username/copilot-data-eng-starter.git
cd copilot-data-eng-starter
```

### 2. Set Up Your Environment

#### Python (included by default)
```bash
make install
source venv/bin/activate
make test
```

#### For dbt Projects
```bash
pip install dbt-databricks  # or your adapter
dbt init
# Follow dbt conventions in .github/instructions/dbt/
```

### 3. Development Workflow

```bash
# 1. Understand requirements (read docs/specs/spec.md)
# 2. Write failing tests (TDD Red)
# 3. Implement minimal solution (TDD Green)
# 4. Refactor for quality (TDD Refactor)
# 5. Run full test suite
make test  # Python

# 6. Format and lint
make format
make lint

# 7. Commit with conventional format
git commit -m "feat: add user authentication with OAuth2"
```

### 4. Pull Request Process

#### Before Submitting
- ✅ All tests pass (`make test`)
- ✅ Code formatted (`make format`)
- ✅ Linting clean (`make lint`)
- ✅ Pre-commit hooks pass
- ✅ Documentation updated
- ✅ Security review completed

#### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Security review passed
- [ ] Performance impact assessed
```

## Examples

### Python TDD Example

```python
# 1. Write failing test first (Red)
def test_email_validator():
    validator = EmailValidator()
    assert validator.is_valid("user@example.com") == True
    assert validator.is_valid("invalid-email") == False

# 2. Implement minimal code (Green)
class EmailValidator:
    def is_valid(self, email: str) -> bool:
        return "@" in email  # Minimal implementation

# 3. Refactor for quality (Refactor)
import re

class EmailValidator:
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}}$')

    def is_valid(self, email: str) -> bool:
        """Validate email format using regex."""
        if not isinstance(email, str):
            return False
        return bool(self.EMAIL_REGEX.match(email.strip()))
```

**Copilot Tips**: Use `refactor-python` skill in step 3 to further optimize code structure, add type hints, and ensure security best practices.

### dbt Model Example

```sql
-- models/staging/stg_raw__orders.sql
with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        total_amount
    from source
)

select * from renamed
```

```yaml
# models/staging/schema.yml
models:
  - name: stg_raw__orders
    description: Staged orders from the raw source
    columns:
      - name: order_id
        description: Unique order identifier
        tests:
          - not_null
          - unique
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'completed', 'cancelled']
```

**Copilot Tips**: Reference `.github/instructions/dbt/dbt-sql.instructions.md` when asking Copilot to generate dbt models. Always ask for accompanying `schema.yml` tests.

## Troubleshooting

### Copilot Issues
- **Not following instructions**: Provide more context and be specific
- **Security concerns**: Always review and test generated code
- **Wrong language version**: Specify version explicitly
- **Poor suggestions**: Break down into smaller, focused requests

### Development Issues
- **Test failures**: Check test setup and dependencies
- **Linting errors**: Run `make format` and `make lint`
- **Pre-commit failures**: Address issues before committing
- **Performance problems**: Profile code and optimize bottlenecks

## Resources

### Documentation
- [VIBE_CODING_GUIDE.md](VIBE_CODING_GUIDE.md) - This guide
- [spec.template.md](spec.template.md) - Specification template
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development workflow
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

### Copilot Skills
The repository includes specialized skills for common development tasks:
- **create-spec**: Specification-driven development; writes `docs/specs/spec.md`
- **create-tasks**: Decomposes a spec into ordered, executable tasks at `docs/specs/tasks.md`
- **audit-security**: Comprehensive security audits with OWASP Top 10 checks
- **refactor-python**: Python code refactoring and optimization
- **generate-prompt**: Generate structured multi-step prompts
- **run-prompt**: Execute saved prompts as isolated sub-tasks

See the "Available Copilot Skills" section above for detailed usage.

### Tools
- **Python**: pytest, black, pylint, pyright, mypy
- **dbt**: dbt-databricks, dbt-spark, dbt-core
- **Databricks**: Databricks CLI, databricks-connect
- **Git**: pre-commit hooks, conventional commits

### Learning
- [Test-Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Clean Code](https://www.oreilly.com/library/view/clean-code/9780136083238/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [Databricks Documentation](https://docs.databricks.com/)

## Questions?

- **For spec clarification**: Check docs/specs/spec.md or ask maintainers
- **For implementation help**: Reference language-specific instructions
- **For Copilot issues**: Try rephrasing prompts with more context
- **For general questions**: Check existing issues or create new discussion

Remember: Vibe coding is about enjoying the process while maintaining high standards. Use Copilot as your coding companion, but always apply your expertise and judgment!

🚀 Happy coding! 🎯
