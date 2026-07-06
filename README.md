# ai-task-state-capsule

A lightweight, local-first **task state capsule format** for long-running AI workflows.

> **Status:** early release (v0.1.4). File format + templates + packaging scripts — not a hosted product, IDE plugin, or auto-sync service.

**Why this exists (short essay):** [English](docs/WHY_TASK_STATE_CAPSULE.md) · [中文](docs/WHY_TASK_STATE_CAPSULE.zh.md)

## Positioning: the Gap Between AI Endpoints

Most AI tools optimize models, IDEs, and agents. This project optimizes **what happens between them** — handoff, verification, evidence, and resume across sessions and tools.

That middle layer is the **AI Workflow Interlock Layer**. This repo implements one concrete format for it: the task state capsule.

Full concept: [`docs/INTERLOCK_LAYER.md`](docs/INTERLOCK_LAYER.md)

## What this is

When a coding or research task spans multiple AI sessions, chat history becomes hard to diff, hand off, and recover. This project defines six files that capture **durable task state**:

| File | Purpose |
|------|---------|
| `TASK_STATUS_REPORT.md` | Progress, blockers, next actions, compressed summary |
| `DECISION_LOG.md` | Decisions, rationale, alternatives, status |
| `BRANCH_INFO.md` | Experiment / rollback / review branch lineage |
| `RESUME_INSTRUCTIONS.md` | Copy-paste prompt for the next AI session |
| `RECOVERY_CHECK.md` | Checklist when the AI drifts or a branch fails |
| `STATE_MANIFEST.json` | Machine-readable metadata |

Think: **checkpoint save for AI work** — versioned, auditable, tool-neutral.

## What this is not

Do not mistake this project for:

| Misread | Reality |
|---------|---------|
| Prompt manager / prompt library | Curated **task state**, not prompt collection |
| Chat exporter | Intentionally **not** a raw chat dump |
| Clipboard watcher | No background capture |
| Cloud sync platform | Local-first; ZIP/Git optional |
| VS Code / Chrome extension | File format only |
| Trading system / strategy platform | Can document research state; does not execute trades |
| Replacement for Git, issues, or design docs | Complements them for **session handoff** |

## Who it is for

- Developers using Codex, Claude Code, Grok, Cursor, or similar for **multi-day tasks**
- Research workflows with experiments, rejected options, and hard gates
- Teams that need **human or AI handoff** without re-explaining context
- Anyone who wants task state beside a code repo (`.capsule/` or sibling folder)

## Who it is not for

- One-shot Q&A
- Teams already fully covered by tickets + specs + CI with no AI handoff pain
- Real-time automation or intraday decision systems

## Examples

| Example | Shows |
|---------|-------|
| [`examples/example-coding-task/`](examples/example-coding-task/) | Generic multi-day coding / planning capsule |
| [`examples/example-twse-research/`](examples/example-twse-research/) | Real-style **research-state** capsule: baseline null, virtual trade blocked, read-only audit adapter |

The TWSE example demonstrates a common high-value pattern:

```text
research mode ≠ trade mode
baseline not accepted → do not enable simulation
next step = dry-run export / audit only
```

## Quick start

```bash
cp -r templates/ my-task-capsule/
# edit TASK_STATUS_REPORT.md + STATE_MANIFEST.json as you work
git add my-task-capsule/
```

Resume in a new AI session:

1. Paste `RESUME_INSTRUCTIONS.md` into the new session
2. Attach the capsule files (or a sealed ZIP)
3. If the AI drifts, run `RECOVERY_CHECK.md`

## Packaging

```bash
python scripts/patch_release.py          # source + capsule + audit ZIPs
python scripts/generate_capsule_zip.py --source examples/example-twse-research
python scripts/verify_zips.py
```

Audit archives use **external sealing** (final SHA not stored inside the audit ZIP):

```text
dist/ai-task-state-capsule-work-audit-v....zip
dist/ai-task-state-capsule-work-audit-v....zip.sha256
dist/ai-task-state-capsule-work-audit-v....sealed.json   # external .sealed.json
```

## Version hash

Format: `vYYYYMMDD-HHMM-xxxx` — see [`docs/VERSION_HASH_RULES.md`](docs/VERSION_HASH_RULES.md).

## Branching and recovery

Lightweight branch names: `main`, `experiment/<name>`, `rollback/<hash>`, `review/<name>`.

See [`docs/BRANCH_AND_ROLLBACK.md`](docs/BRANCH_AND_ROLLBACK.md), [`docs/GIT_CAPSULE_ALIGNMENT.md`](docs/GIT_CAPSULE_ALIGNMENT.md) · [中文](docs/GIT_CAPSULE_ALIGNMENT.zh.md), and [`docs/AI_RESUME_PROTOCOL.md`](docs/AI_RESUME_PROTOCOL.md).

## Suggested GitHub repo metadata

**Name:** `ai-task-state-capsule`

**Description (short):**
```text
Local-first file format for versioning, handoff, and recovery of long-running AI task state.
```

**Topics:** `ai-workflow`, `developer-tools`, `markdown`, `handoff`, `context-management`

**Do not use in description:** "prompt manager", "clipboard", "cloud platform", "autopilot", "trading bot"

## Maturity

| Area | Status |
|------|--------|
| File format | usable v0.1 |
| Templates + examples | yes |
| Packaging / verification scripts | yes |
| JSON Schema validation | not yet |
| Editor integrations | not planned as core |
| Community adoption | early / personal-scale |

## Future extensions

- JSON Schema for `STATE_MANIFEST.json`
- Capsule diff CLI
- Optional encryption for sensitive metadata
- Optional export adapters (never required for core use)

## License

MIT — see [`LICENSE`](LICENSE).

## Documentation

- [`docs/WHY_TASK_STATE_CAPSULE.md`](docs/WHY_TASK_STATE_CAPSULE.md) · [`docs/WHY_TASK_STATE_CAPSULE.zh.md`](docs/WHY_TASK_STATE_CAPSULE.zh.md) — motivation essay (EN / 中文)
- [`docs/INTERLOCK_LAYER.md`](docs/INTERLOCK_LAYER.md)
- [`docs/VERSION_HASH_RULES.md`](docs/VERSION_HASH_RULES.md)
- [`docs/BRANCH_AND_ROLLBACK.md`](docs/BRANCH_AND_ROLLBACK.md)
- [`docs/GIT_CAPSULE_ALIGNMENT.md`](docs/GIT_CAPSULE_ALIGNMENT.md) · [`docs/GIT_CAPSULE_ALIGNMENT.zh.md`](docs/GIT_CAPSULE_ALIGNMENT.zh.md) — Git + capsule dual rollback
- [`docs/AI_RESUME_PROTOCOL.md`](docs/AI_RESUME_PROTOCOL.md)
- [`docs/CUSTOMIZATION_GUIDE.md`](docs/CUSTOMIZATION_GUIDE.md)
- [`RELEASE.md`](RELEASE.md)