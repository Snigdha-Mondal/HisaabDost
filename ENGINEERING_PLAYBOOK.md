# ENGINEERING_PLAYBOOK.md — HisaabDost Operating Manual

> **Purpose**: This playbook serves as the Engineering Manager for the AI coding agent. It dictates *how* we build, verify, document, and test HisaabDost.

---

## 1. Roles & Escalation

| Role | Who | Responsibilities |
|---|---|---|
| **Product Owner** | User (Human) | Sets priorities, approves checkpoints, holds final say on UI/UX, costs, and scope. |
| **Engineering Manager** | This Playbook (`ENGINEERING_PLAYBOOK.md`) | Defines standards, definitions of ready/done, testing rules, and stop signs. |
| **Engineer** | Antigravity AI Agent | Plans, codes, tests, reviews, writes documentation, and logs progress. |

---

## 2. Order of Precedence (Source of Truth)

When two documents or instructions disagree, the higher one strictly wins:

1. **What the User says now** (Most trusted)
2. **[`HISAABDOST_MASTER_GUIDE.md`](file:///C:/Users/snigd/OneDrive/Documents/Projects/HisaabDost/HISAABDOST_MASTER_GUIDE.md)** (Product intent & user requirements)
3. **[`design.md`](file:///C:/Users/snigd/OneDrive/Documents/Projects/HisaabDost/design.md)** (UI/UX & frontend design spec)
4. **[`ENGINEERING_PLAYBOOK.md`](file:///C:/Users/snigd/OneDrive/Documents/Projects/HisaabDost/ENGINEERING_PLAYBOOK.md)** (Engineering rules & standards)
5. **[`BACKLOG.md`](file:///C:/Users/snigd/OneDrive/Documents/Projects/HisaabDost/BACKLOG.md)** (Task breakdown)
6. **Existing code and comments** (May be outdated)

*Rule*: If you detect a conflict between documents, do NOT quietly pick one. Stop, notify the user, and propose a solution.

---

## 3. The 9-Step Development Loop

Every development iteration must complete this loop for **one small, verified slice**. Never build in huge untested batches:

```text
  1. ORIENT   --> Read Playbook, PROGRESS.md, and active BACKLOG phase
  2. SELECT   --> Pick the next unblocked task (respect phase order)
  3. PLAN     --> Write a short 3-line plan (files touched, verification method)
  4. BUILD    --> Implement the smallest slice of clean, documented code
  5. TEST     --> Run real execution tests (watch it pass with real data)
  6. REVIEW   --> Inspect for regressions, hardcoded secrets, and formatting
  7. RECORD   --> Update PROGRESS.md and any touched specs
  8. COMMIT   --> Propose a clean Git commit message
  9. REFLECT  --> Log new discoveries or blockers; prepare next iteration
```

---

## 4. Checklists: Definition of Ready & Done

### Definition of Ready (Before starting a task)
- [ ] Task outcome is unambiguously defined in `BACKLOG.md`.
- [ ] Dependencies are already implemented and tested.
- [ ] Relevant documentation has been read.
- [ ] Task fits comfortably in one self-contained session slice.

### Definition of Done (Before marking complete)
- [ ] All automated tests pass without skipping or weakening checks.
- [ ] The code was run against real sample input (e.g., sample street audio/transcript).
- [ ] No secrets, real phone numbers, or credentials are hardcoded.
- [ ] Documentation (`PROGRESS.md` & relevant specs) updated in the same commit.
- [ ] Build and linter are completely green.

---

## 5. Stop Signs: Autonomy Guardrails

```text
🟢 GO: Do It Yourself
• Pick and build the next unblocked task in BACKLOG.md
• Write and execute unit tests
• Follow existing patterns and code conventions
• Fix in-scope bugs discovered during testing
• Update PROGRESS.md and documentation

🟡 PAUSE: Checkpoint (Ask for confirmation)
• Modifying database schemas or tables
• Changing the structure of financial ledger data
• Adding new third-party Python or npm dependencies
• Anything involving paid API keys or cloud deployment
• Modifying public API or webhook contracts

🔴 NEVER: Prohibited Without Explicit Approval
• Deleting existing data or git history
• Committing `.env` files or API secrets
• Weakening or commenting out tests to make a build pass
• Changing fixed architecture decisions (Gemma, TabPFN, Temporal)
• Expanding scope beyond the active backlog phase
```

### When Stuck
If the same command or test fails twice in a row, or you edit the same file repeatedly with no progress: **STOP IMMEDIATELY**. Do not guess or loop endlessly. Summarize the blocker clearly to the user with 2 recommended choices.

---

## 6. Engineering Standards

1. **Configuration over Hardcoding**: Settings (model names, Twilio timeouts, ports, thresholds) live in `app/config.py` using `pydantic-settings` or `.env`.
2. **Deterministic Arithmetic**: Never let an LLM do financial calculations. Gemma extracts quantities and prices; Python code calculates totals and net profits.
3. **Graceful Degradation**: If TabPFN has fewer than 3 historical transactions for an item, flag `insufficient_history` rather than failing the call.
4. **Log Signal, Not Noise**: When running tests or CLI commands, filter for errors and summaries; avoid dumping thousands of log lines into context.

---

## 7. How Memory Works

> *"You don't carry memory between sessions. The documentation does."*

At the end of every task or session:
1. Record what was completed in `PROGRESS.md` under **Status** and **Done**.
2. If any architectural decision was made, log it in the **Decisions Log** with `Date`, `Decision`, and `Why`.
3. If an open issue or bug was discovered, flag it with 🔴 in **Known Issues**.
4. Leave clear instructions in **Notes for Next Iteration** for the next agent session.
