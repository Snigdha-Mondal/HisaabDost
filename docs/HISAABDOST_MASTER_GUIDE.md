# HisaabDost (हिसाब दोस्त) — Master Guide

> **HisaabDost is the zero-tech, voice-first daily bookkeeper and price-gouging shield for roadside stalls and micro-food vendors.**
>
> An elderly street vendor with a $10 push-button phone simply speaks their daily expenses and cash sales into an automated phone call. HisaabDost converts informal street dialogue into structured accounting, audits supplier prices against historical data to catch overcharging, and speaks back in a warm, respectful human voice.

---

## 1. Project Overview

### The Problem

Across the world, millions of elderly vendors run roadside food carts, chai stalls, snack kiosks, fruit stands, and flower stalls. They do not own smartphones, have zero computer or internet literacy, and operate in grease-stained, chaotic environments where touchscreens and apps are impossible to use.

These micro-entrepreneurs face four silent profit-killers:

1. **Supplier Price Creep**: Wholesalers quietly raise prices on staples (cooking oil, milk, flour, vegetables) by 10–15% without notice. Elderly vendors don't spot the markup and wonder why their pockets are empty at month's end.
2. **Lost Customer Credit (*Udhar / Khata*)**: Regulars say *"Put it on my tab, I'll pay Friday."* Vendors lose paper scraps or forget who owes what.
3. **Double-Billing & Unchecked Delivery Slips**: Deliveries happen in morning rushes with greasy carbon-copy chits that get shoved into biscuit tins without reconciliation.
4. **Exhausting Nightly Calculations**: After standing 14 hours over a hot stove or roadside cart, doing mental arithmetic with fading eyesight leads to daily revenue miscalculations.

### The Solution

HisaabDost is an **automated telephony-based AI bookkeeper**:

1. At 8:30 PM closing time, the vendor's basic phone rings automatically (orchestrated by **Temporal**).
2. The vendor answers and talks naturally in everyday street language (*Hindi, Hinglish, or plain English*).
3. **Gemma 2** parses the colloquial speech into structured income and expense transactions.
4. **TabPFN-3.5** audits the day's unit prices against historical tabular records, spotting price hikes and anomalies.
5. **ElevenLabs** responds immediately over the phone line in a warm, patient, elderly-friendly voice with net profit and supplier price warnings.
6. **Tiger Data (pgvector) / MongoDB** updates their ledger history and customer credit balances without the vendor touching a single screen or keyboard.

### One-Line Pitch

> **HisaabDost pairs Gemma 2, TabPFN, and Temporal into an automated voice agent that lets elderly roadside vendors do complete daily bookkeeping and catch supplier price-gouging using nothing more than a 60-second call on a basic button phone.**

---

## 2. Why This Idea Is Different

Existing accounting and POS apps (QuickBooks, Khatabook, Vyapar) are built for smartphone-literate shop owners with clean screens and reliable WiFi. They fail completely at roadside carts.

| Typical POS / Khata App | HisaabDost |
|---|---|
| Requires smartphone, touchscreen & 4G/WiFi | Works on **any $10 button phone or landline** |
| Requires manual typing, navigation, and reading | **100% voice-driven** in natural street dialect |
| Passive record book (records numbers blindly) | **Active auditor** (detects price gouging & missing stock) |
| Uses cloud APIs that store private business data | Uses **open-weight Gemma 2**; vendor data stays private |
| Silently fails if an app crashes or session expires | **Durable Temporal workflows** handle retries and closing schedules |
| High monthly software subscription fee | Extremely low cost: runs open-weight models for fractions of a cent |

---

## 3. Target Users & Personas

### 3.1 The Elderly Roadside Vendor (Primary End User)
* **Demographics**: 50–70 years old, running a roadside tea stall, snack cart, or fruit/vegetable stall.
* **Tech Reality**: Uses a basic Nokia-style feature phone; hands are often wet, greasy, or covered in flour; declining eyesight.
* **Core Need**: Peace of mind that they aren't being cheated on milk or oil prices and knowing their true daily take-home profit.

### 3.2 The Adult Child / Family Supporter (The Buyer / Payer)
* **Demographics**: Son, daughter, or younger family member working an office job.
* **Core Need**: Anxious about aging parents being taken advantage of or exhausted by manual stall management.
* **Willingness to Pay**: Gladly pays a **$3 to $10/month** subscription to give their parent an automated bookkeeping assistant with nightly WhatsApp/SMS summaries.

### 3.3 The Neighborhood Micro-Bookkeeper (The Side Hustle Operator)
* **Demographics**: Local freelancer or student offering micro-business bookkeeping services to 10–20 neighborhood stalls.
* **Core Need**: A turnkey web agent where stalls call in daily, and the dashboard automatically flags fraud, prints weekly statements, and reconciles cash flows.

---

## 4. MVP Scope

### Must-Have Features

#### A. Telephony Inbound & Outbound Calling
- Inbound: Vendor presses Speed Dial 1 to report an expense or customer credit on the fly.
- Outbound: Automated 8:30 PM closing call scheduled and orchestrated via Temporal.
- Fallback: If line is busy (serving a customer), retry with exponential backoff.

#### B. Gemma 2 Colloquial Entity Extraction
- Converts natural, unscripted street speech into structured JSON:
  ```json
  {
    "call_type": "closing_summary",
    "expenses": [
      { "item": "milk", "quantity": 10, "unit": "liters", "total_cost": 600.0, "unit_price": 60.0 },
      { "item": "mustard oil", "quantity": 2, "unit": "cans", "total_cost": 1900.0, "unit_price": 950.0 },
      { "item": "vegetables", "quantity": 1, "unit": "basket", "total_cost": 450.0, "unit_price": 450.0 }
    ],
    "revenue": 4200.0,
    "calculated_profit": 1250.0,
    "unresolved_text": null
  }
  ```

#### C. TabPFN Anomaly & Price-Gouging Engine
- Maintains a historical CSV ledger: `[date, item_id, supplier_id, unit_price, quantity, total_amount]`.
- Compares today’s unit prices against the 30-day baseline.
- Flags any unit price spike greater than 8% over moving average.
- Output: Anomaly alert object passed back to the voice agent before replying.

#### D. ElevenLabs Voice Response
- Generates clear, warm, patient speech synthesized in Hindi or Indian-accented English.
- Script structure:
  1. *Acknowledgment*: "Namaste Uncle, everything has been recorded."
  2. *Daily Summary*: "Today's profit is 1,250 rupees after spending 2,950 on supplies."
  3. *Price Alert*: "Warning: Mustard oil was 950 per can today. Last week it was 850. You paid 200 rupees extra."

#### E. Durable Temporal Sagas
- `DailyClosingSchedule`: Triggers call at 8:30 PM local time.
- `CallRetryPolicy`: 3 retries with a 15-minute jitter if vendor is busy or unanswered.
- `GougingAlertSaga`: If an anomaly is severe (>20% price hike), dispatches an SMS alert to the son/daughter's smartphone.

---

## 5. The Role of Core Technologies

### Gemma 2 (Google Open-Weight Model)
- **Role**: Natural language understanding, colloquial dialect parsing, entity disambiguation.
- **Why Open Innovation Matters**:
  - Street speech contains heavy regional code-switching (Hinglish, local slang). Gemma 2 can be given tailored few-shot prompts with zero censorship or corporate filter interference.
  - Zero per-token cloud billing: running Gemma 2 locally or on a cheap self-hosted GPU keeps the marginal cost per call at fractions of a cent, making a $3/month subscription sustainable.

### TabPFN-3.5 (Prior Labs Tabular Foundation Model)
- **Role**: In-context tabular classification and price anomaly detection.
- **Why It's Essential**:
  - LLMs are notoriously bad at rigorous statistical numerical analysis on tabular data.
  - TabPFN accepts the historical CSV table directly and instantly infers whether a new price point is an outlier without needing heavy retraining or hours of hyperparameter tuning.

### Temporal (Durable Execution)
- **Role**: State machine, schedules, retries, and failure recovery.
- **Why It's Essential**:
  - Telephony is flaky: calls drop, stalls get crowded, networks glitch.
  - Temporal ensures no vendor's closing report is lost mid-flight. If the LLM or TTS service experiences latency, Temporal workflows resume seamlessly without double-charging or dropping state.

### Tiger Data (pgvector) / MongoDB Atlas
- **Role**: Database & semantic search.
- **Why It's Essential**:
  - Stores vendor profiles, supplier name mappings (*"Shyam Dairy"* vs *"Milk guy on bicycle"*), and historical transaction vectors.

---

## 6. High-Level Architecture

```text
 ┌────────────────────────────────────────────────────────┐
 │        Elderly Vendor (Basic Push-Button Phone)        │
 └───────────────────────────┬────────────────────────────┘
                             │
                  Standard Telephony (PSTN)
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │            Twilio / Telephony Gateway API              │
 └───────────────────────────┬────────────────────────────┘
                             │ Audio Stream / Webhook
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │          Temporal Durable Orchestrator ($100)          │
 │  - Schedules daily 8:30 PM call                        │
 │  - Manages retries if vendor is busy (15 min backoff)  │
 │  - Executes multi-step transaction saga                │
 └──────┬────────────────────┬────────────────────┬───────┘
        │                    │                    │
        ▼                    ▼                    ▼
 ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
 │   Gemma 2    │     │  TabPFN-3.5  │     │  Tiger Data  │
 │ Entity Parser│     │ Anomaly Core │     │   pgvector   │
 │   ($200)     │     │   ($200)     │     │   ($100)     │
 └──────┬───────┘     └──────┬───────┘     └──────────────┘
        │                    │
        └─────────┬──────────┘
                  ▼
 ┌────────────────────────────────────────────────────────┐
 │         ElevenLabs Voice Synthesis Engine ($100)       │
 │   Warm, patient, elder-friendly spoken feedback        │
 └────────────────────────┬───────────────────────────────┘
                          │
                          ▼
 ┌────────────────────────────────────────────────────────┐
 │        Sentry Agent Tracing & Observability ($100)     │
 │   Traces audio stream latency, token count, errors     │
 └────────────────────────────────────────────────────────┘
```

---

## 7. Recommended Project Structure

```text
hisaabdost/
├── README.md
├── LICENSE                         # Apache-2.0
├── pyproject.toml
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI server for Twilio webhooks
│   ├── config.py                   # Environment & model settings
│   ├── telephony/
│   │   ├── twilio_handler.py       # TwiML call setup & speech gather
│   │   └── voice_stream.py         # Audio streaming handler
│   ├── agent/
│   │   ├── gemma_parser.py         # Gemma 2 entity extraction
│   │   ├── prompts.py              # Few-shot prompts for street Hindi/English
│   │   └── schemas.py              # Pydantic transaction schemas
│   ├── audit/
│   │   ├── tabpfn_engine.py        # TabPFN price anomaly detector
│   │   └── ledger_manager.py       # CSV / Tabular history manager
│   ├── voice/
│   │   └── elevenlabs_client.py    # Spoken audio generation
│   ├── workflows/
│   │   ├── closing_workflow.py     # Temporal workflow definition
│   │   ├── activities.py           # Temporal activities (call, audit, notify)
│   │   └── worker.py               # Temporal worker process
│   └── database/
│       ├── tiger_client.py         # Tiger Data / pgvector connector
│       └── models.py               # Vendor, Transaction, Supplier models
├── skills/
│   └── voice-ledger-audit/
│       ├── SKILL.md                # Agent Skills Open Standard
│       ├── references/
│       │   └── street-dialects.md
│       └── scripts/
│           └── test_extraction.py
├── data/
│   ├── sample_history.csv          # 30-day baseline vendor transactions
│   └── sample_audio_transcripts.json
├── tests/
│   ├── test_gemma_parser.py
│   ├── test_tabpfn_anomaly.py
│   ├── test_temporal_workflow.py
│   └── test_telephony_mock.py
└── docs/
    ├── architecture.md
    └── challenge_submission.md
```

---

## 8. Agent Skill Package

To qualify for Open Standard Agent Skill standards, include `skills/voice-ledger-audit/SKILL.md`:

```markdown
---
name: voice-ledger-audit
description: Transcribes and structures informal spoken street food vendor dialogue into double-entry ledger records and performs tabular anomaly detection to catch wholesale supplier price gouging. Use when processing phone transcripts or audio logs from roadside micro-merchants.
license: Apache-2.0
compatibility: Requires Gemma 2 or open-weight LLM, TabPFN tabular model, and Temporal workflow harness.
metadata:
  author: HisaabDost Contributors
  version: "0.1.0"
---

# Voice Ledger Audit Skill

## Procedure

1. Ingest raw spoken text transcript from telephony bridge.
2. Identify language/dialect code-switching (Hindi, English, regional slang).
3. Extract financial entities: Item, Quantity, Unit, Total Price, and Transaction Type (Expense vs Revenue).
4. Compute derived unit prices for every commodity item.
5. Query historical price baseline via TabPFN tabular model.
6. Flag any item deviating by more than 8% above expected baseline.
7. Return structured JSON payload for voice generation.

## Hard Rules

- Never assume currency without locale confirmation (default: INR ₹ for Indian vendors).
- If vendor statement is ambiguous (e.g. "bought oil for 900" without specifying quantity), flag as `unresolved_quantity` rather than guessing.
- Always preserve vendor's raw verbal statement in the audit log for record integrity.
```

---

## 9. Gemma 2 Prompt Design

### System Prompt (`app/agent/prompts.py`)

```text
You are HisaabDost (हिसाब दोस्त), an expert accounting assistant for roadside food stalls and street vendors.
Your job is to listen to the vendor's informal spoken summary and extract precise financial figures into clean JSON.

Rules:
1. Vendors speak casually in Hindi, English, or Hinglish (e.g., "doodh", "tel", "tamatar", "chawal").
2. Standardize item names to English common names (e.g. "mustard oil", "milk", "potatoes").
3. Always calculate unit_price = total_cost / quantity when quantity is given.
4. Distinguish clearly between EXPENSES (money paid out for supplies) and REVENUE (money collected in cash/digital).
5. Calculate net_profit = total_revenue - total_expenses.
6. If an item price is unclear or missing, do NOT hallucinate; set "unresolved_text".
7. Return valid JSON only adhering strictly to the schema.
```

### Extraction Schema (`app/agent/schemas.py`)

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class ExpenseItem(BaseModel):
    item: str = Field(description="Normalized name of commodity or ingredient")
    raw_name: str = Field(description="Exact phrase spoken by vendor")
    quantity: float
    unit: str = Field(description="liters, kg, cans, packets, pieces")
    total_cost: float
    unit_price: float

class DailyAuditSummary(BaseModel):
    expenses: List[ExpenseItem]
    total_expenses: float
    revenue: float
    net_profit: float
    price_warnings: List[str] = []
    unresolved_text: Optional[str] = None
```

---

## 10. TabPFN Price-Gouging Anomaly Engine

TabPFN evaluates incoming unit prices against the vendor's historical purchases:

```python
# app/audit/tabpfn_engine.py
import pandas as pd
import numpy as np

def detect_price_anomaly(history_df: pd.DataFrame, new_item: str, unit_price: float) -> dict:
    """
    Uses TabPFN or historical statistical distribution to detect price gouging.
    """
    item_history = history_df[history_df['item'] == new_item]
    
    if len(item_history) < 3:
        return {"anomaly": False, "reason": "Insufficient history"}
        
    baseline_mean = item_history['unit_price'].mean()
    baseline_std = item_history['unit_price'].std() or 1.0
    
    pct_difference = ((unit_price - baseline_mean) / baseline_mean) * 100.0
    
    # Flag anything 8% or more above moving average
    if pct_difference >= 8.0:
        return {
            "anomaly": True,
            "baseline_price": round(baseline_mean, 2),
            "current_price": unit_price,
            "pct_increase": round(pct_difference, 1),
            "extra_cost": round(unit_price - baseline_mean, 2),
            "warning": f"{new_item} is {round(pct_difference, 1)}% higher than your past average of ₹{round(baseline_mean, 1)}"
        }
        
    return {"anomaly": False, "pct_difference": round(pct_difference, 1)}
```

---

## 11. Temporal Durable Workflow Design

Temporal ensures that if an elderly vendor is busy with a customer, the call is gracefully retried without losing the day's record.

### Workflow Code (`app/workflows/closing_workflow.py`)

```python
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from app.workflows.activities import (
        InitiateClosingCallActivity,
        ExecuteAuditActivity,
        SendCaregiverSummaryActivity
    )

@workflow.defn
class DailyClosingWorkflow:
    @workflow.run
    async def run(self, vendor_id: str, phone_number: str) -> str:
        # Step 1: Initiate call with 3 retries on busy/unanswered
        call_result = await workflow.execute_activity(
            InitiateClosingCallActivity,
            args=[vendor_id, phone_number],
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(minutes=10),
                backoff_coefficient=1.5
            )
        )
        
        if not call_result.get("completed"):
            # Escalate: notify family caregiver that call was missed
            await workflow.execute_activity(
                SendCaregiverSummaryActivity,
                args=[vendor_id, "MISSED_CLOSING_CALL"],
                start_to_close_timeout=timedelta(minutes=1)
            )
            return "Call missed after 3 retries"

        # Step 2: Run Gemma + TabPFN Audit
        audit_result = await workflow.execute_activity(
            ExecuteAuditActivity,
            args=[vendor_id, call_result["transcript"]],
            start_to_close_timeout=timedelta(minutes=2)
        )

        # Step 3: Send summary to caregiver/dashboard
        await workflow.execute_activity(
            SendCaregiverSummaryActivity,
            args=[vendor_id, audit_result],
            start_to_close_timeout=timedelta(minutes=1)
        )

        return "Daily reconciliation completed"
```

---

## 12. Testing Plan

### Unit Tests
- `test_gemma_parser.py`: Verifies Hinglish dialect parsing ("2 dabba tel", "dus liter doodh").
- `test_tabpfn_anomaly.py`: Injects 15% price spike on mustard oil and asserts anomaly flag triggers.
- `test_temporal_workflow.py`: Simulates telephone `busy` signal and verifies 15-minute retry execution.
- `test_telephony_mock.py`: Tests Twilio TwiML webhook generation and audio stream responses.

### Acceptance Criteria
1. Full workflow functions with zero smartphone or web UI dependency for the vendor.
2. Colloquial spoken quantities are accurately normalized to liters/kg/units.
3. Price anomalies over 8% produce an explicit spoken warning in the ElevenLabs audio stream.
4. Temporal recovers cleanly from network timeouts without dropping closing records.

---

## 13. Three-Minute Hackathon Demo Flow

Prepare this exact script for your DEV Challenge video demo:

* **0:00–0:35 — The Problem**:
  "This is a $10 button phone. It doesn't have an app store, internet, or a touchscreen. Over 100 million elderly street vendors run daily food stalls using this phone. Every week, they lose hard-earned profits to wholesale price creep and uncollected customer tabs because modern accounting software wasn't built for them. Meet **HisaabDost**."
* **0:35–1:20 — The Live Call**:
  - Show the basic phone ringing.
  - Put it on speaker. The warm ElevenLabs voice asks for the day's numbers.
  - You speak into the phone in Hindi/Hinglish: *"Beta, bought 10 liters of milk for 600, 2 cans of mustard oil for 1900, vegetables for 450. Total cash is 4200."*
* **1:20–2:10 — The AI Brain in Action**:
  - Show the backend console: **Gemma 2** parsing the speech into clean JSON.
  - Show **TabPFN** running on the historical CSV: highlighting that mustard oil jumped from ₹850 to ₹950 per can!
  - The phone speaks back immediately: *"Recorded, Uncle! Today's profit is 1,250 rupees. But warning: your oil vendor charged 100 rupees extra per can compared to last week."*
* **2:10–2:45 — The Temporal Architecture & Sponsors**:
  - Show the **Temporal** workflow UI: showing the durable scheduled timer, retry policies, and execution traces.
  - Show **Sentry** tracing latency and token usage.
* **2:45–3:00 — Why Open Innovation Matters**:
  - "With open-weight Gemma 2 and TabPFN, this service costs less than half a cent per call to operate. That means we can offer this to elderly street vendors for just $2 a month—turning a shoebox of forgotten debts into protected daily profit."

---

## 14. Hacktoberfest Challenge Fit & Prize Stacking

HisaabDost uniquely stacks **5 to 6 official challenge categories**:

1. **Best Use of Gemma ($200)**: Gemma 2 serves as the core linguistic and entity-extraction engine for colloquial street dialects.
2. **Best Use of TabPFN ($200)**: Prior Labs' tabular model directly audits the vendor's CSV purchase records for pricing anomalies.
3. **Best Use of Temporal ($100)**: Provides durable scheduling, retry backoff for busy street stalls, and multi-step closing sagas.
4. **Best Use of ElevenLabs ($100)**: Delivers an elder-accessible, warm, patient spoken telephone persona.
5. **Best Use of Tiger Data ($100)**: Manages vendor transaction embeddings and supplier catalog mappings.
6. **Best Use of Sentry ($100)**: End-to-end tracing across telephony audio buffers, LLM inference, and tabular evaluation.
7. **Best Open-Source AI Project & Overall ($250)**: Open-source repository with Apache-2.0 license, fully reproducible local demo, and reusable Agent Skill.

---

## 15. Seven-Day Build Plan

| Day | Goal | Deliverable |
|---|---|---|
| **Day 1** | Project Setup & Telephony Mock | Setup FastAPI + Mock Phone Call CLI simulator (`mock_call.py`) |
| **Day 2** | Gemma 2 Extraction Engine | Prompt engineering & Pydantic schema validation for Hinglish street dialogue |
| **Day 3** | TabPFN Anomaly Detection | Integrate TabPFN with historical CSV ledger to detect wholesale price spikes |
| **Day 4** | Temporal Workflow Harness | Implement `DailyClosingWorkflow` with retries, timeouts, and state persistence |
| **Day 5** | ElevenLabs Voice & Sentry | Connect TTS generation and drop in Sentry agent tracing SDK |
| **Day 6** | Testing, Audio Fixtures & Skill | Write unit tests, create synthetic audio samples, and package Agent Skill |
| **Day 7** | Video Demo & DEV Post | Record 3-minute video, capture Sentry/Temporal screenshots, and publish |

---

## 16. Final Judge Message

End your DEV Challenge submission article with this exact conviction:

> **“Most AI applications are built for people who already have the newest MacBook and the fastest 5G connection. HisaabDost was built for the 65-year-old grandmother frying samosas on the corner with a cracked button phone, making sure not a single rupee of her hard-earned profit is taken from her.”**
