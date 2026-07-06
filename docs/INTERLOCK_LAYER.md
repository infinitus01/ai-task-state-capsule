# AI Workflow Interlock Layer

Most people focus on **endpoints**:

```text
Which model is stronger?
Which IDE is better?
Which agent writes better code?
Which tool is faster?
```

This project focuses on **what happens between endpoints**:

```text
How does a model hand off to the next task state?
How do humans and AI accept work?
How does session N connect to session N+1?
How do execution and audit stay separated?
How do results become evidence?
How do tools transport context to other tools?
```

That middle layer is the **AI Workflow Interlock Layer** — lightweight interfaces for handoff, rollback, audit, and resume.

> 專做 AI 工作流斷層修補：讓 AI 任務可交接、可回滾、可審計、可封存。

**One-line (EN):** workflow infrastructure for the gaps between AI tools.

---

## The gaps this layer addresses

### 1. Human ↔ AI

Not just “human asks, AI answers”:

```text
human intent
→ AI task understanding
→ executable specification
→ verifiable outcome
```

Without an interlock layer, AI sounds capable but tasks drift.

Common partial fixes: `AGENTS.md`, contracts, prompt discipline, **task capsules**.

### 2. AI session ↔ AI session

Typical failure:

```text
previous chat is long
next chat does not know what happened
context window fills → restart from scratch
```

Interlock fix:

```text
TASK_STATUS_REPORT
RESUME_INSTRUCTIONS
VERSION_HASH
ZIP capsule
```

Conversation becomes a **shift-change snapshot**, not a fragile memory thread.

### 3. AI execution ↔ AI review

Typical failure:

```text
AI says done
human half-believes it
no independent evidence
```

Interlock principle:

```text
Builder ≠ Reviewer
Executor ≠ Verifier
No evidence → no completion
```

A model saying PASS is not proof. Files inside a sealed archive, hashes, and external `.sealed.json` are.

### 4. Tool ↔ tool

ChatGPT, Claude, Codex, Cursor, browsers, and IDEs are strong **alone** but weakly connected.

Context Relay-style ideas address:

```text
Browser ↔ IDE
Claude ↔ Codex
human notes ↔ AI task
runtime ↔ archive
```

This is not a clipboard. It is a **context transport layer**.

### 5. Result ↔ evidence

AI tools often deliver:

```text
an answer
some code
a report
```

Long-running work needs:

```text
why was this done?
which files changed?
what was verified?
what was not verified?
which version is canonical?
can we roll back?
```

Audit ZIP, SHA-256 sums, external `.sealed.json`, and deliverable manifests address this gap.

---

## This repo is not “a tool” — it is an interface format

Tools change. Models change. IDEs change.

These needs do not:

```text
handoff
recovery
audit
sealing
comparison
acceptance
context transport
```

`ai-task-state-capsule` is one concrete format in the Interlock Layer — not the whole layer.

---

## Three-layer product map

| Layer | Solves | Examples in this ecosystem |
|-------|--------|----------------------------|
| **Context** | How context moves; how sessions resume | Task State Capsule, Resume Protocol, Context Relay (concept) |
| **Control** | How AI stays in bounds; who verifies | `DECISION_LOG.md`, `RECOVERY_CHECK.md`, rules, hooks, verifier agents |
| **Evidence** | What was done; how to prove it | audit ZIP, external `.sha256`, external `.sealed.json`, `verify_zips.py` |

Together they form **AI workflow infrastructure** — not a model, not an app runtime.

### How this repo maps today

| Layer | In `ai-task-state-capsule` |
|-------|----------------------------|
| Context | six capsule files, `RESUME_INSTRUCTIONS.md`, version hash |
| Control | `DECISION_LOG.md`, `RECOVERY_CHECK.md`, `BRANCH_INFO.md` |
| Evidence | `patch_release.py`, external seal files, `VERIFICATION_REPORT.external.md` |

---

## Why ZIP?

ZIP here is not nostalgia. It is the smallest portable protocol many environments already understand:

```text
ZIP        = state container
manifest   = readable index
hash       = identity
audit      = acceptance record
handoff    = next-session entry point
```

> **ZIP is the container. The format is the product.**

---

## Commercial value (why the gap matters)

Clients rarely fail because “AI cannot do the task.” They fail because:

```text
nobody knows how to continue after handoff
errors are hard to localize
people change → context breaks
models change → work restarts
progress cannot be shown on demand
AI output grows faster than governance
```

None of these are model problems. They are **workflow seam** problems.

> **The stronger AI gets, the more valuable the seams become.**

Faster generation increases pressure on handoff, review, sealing, and audit — not less.

---

## Positioning statement

**EN:**

> Workflow infrastructure for the gaps between AI tools.  
> This project defines a lightweight state capsule format for handoff, rollback, audit, and resume across long-running AI workflows.

**ZH:**

> 本專案處理 AI 對話與可持續任務執行之間的斷層。  
> 它不是聊天工具、prompt 倉庫或剪貼簿，而是一種任務狀態膠囊格式，用於交接、復原、審計與續接。

---

## What this document does not claim

- Not a hosted platform
- Not an agent runtime
- Not cloud sync or clipboard automation
- Not a replacement for Git, issues, or design docs
- Not HEA-specific or domain-locked

It documents the **conceptual layer** that `ai-task-state-capsule` implements in file form.