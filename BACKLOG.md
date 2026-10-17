# BACKLOG.md — Phased Task List for HisaabDost

> **Legend**:  
> `[ ]` Not Started  
> `[>]` In Progress  
> `[x]` Completed & Verified  
> `🔒` Requires Human Checkpoint / Approval before proceeding  

---

## Phase 1: Project Foundation & Mock Simulator
*Exit Goal*: A running local environment with mock phone calls and baseline directory structure.

- [x] **1.1 Project Scaffolding**: Setup `pyproject.toml`, directory tree, `.env.example`, and `.gitignore`.
- [x] **1.2 Pydantic Financial Schemas**: Implement `ExpenseItem`, `DailyAuditSummary`, and `VendorProfile` in `app/agent/schemas.py`.
- [x] **1.3 Mock Telephony CLI Simulator**: Create `scripts/mock_call.py` allowing developers to simulate an 8:30 PM vendor phone call from the terminal.
- [x] 🔒 **1.4 Phase 1 Checkpoint**: Verify mock runner prints structured input/output end-to-end.

---

## Phase 2: Gemma 2 Colloquial Entity Extraction Engine
*Exit Goal*: Raw spoken transcripts (Hindi, Hinglish, English) parsed into strict financial JSON.

- [x] **2.1 Prompt Engineering**: Create few-shot prompt in `app/agent/prompts.py` supporting Indian street slang ("dabba", "liter", "kilo", "galla").
- [x] **2.2 Gemma 2 Adapter**: Implement `app/agent/gemma_parser.py` using Ollama / HuggingFace / Gemini API fallback.
- [x] **2.3 Dialect Unit Tests**: Implement `tests/test_gemma_parser.py` with 5 authentic street vendor test audio transcripts.
- [x] 🔒 **2.4 Phase 2 Checkpoint**: Review parser accuracy and currency safety.

---

## Phase 3: TabPFN Price-Gouging Anomaly Engine
*Exit Goal*: Historical 30-day CSV ledger evaluated; price spikes >8% flagged with warnings.

- [x] **3.1 Baseline Dataset**: Create `data/sample_history.csv` containing 30 days of tea stall purchase logs.
- [x] **3.2 TabPFN Anomaly Detector**: Implement `app/audit/tabpfn_engine.py` to compare new unit prices against moving average.
- [x] **3.3 Anomaly Unit Tests**: Implement `tests/test_tabpfn_anomaly.py` verifying oil and milk price spike flags.
- [x] 🔒 **3.4 Phase 3 Checkpoint**: Verify mathematical calculations (extra rupee overcharge) are 100% accurate.

---

## Phase 4: Temporal Durable Workflows
*Exit Goal*: Daily closing call scheduled, with 15-minute retry on busy line and state persistence.

- [x] **4.1 Workflow Definition**: Implement `DailyClosingWorkflow` in `app/workflows/closing_workflow.py`.
- [x] **4.2 Activities Implementation**: Implement activities for call placement, parsing, audit, and SMS dispatch in `app/workflows/activities.py`.
- [x] **4.3 Telephony Failure Simulation**: Test workflow behavior when the vendor line is busy or unanswered.
- [x] 🔒 **4.4 Phase 4 Checkpoint**: Verify Temporal UI shows clean execution history and retry backoffs.

---

## Phase 5: Voice Synthesis & Caregiver Dashboard
*Exit Goal*: Spoken feedback audio synthesized via ElevenLabs and live dashboard connected.

- [x] **5.1 ElevenLabs Voice Bridge**: Implement `app/voice/elevenlabs_client.py` for warm Hindi/English TTS generation.
- [x] **5.2 Sentry Agent Tracing**: Configure Sentry spans for LLM, TabPFN, and TTS audio latency.
- [x] **5.3 Web Dashboard Integration**: Connect `demo.html` / Next.js to FastAPI backend for live call visualization.
- [x] 🔒 **5.4 Phase 5 Checkpoint**: Full demo call tested live with audio output.

---

## Phase 6: Hackathon Submission & Agent Skill
*Exit Goal*: Reusable Agent Skill packaged, demo video recorded, and DEV post staged.

- [x] **6.1 Agent Skill Packaging**: Finalize `skills/voice-ledger-audit/SKILL.md` following Open Standards.
- [x] **6.2 Video Demo Recording**: Rehearse 3-minute hackathon pitch following demo script.
- [x] **6.3 DEV Challenge Post**: Stage submission article highlighting Gemma 2, TabPFN, and Temporal.
- [x] 🔒 **6.4 Final Project & Hackathon Delivery**: All 6 phases complete, verified with 35/35 passing unit tests and published documentation.
