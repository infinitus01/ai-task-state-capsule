# How I Handle the "Gap" in Long-Running AI Tasks

A short, domain-neutral note on why this format exists.

---

## The bottleneck is usually not the model

When I use AI for multi-day work, the friction is rarely "it cannot write the code." More often:

- A new session does not know what the previous one finished
- Long chats drift, repeat work, or change direction silently
- Important decisions live inside conversation threads and are hard to retrieve later
- Version control remembers file diffs, but not **task context**

I call this the **long-task gap** — a seam between models, IDEs, and agents, not a weakness in any single tool.

---

## Chat history is a poor task database

Chat is great for **exploration**. It is a weak **source of truth**:

| What you need to keep | Why chat struggles |
|-----------------------|-------------------|
| Current progress | Hard to search and diff |
| Why a decision was made | Buried in long threads |
| What the next step may do | Easy for AI to over-extend |
| What is still unverified | Easy to lose |
| How to hand off to the next session | You retell the whole story |

The fix is not "a better prompt." Long tasks need a **handoff-friendly state format**.

---

## My approach: a task state capsule

At meaningful milestones, I extract task state from chat into a small, fixed set of files — a **Task State Capsule**.

The product is not a new app. The product is a **stable shape**:

```text
Status report      → progress, blockers, next actions
Decision log       → choices, rationale, alternatives
Branch info        → main / experiment / rollback / review naming
Resume instructions → paste-ready prompt for the next AI session
Recovery checklist  → what to check when the AI drifts
State manifest      → version hash, timestamps, machine-readable metadata
```

Conceptually, this is an **Interlock Layer** between sessions:

```text
Session A reaches a milestone → update capsule → Session B resumes from capsule
```

Conversation becomes the **working process**. The capsule becomes the **shift-change snapshot**.

---

## A generic workflow

1. Save at clear milestones — not after every message
2. Spend a few minutes updating the capsule instead of re-explaining context in a new chat
3. In the next session, paste resume instructions and attach the capsule
4. If scope creeps, run the recovery checklist instead of arguing from scratch

The format is **tool-neutral**: models, IDEs, and agents can change; the capsule shape does not have to.

---

## Three layers, three jobs

| Layer | Remembers |
|-------|-----------|
| Version control (e.g. Git) | Code and file changes |
| Task capsule | Progress, decisions, next steps, boundaries |
| Audit bundle (optional) | Whether a deliverable can be verified |

A capsule does not replace Git or export raw chat. It holds **live task state while the work is still moving**.

---

## One intuition

The stronger AI gets, the more **handoff and verification** matter — not less.

As generation speeds up, cost often shifts to:

- How to continue
- How to bound scope
- How to show a step is actually done

So I stopped asking, "Will the next session remember?"  
I started asking, **"Do I have task state worth handing off?"**

---

## Where this repo fits

[`ai-task-state-capsule`](../README.md) is an early, open template for that idea: file format, templates, and packaging scripts — not a hosted platform or autonomous agent.

Standardizing how long tasks survive across sessions matters more to me right now than promoting a product narrative.

For the full concept layer, see [`INTERLOCK_LAYER.md`](INTERLOCK_LAYER.md).  
Chinese version: [`WHY_TASK_STATE_CAPSULE.zh.md`](WHY_TASK_STATE_CAPSULE.zh.md).