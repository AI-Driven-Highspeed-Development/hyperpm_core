---
applyTo: "**/.kanbn/tasks/*.md"
---

# Task Writing Standards for HyperPM

## Purpose

This document defines how HyperPM writes task descriptions. The goal is consistency, traceability, and actionability without inventing requirements.

## Core Principle: Source-Based Writing

**NEVER invent requirements.** All task details MUST trace back to:

- User's explicit request
- Blueprint documents (`.agent_plan/`)
- Existing code or module documentation
- Referenced source documents

If no source exists, keep the description minimal and factual. State only what is known.

## Required Metadata Fields

Every task MUST have these fields populated when information is available:

**Always Required:**
- `tags` — At minimum: one work-type tag, one priority tag, one workload tag

**Fill If Known:**
- `assigned` — Who owns this task (from user input or project context)
- `due` — Deadline if specified or implied by milestone

**Auto-Managed:**
- `created` — Set by MCP on creation
- `updated` — Set by MCP on modification
- `progress` — Default 0.0, update as subtasks complete

## Tag Selection Guidelines

### Priority Tags (Required - Pick One)

Estimate relative to OTHER tasks on the board:

- `urgent` — Blocking other work, needed today
- `high-priority` — Critical path, needed this week
- `medium-priority` — Important but not blocking
- `low-priority` — Nice to have, can wait

### Workload Tags (Required - Pick One)

Estimate relative to OTHER tasks on the board:

- `Nothing` (0) — Trivial, minutes
- `Tiny` (1) — Under 1 hour
- `Small` (2) — 1-4 hours, half day
- `Medium` (3) — 4-8 hours, full day
- `Large` (5) — 2-3 days
- `Huge` (8) — Week or more

### Work-Type Tags (Required - Pick One or More)

- `feature` — New functionality
- `bug` — Defect fix
- `chore` — Maintenance, cleanup
- `refactor` — Restructure without behavior change
- `testing` — Test creation or execution
- `documentation` — Docs, README, comments
- `research` — Investigation, spike
- `review` — Code review, audit

### Domain Tags (Optional - Pick Relevant)

- `frontend`, `backend`, `database`, `api`
- `infrastructure`, `security`, `devtools`
- `config`, `logging`, `performance`

## Description Structure

Use this structure for task descriptions. Omit sections that have no content.

### Section 1: Context Line

One sentence stating what stage/milestone this belongs to and the high-level goal.

Example:
```
**Stage 1: Authentication** — Create the session manager CLI for user operations.
```

### Section 2: Summary

2-3 sentences explaining what this task accomplishes. Write for someone unfamiliar with the codebase.

### Section 3: Acceptance Criteria (If Source Exists)

List what "done" looks like. Use plain text with checkmark emoji or bullet points.

Example:
```
✅ User creation via CLI works
✅ Session tokens generated correctly
✅ Integration with auth_manager tested
```

Avoid markdown checkboxes (`- [ ]`) as they render poorly in some viewers.

### Section 4: Technical Details (If Source Exists)

Include ONLY details from source documents:

- File paths and locations
- Dependencies on other modules
- Code patterns to follow
- Configuration requirements

Use code blocks for file structures or command examples.

### Section 5: Notes or Warnings (Optional)

Any gotchas, blockers, or special considerations.

## Formatting Rules

**Line Breaks:**
Single `\n` does not create visual separation. Always use double line breaks between paragraphs and sections.

**Avoid:**
- Markdown checkboxes (`- [ ]`) — Use ✅ or bullet points instead
- Tables — They render inconsistently
- Deeply nested lists — Keep structure flat

**Prefer:**
- Short paragraphs (2-4 sentences)
- Code blocks for technical content
- Emoji sparingly for visual anchors (✅, ⚠️, 📁)

## Examples

### Minimal Task (No Source Document)

When user says "add a login page" with no further details:

```
**Stage 1: Authentication** — Add login page to web interface.

User requested a login page. No design spec or technical requirements provided yet.

Awaiting further specification before implementation.
```

### Detailed Task (With Source Document)

When blueprint or spec exists:

```
**Stage 1: Authentication** — Implement session manager CLI commands.

Add CLI interface to session_manager for user and session operations. Commands register via cli_manager with short alias "ssm".

✅ session_manager_cli.py created with register_cli() function
✅ Commands: create-user, list-users, revoke, delete-user
✅ refresh.py calls register_cli() on framework refresh
✅ Integration tested with admin_cli.py

**File Location:** managers/session_manager/session_manager_cli.py

**Commands to Implement:**

python admin_cli.py ssm create-user --username NAME
python admin_cli.py ssm list-users
python admin_cli.py ssm revoke --username NAME

**Pattern Reference:** Follow managers/secret_manager/secret_cli.py
```

## Anti-Patterns

**DO NOT:**

- Invent requirements not in source docs
- Copy entire blueprint sections verbatim (summarize instead)
- Leave priority or workload tags empty
- Write vague descriptions like "implement the thing"
- Create tasks without understanding what they ask for

**DO:**

- Quote or reference source documents
- Ask user for clarification if requirements unclear
- Keep descriptions scannable (headers, short paragraphs)
- Estimate priority/workload relative to board context
