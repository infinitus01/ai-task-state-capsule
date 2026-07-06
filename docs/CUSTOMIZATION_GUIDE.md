# Customization Guide

## Directory Layout

**Recommended layout:**

```text
your-repo/
├── .capsule/
│   ├── TASK_STATUS_REPORT.md
│   ├── DECISION_LOG.md
│   ├── BRANCH_INFO.md
│   ├── RESUME_INSTRUCTIONS.md
│   ├── RECOVERY_CHECK.md
│   └── STATE_MANIFEST.json
└── src/
```

**Alternative:** Sibling directory outside the code repo for research-only tasks.

## Adapting Templates

1. Copy `templates/` to your capsule directory
2. Set `project_name` in manifest
3. Replace placeholder sections; keep heading structure for tooling compatibility

## Status Classifications

Add subsections under Done / In Progress / Todo if needed, but keep the six top-level buckets for cross-tool consistency.

## Decision Log

Use your own ID scheme (`DEC-YYYYMMDD-NNN` or `ADR-001`). Keep **Status** field values stable: `proposed`, `accepted`, `superseded`, `rejected`.

## Branch Names

Short, kebab-case: `experiment/new-api`, not `experiment/trying_the_new_api_design_v2`.

## Compressed Summary Rules

- 150–250 words
- Past tense for done work, present for state, future for next steps
- No marketing language; include file paths and version hash when relevant

## Schema Version

`STATE_MANIFEST.json` uses `schema_version: "0.1.0"`. Bump only when breaking field changes occur. Document migrations in `DECISION_LOG.md`.

## Tool-Specific Notes

| Tool | Suggestion |
|------|------------|
| Cursor | Keep capsule in repo; @-mention files on resume |
| Claude Code | Paste resume block in first message |
| Grok | Attach capsule ZIP or individual md files |
| Codex | Same as Claude; prefer manifest for machine checks |

## What Not to Customize Away

- Version hash format (`vYYYYMMDD-HHMM-xxxx`)
- Six core file names (for interoperability)
- Resume instruction closing line: `Resume this task from version [VERSION_HASH].`