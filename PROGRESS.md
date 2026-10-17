# PROGRESS.md — Project Memory & Session Diary

> **Rule**: Update this file at the end of every development session or task slice. Code and documentation ship in the same commit.

---

## 1. Project Health & Current Status

* **Current Phase**: Phase 1 (Project Foundation & Mock Simulator)
* **Next Task**: `1.3 Mock Telephony CLI Simulator` (`scripts/mock_call.py`)
* **Overall Status**: 🟢 Phase 1 task 1.2 complete. All financial schemas and validation tests passing (12/12 total suite).
* **Last Verified Date**: 2026-10-17

---

## 2. What's Done

| Date | Task / Slice | Evidence / What Was Seen |
|---|---|---|
| 2026-10-17 | Product Specification | Created `HISAABDOST_MASTER_GUIDE.md` covering problem, business model, and Hacktoberfest strategy. |
| 2026-10-17 | UI/UX Design System | Created `design.md` covering Dukaan & Chai theme, wireframes, and component hierarchy. |
| 2026-10-17 | Interactive Prototype | Built `demo.html` with working retro button phone simulator and live audit dashboard. |
| 2026-10-17 | Agent Loop Framework | Established `AGENTS.md`, `ENGINEERING_PLAYBOOK.md`, `BACKLOG.md`, and `PROGRESS.md` (DeftBench methodology). |
| 2026-10-17 | 1.1 Project Scaffolding | Established directory tree, package `__init__.py` files, `pyproject.toml`, `.env.example`, `.gitignore`, baseline `sample_history.csv`, and verified with `tests/test_scaffolding.py` (4/4 passing). |
| 2026-10-17 | 1.2 Financial Schemas | Implemented `ExpenseItem`, `VendorProfile`, `DailyAuditSummary`, `GougingAlert`, and `CustomerCreditItem` with deterministic profit margin arithmetic and Pydantic validators in `app/agent/schemas.py`. Verified with `tests/test_schemas.py` (8/8 passing). |

---

## 3. Decisions Log

| Date | Decision | Rationale | Alternatives Considered |
|---|---|---|---|
| 2026-10-17 | Zero Hardware / Pure Software Telephony | Stall owners already own basic button phones. No hardware cost or soldering required; faster to build and ship. | Arduino UNO Q physical scanner box |
| 2026-10-17 | Gemma 2 for Dialect Extraction | Open-weight, free inference, handles colloquial Hinglish without cloud API billing. | Claude 3.5 / GPT-4o (Too expensive for $2/mo micro-SaaS) |
| 2026-10-17 | TabPFN for Tabular Price Auditing | Foundation model purpose-built for tabular in-context anomaly detection on CSV data. | Hardcoded static threshold rules or training custom XGBoost |
| 2026-10-17 | Temporal for Call Orchestration | Durable scheduling and automatic 15-minute retry backoff for busy street stalls. | Cron jobs / Celery (No native durable state recovery) |

---

## 4. Known Issues & Open Questions

* 🔴 None currently open.

---

## 5. Notes for Next Iteration

> **Start next session here**:  
> Read `AGENTS.md` $\rightarrow$ `ENGINEERING_PLAYBOOK.md` $\rightarrow$ `PROGRESS.md` $\rightarrow$ pick task `1.3 Mock Telephony CLI Simulator` from `BACKLOG.md`.  
> *Goal for next session*: Implement `scripts/mock_call.py` to simulate an 8:30 PM closing call with sample dialogues.
