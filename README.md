# HisaabDost (हिसाब दोस्त) ☕📞

> **Zero-Tech, Voice-First Daily Bookkeeper and Wholesale Price-Gouging Auditor for Roadside Micro-Vendors**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python: 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests: 35 Passed](https://img.shields.io/badge/tests-35%20passed-brightgreen.svg)](tests/)
[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026%20Week%202-orange.svg)](https://dev.to)
[![Prior Labs TabPFN](https://img.shields.io/badge/Audit-TabPFN--3.5-blueviolet.svg)](https://priorlabs.ai)
[![Temporal Workflows](https://img.shields.io/badge/Workflow-Temporal.io-black.svg)](https://temporal.io)

---

## 🌟 What is HisaabDost?

**HisaabDost (हिसाब दोस्त — "Accountant Friend")** brings Wall Street-grade financial auditing to the informal street retail economy. 

Every evening at **8:30 PM closing time**, HisaabDost places an automated voice phone call to an elderly roadside stall vendor's **basic $10 button phone** (e.g. Nokia 105 or JioBharat). 

The vendor does not open an app, read English, or type numbers. They simply answer the call and speak naturally in colloquial street Hindi or Hinglish about their day's sales and wholesale inventory purchases.

Within seconds, HisaabDost:
1. **Parses informal street slang** (*dabba*, *peti*, *galla*, *paav*) and safely ignores unbilled deliveries.
2. **Audits prices against historical data** using **TabPFN** tabular foundation models, catching wholesale price creep (>8% spikes) and calculating exact rupee overcharges.
3. **Performs deterministic financial arithmetic** (Total Sales − Expenses = Net Cash).
4. **Speaks back over the phone** in a warm, respectful elder-friendly voice (ElevenLabs).
5. **Dispatches an itemized receipt** via SMS/WhatsApp to the vendor's tech-savvy caregiver or family member.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Street_PSTN ["📞 Street Reality (Zero Tech)"]
        Vendor["Elderly Stall Owner<br/>($10 Button Phone)"]
    end

    subgraph Temporal_Cloud ["🔄 Durable Orchestration"]
        Workflow["DailyClosingWorkflow<br/>(8:30 PM Schedule)"]
        Retry["15-Min Exponential<br/>Retry Backoff Saga"]
        Workflow --> Retry
    end

    subgraph Intelligence_Core ["⚡ HisaabDost AI Pipeline"]
        Gemma["Gemma 2 (2B / 9B)<br/>Colloquial Dialect Extractor"]
        Ledger["30-Day Historical<br/>Wholesale CSV Ledger"]
        TabPFN["TabPFN-3.5 (Prior Labs)<br/>In-Context Tabular Auditor"]
        Math["Deterministic Python<br/>Financial Math Engine"]
        TTS["ElevenLabs Bilingual<br/>Elder-Friendly Audio"]
    end

    subgraph Web_Caregiver ["💻 Caregiver & Family Dashboard"]
        FastAPI["FastAPI Backend<br/>(Port 8000)"]
        Simulator["Retro Button Phone<br/>Browser Call Simulator"]
        Tracer["Sentry Latency Spans<br/>(<50ms Total)"]
        Alert["Caregiver SMS / WhatsApp<br/>(Itemized Receipt)"]
    end

    Workflow -->|Outbound PSTN Call| Vendor
    Vendor -->|Street Hindi/Hinglish Voice| Gemma
    Gemma -->|Structured JSON| Math
    Gemma -->|Extracted Commodities| TabPFN
    Ledger -->|30-Day Baselines| TabPFN
    TabPFN -->|Price Spikes & Overcharge ₹| Math
    Math -->|Receipt Summary| TTS
    TTS -->|Spoken Response| Vendor
    Math -->|Atomic Event| FastAPI
    FastAPI --> Simulator
    FastAPI --> Tracer
    FastAPI --> Alert
```

---

## ⚡ The AI Power Trio

### 1. Gemma 2 (2B / 9B) Open-Weight Dialect Extraction
- Extracts non-standard colloquial street Hindi & Hinglish (*"2 dabba sarson ka tel"*, *"subah mandi se 20 liter doodh"*).
- **Unbilled Ambiguity Protection**: If a supplier drops off samples or pending stock without immediate payment (*"bread de gaya bill kal aayega"*), Gemma safely records `cost = 0.0` to avoid artificial cash deficits.

### 2. TabPFN-3.5 Tabular Foundation Model (Prior Labs)
- Traditional models fail on micro-retailers who only buy commodities 2 to 3 times a week (15–30 historical rows).
- TabPFN performs *in-context Bayesian posterior inference* on the 30-day CSV ledger without retraining.
- Automatically flags price spikes $\ge 8\%$ above baseline and calculates exact overcharges (e.g., ₹950 vs ₹850 baseline = ₹200.90 loss on 2 cans).

### 3. Temporal Durable Workflows
- Real street stalls are noisy and chaotic; vendors frequently miss calls while serving customers.
- Orchestrates outbound calls with automatic retry backoffs (3 attempts, 15-minute intervals) and durable state persistence.

---

## 🚀 Quickstart & Installation

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/Snigdha-Mondal/HisaabDost.git
cd HisaabDost

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Key environment variables:
```ini
USE_LOCAL_GEMMA=false
GEMMA_API_KEY=""
TABPFN_API_KEY=""
TABPFN_ANOMALY_THRESHOLD_PCT=8.0
ELEVENLABS_API_KEY=""
TWILIO_ACCOUNT_SID=""
TWILIO_AUTH_TOKEN=""
SENTRY_DSN=""
```
*(Note: HisaabDost includes offline deterministic fallbacks and synthetic audio generators, allowing full offline testing with zero external API keys!)*

---

## 🧪 Testing & Verification

Run the entire test suite (Scaffolding, Schemas, Gemma Dialect Parser, TabPFN Anomaly Engine, Temporal Workflows, and FastAPI Endpoints):

```bash
python -m unittest discover tests
```
> **Result**: `Ran 35 tests in ~0.25s — OK (100% Passing)`

Run the telephony CLI simulator:
```bash
python scripts/mock_call.py --scenario 1
```

Run the Agent Skill verification test:
```bash
python skills/voice-ledger-audit/scripts/test_extraction.py
```

---

## 🌐 Caregiver Dashboard & Web Simulator

Start the FastAPI application:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser to `http://localhost:8000`:
- **Interactive Retro Button Phone**: Click the physical phone keypad, initiate simulated inbound/outbound calls, and test street speech scenarios.
- **Audio Waveform & Player**: Listen to synthesized ElevenLabs voice audio feedback in Hindi and English.
- **Live Auditing Terminal**: Watch Gemma entity extraction, TabPFN price gouging alerts, and Sentry sub-millisecond trace spans in real time.

---

## 📦 Agent Skill: `voice-ledger-audit`

Packaged under `skills/voice-ledger-audit/` following the open Agent Skills standard:
- [`SKILL.md`](skills/voice-ledger-audit/SKILL.md): Complete instructions and workflow rules for AI agents.
- [`references/street-dialects.md`](skills/voice-ledger-audit/references/street-dialects.md): Street glossary of 50+ units (*dabba*, *peti*, *paav*, *galla*) and idioms.
- [`references/tabpfn-auditing.md`](skills/voice-ledger-audit/references/tabpfn-auditing.md): Bayesian tabular anomaly scoring formulas.
- [`scripts/test_extraction.py`](skills/voice-ledger-audit/scripts/test_extraction.py): Autonomous verification script.

---

## 📝 Hacktoberfest 2026 Week 2 Submission

- **Challenge**: Hacktoberfest 2026 Week 2 Challenge ("Side Hustle")
- **Submission Article**: [`docs/challenge_submission.md`](docs/challenge_submission.md)
- **DevRelay Session Transcript**: [`devrelay/session_transcript.json`](devrelay/session_transcript.json)
- **Liquid Embed Tag**: `{% agent_session b773ad0e-2410-4b0e-89b8-f86b01c179e9 %}`

---

## 📄 License

This project is licensed under the **Apache-2.0 License** — see the [LICENSE](LICENSE) file for details.
