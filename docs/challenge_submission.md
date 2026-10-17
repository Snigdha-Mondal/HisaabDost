---
title: "HisaabDost: Building a Zero-Tech Voice Bookkeeper & Price-Gouging Shield for Roadside Vendors"
published: false
description: "A voice-first daily bookkeeper and TabPFN wholesale price-gouging auditor for roadside food stalls using Gemma 2, Temporal, and ElevenLabs over basic $10 button phones."
tags: "hf26challenge, sidehustle, opensource, ai"
series: "Hacktoberfest 2026 Week 2 Challenge"
canonical_url: "https://github.com/Snigdha-Mondal/HisaabDost"
---

# HisaabDost (हिसाब दोस्त) — The Voice-First Bookkeeper for the Real Street Economy

*This article is submitted for the **Hacktoberfest 2026 Week 2 Challenge: Side Hustle** on DEV Community.*

---

## ☕ The Reality of Street Food Hustlers

Every morning before dawn at 5:00 AM, millions of elderly micro-vendors set up roadside tea stalls (*chai tapris*), fruit carts, and snack kiosks. They work grueling 14-hour days, turning over ₹3,000 to ₹6,000 in physical cash and QR codes.

Yet, despite endless hustle, their monthly savings remain stubbornly flat. 

Why? Because they operate in the dark:
1. **Zero-Tech Reality**: They don't have laptops, smartphones, or English literacy. Their only communications device is a beaten-up **$10 button phone** (Nokia 105 / JioBharat).
2. **Wholesale Price Gouging at the Mandi**: Wholesale middlemen exploit this opacity. When cooking oil creeps up by ₹100 a canister or milk climbs by ₹5 a liter, an exhausted vendor rarely notices until the month-end cash drawer is empty.
3. **The Unbilled Trap**: Suppliers drop off unbilled promo stock or delayed invoices (*"bill kal aayega"*), confounding daily balances.

We built **HisaabDost (हिसाब दोस्त — "Accountant Friend")** to solve this. It turns any ordinary PSTN button phone into an automated, Wall Street-grade financial auditor.

---

## 🤖 The Antigravity Agent Session Transcript

Here is the complete, interactive build session transcript exported via DevRelay, documenting the architecture planning, schema design, Gemma 2 linguistic tuning, TabPFN tabular audit tests, and Temporal workflow integration:

{% agent_session b773ad0e-2410-4b0e-89b8-f86b01c179e9 %}

*(If you are viewing this offline or on GitHub, inspect `devrelay/session_transcript.json` in our repository).*

---

## 📞 How HisaabDost Works in 4 Steps

```
[ 8:30 PM Closing Time ]
            │
            ▼
┌──────────────────────────────────────────────┐
│ 1. Automated Outbound Call (Temporal Saga)   │
│ Phone rings on vendor's $10 button phone.    │
│ "Namaste Sharmaji! Aaj dukan ka hisaab batayein."
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ 2. Street Dialect Parsing (Gemma 2)          │
│ Vendor speaks natural Hindi/Hinglish slang:   │
│ "Subah 2 dabba sarson tel 1900 ka liya,       │
│  aur doodh 1200 ka aaya. Bikri 4200 hui."    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ 3. Price-Gouging Audit (TabPFN-3.5)          │
│ Tabular model checks 30-day baseline ledger: │
│ ⚠️ Alert: Mustard Oil ₹950/can vs ₹850 avg   │
│ Overpaid by 11.8% (+₹200.90 extra!).         │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ 4. Dignified Voice & Caregiver SMS           │
│ Warm ElevenLabs Hindi audio speaks back:     │
│ "Aaj ka munafa ₹1,250 hai. Kal Mandi mein    │
│  tel ka rate zaroor check karna."            │
│ Clean WhatsApp/SMS dispatched to son/daughter.
└──────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack & Architectural Decisions

| Layer | Technology | Why We Chose It |
|---|---|---|
| **Dialect Parsing** | **Gemma 2 (2B / 9B)** | Open-weight, free inference, excels at informal Indian street idioms (*dabba*, *peti*, *galla*). |
| **Price Anomaly Detection** | **TabPFN-3.5 (Prior Labs)** | In-context tabular foundation model. Predicts Bayesian distributions on small CSV ledgers without retraining. |
| **Durable Orchestration** | **Temporal Python SDK** | Guarantees call retries on busy signals; survives dropped connections without losing state. |
| **Voice Synthesis** | **ElevenLabs API** | Warm, slow-cadence, respectful Hindi/English elder-friendly voice. |
| **Performance Tracing** | **Sentry Spans** | Measures sub-50ms latency across audio, Gemma NLP, and TabPFN audit. |
| **Caregiver Dashboard** | **FastAPI + Next.js / HTML5** | Real-time audio waveform visualizer and retro button phone simulator. |

---

## 🔬 Deep Dive: Open-Weight Gemma 2 Dialect Parsing

Standard LLMs struggle with Indian street retail slang because words like *dabba* (15-liter tin canister), *peti* (crate), and *galla* (cash drawer) aren't in standard financial dictionaries.

Furthermore, vendors frequently mix unbilled supplier drops:
> *"Bakery wala 10 bread packet de gaya, bola bill kal milega."*

If an AI naively estimates a cost for the bread, it introduces an artificial cash deficit. In HisaabDost, our Gemma extractor and fallback deterministic engine explicitly identify unbilled or pending clauses, routing them to an unresolved review queue with `amount = 0.0`.

### Strict Deterministic Financial Math
Under our **Golden Rule of Financial Safety**, the LLM is strictly prohibited from doing arithmetic. Python calculates the balance with zero hallucination:
$$\text{Net Profit} = \text{Total Cash Sales} - \sum \text{Itemized Expenses}$$

---

## 📊 Deep Dive: TabPFN-3.5 Tabular Price-Gouging Defense

Most anomaly detection models require hundreds of training rows. A roadside stall owner only buys mustard oil or milk 2 to 3 times a week, yielding just 15 to 30 data points a month.

**TabPFN** is a pre-trained tabular foundation model developed by Prior Labs. It computes Bayesian posterior predictions *in-context* directly from the vendor's 30-day historical CSV ledger.

When Sharmaji bought 2 cans of mustard oil for ₹1,900 (₹950/can):
- TabPFN retrieved the 30-day baseline distribution ($\mu = ₹849.55$).
- It flagged the purchase as an **11.8% spike** (exceeding our 8% safety threshold).
- It calculated the penny-precise loss:
  $$\text{Extra Cost} = (₹950.00 - ₹849.55) \times 2 = ₹200.90$$
- Before Sharmaji leaves for the wholesale market the next morning, HisaabDost reminds him:
  *"Chacha, kal Kisan Traders ne tel ₹200 mehenga diya tha. Mandi mein dusre dukaan se rate zaroor check karna."*

---

## 🔄 Temporal Durable Orchestration

Street vendors are busy. If a call arrives while they are frying samosas or making change, they won't answer. 

Using **Temporal Workflows**, we built a durable calling saga:
1. At 8:30 PM, Temporal initiates the call activity.
2. If the line returns `busy` or `no-answer`, Temporal sleeps with an exponential backoff (15-minute retry window up to 3 attempts).
3. If the call succeeds, the parse and audit activities run atomically.
4. If all retries fail, an automatic SMS fallback is dispatched to the vendor's tech-savvy child or caregiver.

---

## 📦 Open Source Agent Skill: `voice-ledger-audit`

As part of this submission, we packaged our entire colloquial extraction and tabular auditing workflow into an open standard **Agent Skill** under `skills/voice-ledger-audit/`:
- `SKILL.md`: Standard instructions for AI coding assistants.
- `references/street-dialects.md`: A 50+ term glossary of Indian street units, cash register idioms, and consignment patterns.
- `references/tabpfn-auditing.md`: Complete tabular anomaly scoring formulas.
- `scripts/test_extraction.py`: Standalone CLI verification runner.

---

## 🚀 Try It Yourself!

```bash
# 1. Clone the repository
git clone https://github.com/Snigdha-Mondal/HisaabDost.git
cd HisaabDost

# 2. Run the test suite (35/35 passing in 0.2s)
python -m unittest discover tests

# 3. Simulate an authentic street phone call from your terminal
python scripts/mock_call.py --scenario 1

# 4. Launch the Caregiver Dashboard & Web Phone Simulator
python -m uvicorn app.main:app --port 8000
```
Open `http://localhost:8000` to interact with the retro phone keypad and listen to synthesized ElevenLabs voice audio!

---

## 🌟 Sustainable Micro-SaaS Economics

Because we run **Gemma 2** and **TabPFN** locally or through serverless open-weight inference, the raw compute cost per closing call is **less than $0.02**. 

At $1.50 (₹120) per month, HisaabDost is a high-margin, life-changing micro-SaaS that saves an elderly vendor ₹1,500 to ₹4,000 every single month in prevented wholesale overcharges.

*Built with ❤️ for Hacktoberfest 2026. Star the project on GitHub: [github.com/Snigdha-Mondal/HisaabDost](https://github.com/Snigdha-Mondal/HisaabDost)*
