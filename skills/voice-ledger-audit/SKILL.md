---
name: voice-ledger-audit
description: >-
  Extract colloquial street-vendor voice logs into structured financial ledger items,
  perform deterministic arithmetic calculations, and detect wholesale price-gouging anomalies
  using TabPFN foundation models.
---

# Voice Ledger Audit Skill (हिसाब दोस्त)

The `voice-ledger-audit` skill equips agents to act as trustworthy, voice-first bookkeepers and price-gouging auditors for informal micro-vendors (tea stalls, fruit carts, food kiosks). It addresses the linguistic nuances of colloquial Hindi/Hinglish street speech, enforces deterministic financial balance arithmetic, and runs tabular in-context anomaly detection against historical wholesale prices.

---

## 1. When to Use This Skill

Activate this skill when:
- Parsing spoken or transcribed voice records from informal micro-retailers containing colloquial units (e.g., *dabba*, *peti*, *galla*, *paav*).
- Extracting mixed financial statements with daily cash sales, direct operational expenses, and informal customer credit (*udhaari*).
- Filtering out unbilled or sample supplier deliveries that must NOT be counted as immediate cash outflows.
- Auditing commodity purchases against a vendor's historical wholesale purchase ledger to flag price creep (>8% deviation).
- Generating respectful, elder-friendly spoken and SMS audit summaries in Hindi or Hinglish.

---

## 2. Core Operational Workflow

```
[Spoken Audio / Transcript]
            │
            ▼
┌──────────────────────────────────────────────┐
│ Step 1: Colloquial Linguistic Extraction     │
│ (Gemma 2 Open-Weight LLM / Offline Lexicon)   │
│ - Parse Hindi/Hinglish slang                 │
│ - Identify unbilled items & skip cost       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ Step 2: Deterministic Financial Arithmetic   │
│ (Strict Python Math - Never LLM Math)        │
│ - Cash in Galla = Total Sales                │
│ - Total Expenses = Sum(Expense Items)        │
│ - Net Profit = Total Sales - Total Expenses  │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ Step 3: TabPFN In-Context Gouging Audit      │
│ (Tabular Foundation Model / Ledger History)   │
│ - Compare unit price with 30-day baseline   │
│ - Flag anomalies > 8% over distribution      │
│ - Compute exact rupee overcharge             │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ Step 4: Dignified Spoken & SMS Response      │
│ (ElevenLabs TTS & Structured Receipt)        │
│ - Respectful tone (Chacha / Kaka / Didi)     │
│ - Actionable alert for next market run       │
└──────────────────────────────────────────────┘
```

---

## 3. Colloquial Street Glossary

Refer to [`references/street-dialects.md`](./references/street-dialects.md) for the full glossary. Key mappings include:

| Street Term | Meaning | Standard Unit | Category |
|---|---|---|---|
| *galla* / *gallay mein* | Cash register drawer | Currency (₹) | Sales Revenue |
| *dabba* | Tin / can (oil, ghee) | 15 kg / 15 L | Expense Unit |
| *peti* | Box / crate (fruits, eggs) | Crate / box | Expense Unit |
| *paav* | Quarter (250g) | 0.25 kg | Expense Unit |
| *aadha kilo* | Half kilogram | 0.5 kg | Expense Unit |
| *kharcha* | Out-of-pocket expense | Currency (₹) | Expense |
| *udhaari* / *baaki* | Customer credit balance | Currency (₹) | Receivable |
| *sample deke gaya* | Unbilled promo delivery | Zero ₹ (flagged) | Inventory Note |
| *kal aayega bill* | Delayed supplier invoice | Zero ₹ (flagged) | Unbilled Delivery |

---

## 4. Rule-Based Guardrails

1. **Unbilled Ambiguity Protection**:
   - If a vendor mentions an item delivered without cost (e.g., *"supplier bread chhod gaya, bill kal aayega"*), set `amount = 0.0` and mark `notes = "Unbilled delivery - pending invoice"`. **Never guess or impute an expense amount.**
2. **Deterministic Arithmetic**:
   - The LLM must **never** compute net profit or total balances. Financial math must be executed using Python's `Decimal` or strict rounded floating-point logic:
     $$\text{Net Profit} = \text{Total Cash Sales} - \sum \text{Expenses}$$
3. **8% Gouging Threshold**:
   - An expense is flagged as a gouging anomaly if:
     $$\frac{\text{Unit Price} - \mu_{\text{baseline}}}{\mu_{\text{baseline}}} > 0.08$$
   - The extra rupee cost is computed exactly as:
     $$\text{Overcharge} = (\text{Unit Price} - \mu_{\text{baseline}}) \times \text{Quantity}$$
4. **Tone of Voice**:
   - Always address the vendor with family honorifics (*Chacha-ji*, *Bhaiya*, *Didi*).
   - Never sound accusatory or robotic; speak with warmth, patience, and clear actionable guidance.

---

## 5. Execution Reference Scripts

- To test transcript extraction against colloquial test cases:
  ```bash
  python skills/voice-ledger-audit/scripts/test_extraction.py
  ```
- To inspect tabular anomaly rules:
  See [`references/tabpfn-auditing.md`](./references/tabpfn-auditing.md).
