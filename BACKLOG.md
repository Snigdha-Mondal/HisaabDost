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
- [ ] **1.2 Pydantic Financial Schemas**: Implement `ExpenseItem`, `DailyAuditSummary`, and `VendorProfile` in `app/agent/schemas.py`.
- [ ] **1.3 Mock Telephony CLI Simulator**: Create `scripts/mock_call.py` allowing developers to simulate an 8:30 PM vendor phone call from the terminal.
- [ ] 🔒 **1.4 Phase 1 Checkpoint**: Verify mock runner prints structured input/output end-to-end.

---

## Phase 2: Gemma 2 Colloquial Entity Extraction Engine
*Exit Goal*: Raw spoken transcripts (Hindi, Hinglish, English) parsed into strict financial JSON.

- [ ] **2.1 Prompt Engineering**: Create few-shot prompt in `app/agent/prompts.py` supporting Indian street slang ("dabba", "liter", "kilo", "galla").
- [ ] **2.2 Gemma 2 Adapter**: Implement `app/agent/gemma_parser.py` using Ollama / HuggingFace / Gemini API fallback.
- [ ] **2.3 Dialect Unit Tests**: Implement `tests/test_gemma_parser.py` with 5 authentic street vendor test audio transcripts.
- [ ] 🔒 **2.4 Phase 2 Checkpoint**: Review parser accuracy and currency safety.

---

## Phase 3: TabPFN Price-Gouging Anomaly Engine
*Exit Goal*: Historical 30-day CSV ledger evaluated; price spikes >8% flagged with warnings.

- [ ] **3.1 Baseline Dataset**: Create `data/sample_history.csv` containing 30 days of tea stall purchase logs.
- [ ] **3.2 TabPFN Anomaly Detector**: Implement `app/audit/tabpfn_engine.py` to compare new unit prices against moving average.
- [ ] **3.3 Anomaly Unit Tests**: Implement `tests/test_tabpfn_anomaly.py` verifying oil and milk price spike flags.
- [ ] 🔒 **3.4 Phase 3 Checkpoint**: Verify mathematical calculations (extra rupee overcharge) are 100% accurate.

---

## Phase 4: Temporal Durable Workflows
*Exit Goal*: Daily closing call scheduled, with 15-minute retry on busy line and state persistence.

- [ ] **4.1 Workflow Definition**: Implement `DailyClosingWorkflow` in `app/workflows/closing_workflow.py`.
- [ ] **4.2 Activities Implementation**: Implement activities for call placement, parsing, audit, and SMS dispatch in `app/workflows/activities.py`.
- [ ] **4.3 Telephony Failure Simulation**: Test workflow behavior when the vendor line is busy or unanswered.
- [ ] 🔒 **4.4 Phase 4 Checkpoint**: Verify Temporal UI shows clean execution history and retry backoffs.

---

## Phase 5: Voice Synthesis & Caregiver Dashboard
*Exit Goal*: Spoken feedback audio synthesized via ElevenLabs and live dashboard connected.

- [ ] **5.1 ElevenLabs Voice Bridge**: Implement `app/voice/elevenlabs_client.py` for warm Hindi/English TTS generation.
- [ ] **5.2 Sentry Agent Tracing**: Configure Sentry spans for LLM, TabPFN, and TTS audio latency.
- [ ] **5.3 Web Dashboard Integration**: Connect `demo.html` / Next.js to FastAPI backend for live call visualization.
- [ ] 🔒 **5.4 Phase 5 Checkpoint**: Full demo call tested live with audio output.

---

## Phase 6: Hackathon Submission & Agent Skill
*Exit Goal*: Reusable Agent Skill packaged, demo video recorded, and DEV post staged.

- [ ] **6.1 Agent Skill Packaging**: Finalize `skills/voice-ledger-audit/SKILL.md` following Open Standards.
- [ ] **6.2 Video Demo Recording**: Rehearse 3-minute hackathon pitch following demo script.
- [ ] **6.3 DEV Challenge Post**: Stage submission article highlighting Gemma 2, TabPFN, and Temporal.
