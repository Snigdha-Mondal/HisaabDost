# HisaabDost — Master Guide

> **HisaabDost is the zero-tech, voice-first daily bookkeeper and wholesale price-gouging shield for roadside food stalls.**
>
> An elderly vendor with a $10 push-button phone simply speaks their daily expenses and cash sales into an automated phone call. HisaabDost converts informal street dialogue into structured accounting, audits supplier prices against historical data to catch overcharging, and speaks back in a warm, respectful human voice.

---

## 1. Project overview

### The problem

Across the world, millions of elderly vendors run roadside food carts, tea (*chai*) stalls, snack kiosks, fruit stands, and flower carts. They do not own smartphones, have zero computer or internet literacy, and operate in chaotic, grease-stained environments where touchscreens and apps are impossible to use.

Before closing each night, they face four silent profit-killers:

- **Supplier price creep:** Wholesalers quietly raise prices on staples (cooking oil, milk, vegetables, flour) by 10–15% without notice. Elderly vendors don't spot the markup and wonder why their profits vanished.
- **Lost customer credit (*Udhar / Khata*):** Regular neighborhood customers say *"Put it on my tab, I'll pay Friday."* Vendors lose paper scraps or forget who owes what.
- **Double-billing and unverified delivery chits:** Deliveries happen in morning rushes with greasy carbon-copy paper slips that get shoved into biscuit tins without reconciliation.
- **Exhausting mental arithmetic:** After standing 14 hours over a hot stove or roadside cart, doing calculations with fading eyesight leads to daily revenue miscalculations.

### The solution

HisaabDost is an **automated telephony-based AI bookkeeper and pricing shield**. At 8:30 PM closing time:

1. it automatically rings the vendor's basic push-button phone (orchestrated by **Temporal**);
2. the vendor speaks naturally in everyday street dialect (*Hindi, Hinglish, or English*);
3. **Gemma 2** parses the colloquial speech into structured income and expense line items;
4. **TabPFN-3.5** audits the day's unit prices against historical tabular records, spotting price hikes and anomalies;
5. **ElevenLabs** responds immediately over the phone line in a warm, patient, elderly-friendly voice with net profit and supplier price warnings;
6. **Tiger Data (pgvector)** updates their ledger history and customer credit balances without the vendor touching a single screen or keyboard.

### One-line pitch

> **HisaabDost pairs Gemma 2, TabPFN, and Temporal into an automated voice agent that lets elderly roadside vendors do complete daily bookkeeping and catch supplier price-gouging using nothing more than a 60-second call on a basic button phone.**

---

## 2. Why this idea is different

Existing accounting and POS apps (QuickBooks, Khatabook, Vyapar) are built for smartphone-literate shop owners with clean screens and reliable WiFi. They fail completely at roadside carts.

HisaabDost asks the opposite question first:

> **“How do we deliver world-class AI financial auditing to someone who has never touched a smartphone?”**

HisaabDost is not just an audio recorder or generic chatbot. It:

- operates through standard 8kHz voice calls on basic button phones;
- understands colloquial market language (*"2 dabba sarson tel", "10 liter doodh"*);
- separates entity extraction from deterministic accounting;
- uses a tabular foundation model (**TabPFN**) to spot price gouging;
- uses durable workflows (**Temporal**) so calls retry if the vendor is busy serving a customer;
- keeps the vendor's financial records private on dedicated open-weight infrastructure.

| Typical POS / Khata App | HisaabDost |
|---|---|
| Requires smartphone, touchscreen & 4G/WiFi | Works on **any $10 button phone or landline** |
| Requires manual typing, navigation, and reading | **100% voice-driven** in natural street dialect |
| Passive record book (records numbers blindly) | **Active auditor** (detects price gouging & missing stock) |
| Uses cloud APIs that store private business data | Uses **open-weight Gemma 2**; vendor data stays private |
| Silently fails if an app crashes or session expires | **Durable Temporal workflows** handle retries and closing schedules |
| High monthly software subscription fee | Extremely low cost: runs open-weight models for fractions of a cent |

---

## 3. Target users

For the first MVP, focus on three specific audiences:

### 3.1 The Elderly Roadside Vendor (Primary End User)

- tea and coffee stalls;
- roadside fried snack (*samosa, pakora, chaat*) carts;
- fruit and vegetable handcart vendors;
- small neighborhood kiosks and flower sellers.

### 3.2 The Adult Child / Family Caregiver (The Buyer)

- working sons, daughters, or relatives who worry about their aging parents being cheated;
- want daily visibility into stall earnings without micro-managing;
- receive an automated WhatsApp/SMS summary after every closing call.

### 3.3 The Neighborhood Micro-Bookkeeper (The Side Hustle Operator)

- local students or freelancers who manage finances for 10–20 neighborhood stalls;
- charge a small $10/month retainer per stall;
- use the HisaabDost web portal to review anomalies and print weekly summary sheets.

For the first demo, show three spoken inputs: a **morning wholesale supply purchase**, an **evening closing call with an oil price hike**, and a **customer credit (*udhar*) addition**.

---

## 4. MVP scope

### Must-have features

#### A. Telephony voice check-in

- Inbound: vendor presses Speed Dial 1 to report an expense on the fly;
- Outbound: automated 8:30 PM closing call scheduled and orchestrated via Temporal;
- Busy retry: if line is busy or unanswered, Temporal sleeps 15 minutes and retries up to 3 times.

#### B. Gemma 2 colloquial entity extraction

The first version should extract:

- expense line items (commodity name, raw spoken phrase, quantity, unit, total cost, derived unit price);
- revenue (cash collected in drawer, digital payments);
- customer credit entries (customer name, borrowed amount, repaid amount);
- ambiguous or unclear speech fragments flagged with uncertainty.

#### C. TabPFN price-gouging audit

Every purchase is audited against the vendor's historical 30-day baseline:

```json
{
  "item": "mustard_oil",
  "today_unit_price": 950.0,
  "historical_baseline": 850.0,
  "pct_spike": 11.7,
  "is_anomaly": true,
  "monetary_overcharge": 200.0,
  "reason": "Mustard oil is ₹100/can higher than your 30-day average of ₹850.",
  "recommended_action": "alert_vendor_and_caregiver"
}
```

#### D. ElevenLabs spoken response

- Clear, respectful, patient voice synthesized in Hindi / Indian-accented English;
- states net profit immediately;
- explicitly warns if supplier price gouging occurred;
- confirms total customer credit balance.

#### E. Caregiver alert dispatch

- If an anomaly exceeds 10% or overcharge exceeds ₹150, dispatches an automated SMS alert to the family caregiver's smartphone.

#### F. Financial safety notice

Always log:

> “HisaabDost calculations reflect vendor speech and historical tabular trends. Verify physical supplier chits before formal disputes.”

---

## 5. The role of Gemma 2 & TabPFN

Gemma 2 and TabPFN are not optional decorations. They form the twin-core cognitive architecture of the system.

### Use Gemma 2 for

- transcribing and parsing colloquial street dialect (Hinglish, Hindi, regional market slang);
- extracting financial entities from unstructured narratives (*"doodh liya che sau ka aur do dabba tel उन्नीस सौ"*);
- standardizing informal units (*"dabba"*, *"bora"*, *"potli"* $\rightarrow$ cans, sacks, packets, liters);
- separating revenue from expense statements;
- generating empathetic, natural spoken response phrasing;
- flagging ambiguous speech without hallucinating missing numbers.

### Use TabPFN for

- in-context tabular anomaly detection across multi-week purchase CSVs;
- identifying supplier price gouging without requiring expensive model retraining;
- detecting volume-pricing irregularities (e.g., paying higher unit cost for bulk orders);
- evaluating demand fluctuations to predict inventory spoilage risks.

### Use deterministic code for

Do not rely on an LLM for financial arithmetic or database operations.

Use code and rules for:

- exact arithmetic calculation (`net_profit = total_revenue - total_expenses`);
- unit price derivation (`unit_price = total_cost / quantity`);
- Temporal workflow state transitions and retry backoff timers;
- Twilio TwiML audio stream and webhook handling;
- database transactions and customer credit ledger updates.

### Core architecture principle

> **Gemma understands and structures; TabPFN audits tabular trends; deterministic code calculates profits.**

This separation guarantees zero arithmetic hallucinations.

---

## 6. High-level architecture

```text
┌──────────────────────────────────────┐
│  Elderly Vendor (Basic Button Phone) │
└──────────────────┬───────────────────┘
                   │ 8kHz PSTN Voice
                   v
┌──────────────────────────────────────┐
│       Twilio Telephony Gateway       │
└──────────────────┬───────────────────┘
                   │ Audio Stream / Webhook
                   v
┌──────────────────────────────────────┐
│      Temporal Workflow Engine        │  Durable schedules, 15m retry loops
└──────┬───────────┬───────────┬───────┘
       │           │           │
       v           v           v
┌──────────────┐ ┌───────────┐ ┌──────────────┐
│   Gemma 2    │ │TabPFN-3.5 │ │ Tiger Data   │
│ Entity Parser│ │Price Audit│ │  (pgvector)  │
└──────┬───────┘ └─────┬─────┘ └──────────────┘
       │               │
       └───────┬───────┘
               v
┌──────────────────────────────────────┐
│   ElevenLabs Voice Response Stream   │  Warm, patient, Hindi/English persona
└──────────────────┬───────────────────┘
                   │
                   v
┌──────────────────────────────────────┐
│  Caregiver SMS Alert / Web Dashboard │  Sentry agent tracing & observability
└──────────────────────────────────────┘
```

---

## 7. Recommended project structure

```text
HisaabDost/
├── README.md
├── LICENSE                         # Apache-2.0
├── pyproject.toml
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI entrypoint for telephony webhooks
│   ├── config.py                   # Settings, API keys, thresholds
│   ├── telephony/
│   │   ├── twilio_handler.py       # TwiML setup & speech gathering
│   │   └── voice_stream.py         # Audio buffer management
│   ├── agent/
│   │   ├── gemma_parser.py         # Gemma 2 entity extraction
│   │   ├── prompts.py              # Few-shot prompts for street dialects
│   │   └── schemas.py              # Pydantic schemas (ExpenseItem, AuditSummary)
│   ├── audit/
│   │   ├── tabpfn_engine.py        # TabPFN anomaly detection core
│   │   └── ledger_manager.py       # Historical CSV ledger updates
│   ├── voice/
│   │   └── elevenlabs_client.py    # Warm voice generation
│   ├── workflows/
│   │   ├── closing_workflow.py     # Temporal workflow definition
│   │   ├── activities.py           # Temporal activities (call, audit, SMS)
│   │   └── worker.py               # Temporal worker runner
│   └── database/
│       ├── tiger_client.py         # Tiger Data / pgvector connector
│       └── models.py               # Vendor, Ledger, and CustomerTab models
├── skills/
│   └── voice-ledger-audit/
│       ├── SKILL.md                # Agent Skills Open Standard
│       ├── references/
│       │   └── street-dialects.md
│       └── scripts/
│           └── test_extraction.py
├── tests/
│   ├── test_gemma_parser.py
│   ├── test_tabpfn_anomaly.py
│   ├── test_temporal_workflow.py
│   ├── test_telephony_mock.py
│   └── fixtures/
│       ├── sample_audio_transcripts.json
│       └── sample_30day_history.csv
├── docs/
│   ├── threat-model.md
│   ├── evaluation.md
│   └── architecture.md
└── demo/
    └── index.html                  # Interactive retro phone simulator
```

---

## 8. Agent Skill package

For the Best Open-Source AI Project category, include a reusable Agent Skill following the Open Standard:

### `skills/voice-ledger-audit/SKILL.md`

```markdown
---
name: voice-ledger-audit
description: Audits spoken financial statements and raw voice call transcripts from roadside vendors. Uses Gemma 2 to extract structured accounting line items and TabPFN to audit unit prices against historical CSV baselines to flag supplier price gouging.
license: Apache-2.0
compatibility: Requires Gemma 2 open-weight model, TabPFN tabular foundation model, and Temporal workflow harness. Designed for zero-tech voice telephony.
metadata:
  author: HisaabDost Contributors
  version: "0.1.0"
---

# Voice ledger audit skill

## Procedure

1. Ingest raw audio transcript from telephony gateway.
2. Identify colloquial market terms and dialect code-switching.
3. Extract commodity items, quantities, units, and total costs.
4. Calculate derived unit prices deterministically.
5. Query 30-day historical tabular data for each item.
6. Run TabPFN anomaly check to detect wholesale price spikes.
7. Return structured JSON with profit summary and price-gouging warnings.
8. Synthesize spoken response for the vendor over telephony.

## Hard rules

- Never guess an ambiguous quantity; flag as `unresolved_text`.
- Never use an LLM for profit arithmetic; calculate strictly in code.
- Always preserve the vendor's raw verbal statement in the audit log.
- Do not transmit vendor financial data to third-party closed clouds.

## Output

Return structured financial JSON, net profit, price anomaly flags, and spoken feedback string.
```

---

## 9. Gemma prompt design

The prompt requires structured evidence for every financial line item and strictly enforces JSON output.

### System prompt draft

```text
You are HisaabDost (हिसाब दोस्त), an expert accounting assistant for roadside food stalls.
Inspect the vendor's spoken transcript and extract only financial transactions that were explicitly stated.
Do not invent or assume missing quantities or prices.
Vendors speak informally in Hindi, Hinglish, or English (e.g. "doodh", "sarson tel", "tamatar", "biki").
Standardize item names to English common names (e.g. "milk", "mustard_oil", "vegetables").
Extract quantity, unit, and total cost.
Distinguish between EXPENSES (supplies bought) and REVENUE (cash collected in drawer).
If an item price is unclear or missing, do NOT guess; flag in "unresolved_text".
Return valid JSON only.
```

### Output schema

```json
{
  "call_type": "daily_closing|expense_report|credit_update",
  "expenses": [
    {
      "item": "mustard_oil",
      "raw_phrase": "2 dabba sarson tel 1900 ka",
      "quantity": 2.0,
      "unit": "cans",
      "total_cost": 1900.0,
      "unit_price": 950.0
    }
  ],
  "revenue": 4200.0,
  "credit_updates": [
    {
      "customer_name": "Ramesh",
      "amount": 45.0,
      "type": "credit_borrowed"
    }
  ],
  "unresolved_text": null,
  "requires_vendor_clarification": false
}
```

---

## 10. Risk & anomaly scoring

Use an explainable statistical anomaly score backed by TabPFN:

```text
anomaly_score = (today_unit_price - historical_mean) / historical_std
```

### Suggested sensitivity by commodity

| Commodity Category | High Sensitivity Threshold | Rationale |
|---|---:|---|
| Cooking oil & ghee | +8.0% | High cost staple; wholesalers frequently scalp on volume |
| Dairy & milk | +5.0% | Regulated daily commodity; sudden jumps indicate vendor overcharge |
| Fresh vegetables & produce | +15.0% | Highly seasonal; wider variance allowed before flagging |
| Commercial LPG / Gas | +3.0% | Fixed municipal rates; any jump indicates broker gouging |
| Spices & dry goods | +10.0% | Non-perishable wholesale goods |

---

## 11. Privacy-first & ethical product rules

### Zero-leakage financial privacy

- Street vendors operate in the informal economy; never share cash earnings or transaction data with tax authorities or third-party brokers;
- store purchase history locally or on self-hosted encrypted PostgreSQL;
- telemetry disabled by default; never log vendor phone numbers in error traces.

### Dignity & respect for elderly vendors

- The agent voice must always use respectful honorifics (*"Namaste Uncle"*, *"Aadab Chachaji"*);
- never scold or make the vendor feel foolish about a bad purchase; frame warnings as supplier scrutiny (*"Your supplier charged more than last week"*);
- speak at a measured, slightly slower pace suitable for noisy roadside environments.

---

## 12. Threat model

### What HisaabDost is designed to protect against

- unnoticed supplier price gouging and hidden inflation;
- uncollected customer tabs that slip the vendor's mind;
- double-billing on delivery chits during busy morning rushes;
- arithmetic mistakes after 14-hour physical workdays;
- lost records when paper slips are damaged by grease or rain.

### What HisaabDost does not guarantee

- legal tax compliance or audit certifications;
- physical prevention of supplier fraud;
- perfect transcription in deafening street environments (>90dB engine noise);
- recovery of cash stolen physically from the stall drawer.

---

## 13. Testing plan

### Unit tests

- Hinglish number parsing works (*"dedh sau"* $\rightarrow 150$, *"dhhai kilo"* $\rightarrow 2.5$);
- derived unit prices match exact division;
- TabPFN correctly triggers an anomaly on a 12% price hike;
- cold-start items with no history do not trigger false-positive warnings;
- Temporal retry policy backs off on telephone busy signal.

---

## 14. Evaluation benchmark

Create at least 30 synthetic test fixtures:

| Fixture group | Count |
|---|---:|
| Clean Hinglish closing reports | 8 |
| Heavy street background noise calls | 6 |
| Supplier price-gouging cases (>10% spike) | 6 |
| Ambiguous or incomplete statements | 4 |
| Pure customer credit updates (*Udhar*) | 4 |
| Extreme cold-start items (new commodities) | 2 |

---

## 15. Three-minute demo flow

### Demo setup

Prepare:

1. a $10 basic button phone (or the interactive `demo.html` browser simulator);
2. a pre-loaded 30-day baseline CSV showing mustard oil steady at ₹850;
3. a microphone to speak the sample Hindi closing statement.

### Presentation script

#### 0:00–0:35 — Problem

“This is a $10 button phone. Over 100 million elderly street vendors run daily food stalls using this phone. They have no touchscreens, no apps, and no spreadsheets. Every week, they lose hard-earned profits to wholesale price creep and uncollected customer credit because modern accounting tools weren’t built for them. Meet **HisaabDost**.”

#### 0:35–1:20 — The live phone call

- Show the phone ringing at 8:30 PM closing time;
- answer on speaker: ElevenLabs voice greets *"Namaste Uncle, closing time! What supplies did you buy today?"*;
- speak naturally into the phone: *"Maine 10 liter doodh 600 ka liya, 2 dabba sarson tel 1900 ka, aur sabzi 450 ki. Total galla 4200 hai."*

#### 1:20–2:10 — The AI brain in action

- Show the terminal: **Gemma 2** parsing colloquial speech into structured JSON in $<400$ms;
- show **TabPFN** running on the historical CSV: flagging that mustard oil jumped from ₹850 $\rightarrow$ ₹950 per can;
- the phone speaks back: *"Recorded Uncle! Today's net profit is ₹1,250. But warning: your oil supplier charged ₹100 extra per can today compared to last week."*

#### 2:10–2:45 — The Temporal & Sentry architecture

- Show the **Temporal** workflow web UI: displaying the scheduled closing timer, retry backoffs, and execution state;
- show **Sentry** agent tracing displaying end-to-end latency and token usage.

#### 2:45–3:00 — Why open innovation matters

- "Running open-weight Gemma 2 and TabPFN means this service costs less than half a cent per call to operate. We can offer full bookkeeping to vulnerable street vendors for just $2 a month—turning a shoebox of forgotten debts into protected daily profit."

---

## 16. GitHub README outline

Put these items on the first screen of the README:

```text
HisaabDost (हिसाब दोस्त)
The zero-tech voice bookkeeper & price-gouging shield for roadside food stalls.

[Live Demo] [Run Locally] [Apache-2.0] [Gemma 2] [TabPFN] [Temporal]

Problem
How it works
Why open innovation matters
Quick start
Architecture
Sponsor track alignment
Evaluation & benchmarks
Threat model
Limitations
License
```

---

## 17. GitHub publishing checklist

```bash
git init
git add .
git commit -m "feat: add voice-first bookkeeping agent for roadside stalls"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hisaabdost.git
git push -u origin main
```

---

## 18. Hacktoberfest challenge fit

HisaabDost uniquely stacks **5 to 6 official challenge categories**:

### Best Use of Gemma ($200)
Gemma 2 serves as the core linguistic and entity-extraction engine for colloquial street dialects.

### Best Use of TabPFN ($200)
Prior Labs' tabular foundation model directly audits the vendor's CSV purchase records for pricing anomalies.

### Best Use of Temporal ($100)
Temporal provides durable scheduling, retry backoff for busy street stalls, and multi-step closing sagas.

### Best Use of ElevenLabs ($100)
Delivers a patient, warm, respectful spoken persona tailored for elderly callers over standard telephony.

### Best Use of Tiger Data ($100)
Manages vendor transaction embeddings and supplier catalog mappings with pgvector.

### Best Use of Sentry ($100)
End-to-end agent tracing across telephony audio buffers, LLM inference, and tabular evaluation.

### Best Open-Source AI Project & Overall Winner ($250)
Open-source repository with Apache-2.0 license, fully reproducible local demo, and reusable Agent Skill.

---

## 19. Seven-day build plan

| Day | Goal | Deliverable |
|---|---|---|
| **Day 1** | Scaffolding & Mock Simulator | Setup FastAPI server, schemas, and `scripts/mock_call.py` CLI simulator |
| **Day 2** | Gemma 2 Extraction Engine | Prompt engineering & Pydantic schema validation for Hinglish street dialogue |
| **Day 3** | TabPFN Anomaly Detection | Integrate TabPFN with historical CSV ledger to detect wholesale price spikes |
| **Day 4** | Temporal Workflow Harness | Implement `DailyClosingWorkflow` with retries, timeouts, and state persistence |
| **Day 5** | ElevenLabs Voice & Sentry | Connect TTS generation and drop in Sentry agent tracing SDK |
| **Day 6** | Testing, Audio Fixtures & Skill | Write unit tests, create synthetic audio samples, and package Agent Skill |
| **Day 7** | Video Demo & DEV Post | Record 3-minute video, capture Sentry/Temporal screenshots, and publish |

---

## 20. Future roadmap

- **WhatsApp voice note bridge:** allow vendors with shared family smartphones to forward 10-second voice notes;
- **Regional language packs:** full dialect support for Tamil, Telugu, Marathi, and Bengali;
- **Visual chit OCR (PaliGemma):** optional camera scanning of crumpled handwritten slips for stalls with tech helpers;
- **Micro-loan creditworthiness scoring:** export certified 90-day cash flow records to help unbanked vendors secure low-interest microfinance loans;
- **Local air-gapped deployment:** run Gemma 2 quantized locally on a $35 Raspberry Pi or mini-PC at vendor cooperatives.

---

## 21. Common mistakes to avoid

### Mistake 1: Letting the LLM do arithmetic
Never ask Gemma to calculate net profit. Use Gemma to extract numbers; calculate `revenue - expenses` strictly in Python.

### Mistake 2: Requiring an app or smartphone
The moment you ask the elderly vendor to download an app or tap a screen, the project fails in reality. Keep it 100% voice on basic phones.

### Mistake 3: Cloud-first unit economics
A cloud API charging $0.05 per conversation turn destroys the margins of a $2/month micro-SaaS. Running open-weight Gemma 2 locally or on cheap VMs is mandatory for financial viability.

### Mistake 4: Disrespectful or patronizing voice tone
Elderly stall workers have decades of street wisdom. The voice persona must be respectful (*"Namaste Uncle"*), never pedantic.

---

## 22. Final judge message

End your DEV Challenge submission article with this exact conviction:

> **“Most AI applications are built for people who already have the newest MacBook and the fastest 5G connection. HisaabDost was built for the 65-year-old grandmother frying samosas on the corner with a cracked button phone, making sure not a single rupee of her hard-earned profit is taken from her.”**

---

## Official references

- [Hacktoberfest DEV Challenge Hub](https://dev.to/challenges/hf26)
- [Prior Labs TabPFN Documentation](https://platform.priorlabs.ai)
- [Temporal Python SDK Documentation](https://docs.temporal.io/develop/python)
- [Google Gemma 2 Documentation](https://ai.google.dev/gemma/docs)
- [Agent Skills Open Standard](https://agentskills.io/specification)
- [ElevenLabs API Documentation](https://elevenlabs.io/docs)

---

## Final recommendation

Do not present HisaabDost as a generic “expense tracker.” Present it as:

> **“The zero-tech voice bookkeeper and wholesale price-gouging shield for roadside stalls.”**
