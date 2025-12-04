---
applyTo: "**/.kanbn/**"
---

# Kanbn Format Specification

## Purpose
Standardized format for `kanbn` planning boards used by the HyperPM agent.
This format is compatible with the [kanbn](https://github.com/basementuniverse/kanbn) tool and VS Code extension.

## Directory Structure
- **Root**: `.kanbn/`
- **Index File**: `.kanbn/index.md`
- **Tasks Directory**: `.kanbn/tasks/`
- **Task Files**: `.kanbn/tasks/<task-id>.md`

## Index File Structure (`index.md`)

The index file defines the board columns and lists the tasks within them.

```markdown
---
# Optional Project Options in YAML front-matter
hiddenColumns:
  - Archive
startedColumns:
  - In Progress
completedColumns:
  - Done
defaultTaskWorkload: 2
taskWorkloadTags:
  Nothing: 0
  Tiny: 1
  Small: 2
  Medium: 3
  Large: 5
  Huge: 8
---

# Project Name

Project description goes here.

## Backlog

- [task-title] (tasks/task-title.md)
- [another-task] (tasks/another-task.md)

## In Progress

- [active-task] (tasks/active-task.md)

## Done

- [completed-task] (tasks/completed-task.md)
```

### Rules for Index
- **Use Options**: For new boards, use the above YAML front-matter options.
- **Level-1 Heading**: Must be the Project Name.
- **Level-2 Headings**: Define the Columns (Lanes).`
- **Task Links**: Must be relative links to files in the `tasks/` directory. Format: `- [filename] (tasks/<filename>.md)`. Must use kebab-case for filenames and titles, they must match exactly. NO spaces between brackets and parentheses (the example above with a space is to make this stupid markdown parser not freak out...).

## Task File Structure (`tasks/<task-id>.md`)

Each task is a separate markdown file.

```markdown
---
created: 2023-10-27T10:00:00.000Z
updated: 2023-10-27T11:00:00.000Z
assigned: "User"
progress: 0.0
tags:
  - "feature"
  - "high-priority"
due: 2023-11-01T17:00:00.000Z
---

# Task Name

Detailed description of the task.
Can include multiple paragraphs, code blocks, etc.
Follow markdown syntax.

## Sub-tasks

- [ ] First sub-task
- [x] Completed sub-task

## Relations

- [blocks other-task.md] (other-task.md)

## Comments

- author: "User"
  date: 2023-10-27T12:00:00.000Z
  This is a comment.
```

### Rules for Tasks
- **Filename**: Use kebab-case (e.g., `implement-login-feature.md`).
- **Task Name**: Use plain English words separated by spaces.
    - AVOID underscores (`_`), special characters (`!?.,@:;|\"'` etc.), and code-style naming.
    - The kanbn library converts names to kebab-case IDs using `paramCase()` which has specific camelCase handling.
    - If the task name contains underscores or special chars, the derived ID may not match the filename, causing silent render failures.
    - ❌ Bad: `Add workspace_core tests` → ID mismatch risk
    - ✅ Good: `Add workspace core tests` → clean ID: `add-workspace-core-tests`

### Task ID Generation (CRITICAL)

The kanbn library uses `paramCase()` from the `change-case` package to generate task IDs from names. This algorithm has specific behavior with camelCase and acronyms:

#### Algorithm Rules
1. **Spaces** → hyphens (`Setup Project` → `setup-project`)
2. **camelCase splits** → hyphens inserted before uppercase letters (`FastAPI` → `fast-api`)
3. **Consecutive uppercase (acronyms)** → treated as single word (`HTTP` → `http`, `XMLParser` → `xmlparser`)
4. **Numbers** → preserved, hyphen inserted before uppercase after number (`123Test` → `123-test`)
5. **Special characters** → removed
6. **Underscores** → converted to hyphens

#### Examples (verified against actual kanbn)
| Task Name | Generated ID | Notes |
|-----------|--------------|-------|
| `Setup FastAPI Project` | `setup-fast-api-project` | camelCase splits |
| `OAuth2 Provider` | `oauth2-provider` | Number stays attached |
| `MyOAuth2Provider Test` | `my-oauth2-provider-test` | Complex camelCase |
| `HTTPServer Setup` | `httpserver-setup` | Acronym = single word |
| `XMLParser Implementation` | `xmlparser-implementation` | Acronym = single word |
| `getHTTPResponse Handler` | `get-httpresponse-handler` | Mixed case + acronym |
| `userID Validation` | `user-id-validation` | Ends with acronym |
| `iOS App Support` | `i-os-app-support` | Single lowercase before caps |
| `Test123 Feature` | `test123-feature` | Word + number |
| `123Test Feature` | `123-test-feature` | Starts with number |
| `Simple Task` | `simple-task` | Normal case |
| `already-kebab-case` | `already-kebab-case` | Already kebab |

#### Best Practices
- **AVOID camelCase in task names** when possible - use spaces instead
- **AVOID acronyms** like `API`, `HTTP`, `XML` in task names - spell them out or use lowercase
- **PREFER**: `Setup Fast API Project` over `Setup FastAPI Project` for predictable IDs
- The MCP handles ID generation automatically - use the MCP tools, NEVER manually create task files
- **YAML Front-matter**:
    - `created`: ISO 8601 date string.
    - `updated`: ISO 8601 date string.
    - `assigned`: String (optional), must have quotation marks.
    - `progress`: Number between 0.0 and 1.0.
    - `tags`: List of strings. Must be list format.
    - `due`: ISO 8601 date string (optional).
    - `started`: ISO 8601 date string (optional).
    - `completed`: ISO 8601 date string (optional).
- **Level-1 Heading**: Must be the Task Name.
- **Reserved Level-2 Headings**:
    - `## Sub-tasks`: List of checklist items (`- [ ]` or `- [x]`).
    - `## Relations`: List of links to other tasks.
    - `## Comments`: List of comments with `author` and `date`. Must get system time for date.

**DO NOT** need to include all reserved sections if not applicable, any empty sections will cause parsing errors.

#### Available Tags

- You must use tags from the following predefined set to ensure consistency across tasks, you may use multiple tags per task.
- You must include at least one tag from the "Task Workload Tags" category, default workload is "Small" if none specified.
- You must also include at least one tag from the "Priority Tags" category to indicate task urgency.

##### Work Type Tags
- feature: New feature implementation
- bug: Bug fixing
- chore: Routine tasks, dependency updates, code cleanup
- refactor: Code restructuring without changing functionality
- testing: Writing and running tests
- documentation: Writing and updating documentation
- research: Exploration and feasibility tasks
- design: Architectural or visual design tasks
- planning: Requirements gathering and task breakdown
- spike: Timeboxed investigation or proof-of-concept

##### Domain / Component Tags
- frontend: Client-side, UI, and presentation layer
- backend: Server-side logic and services
- database: Data storage, schema, and queries
- api: API endpoints and integrations
- infrastructure: Deployment, servers, and environment setup
- ci-cd: Continuous Integration and Deployment pipelines
- security: Authentication, authorization, and safety
- performance: Optimization and efficiency improvements
- accessibility: Usability and accessibility improvements
- ui-ux: User Interface and User Experience design
- algorithm: Algorithm and computational logic
- devtools: Developer tooling, scripts, and CLI utilities
- config: Configuration files, settings, and environment variables
- logging: Logging, monitoring, and observability

##### Management Tags
- communication: Meetings, emails, and coordination
- training: Onboarding and knowledge transfer
- review: Code review and quality assurance
- devops: Operations and infrastructure management
- maintenance: General upkeep and system health
- meta: Meta tasks related to project management itself
- support: User support, issue triage, and assistance

##### Priority Tags
- urgent: Tasks requiring immediate attention
- high-priority: Tasks with high priority
- medium-priority: Tasks with medium priority
- low-priority: Tasks with low priority
- not-planned: Tasks not planned for current cycle, but may be revisited later
- blocked: Tasks currently blocked by dependencies

##### Task Workload Tags
- Nothing: 0
- Tiny: 1
- Small: 2
- Medium: 3
- Large: 5
- Huge: 8

## File Locations
- Workspace-level: `.kanbn/`
