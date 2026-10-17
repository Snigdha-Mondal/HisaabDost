# HisaabDost (हिसाब दोस्त) — 3-Minute Video Demo & Pitch Script

> **Hackathon Track**: Hacktoberfest 2026 Week 2 Challenge ("Side Hustle")  
> **Theme**: Empowering roadside micro-vendors with zero-tech, voice-first bookkeeping & price-gouging defense.  
> **Target Duration**: Exactly 3 minutes (180 seconds).

---

## 🎬 Video Recording Checklist

Before starting recording:
1. Terminal 1: Launch FastAPI backend:
   ```bash
   python -m uvicorn app.main:app --port 8000 --reload
   ```
2. Browser: Open `http://localhost:8000` (or `demo.html`).
3. Audio: Check microphone and speaker output (ElevenLabs synthetic voice playback enabled).
4. Terminal 2: Ready to show `python scripts/mock_call.py` or test suite.

---

## ⏱️ Scene-by-Scene 3-Minute Pitch Script

### Scene 1: The Invisible Street Reality (0:00 – 0:35)
* **Visual**: Close-up of retro button phone interface in `demo.html`, or footage/image of a roadside chai stall.
* **Speaker**:
  > *"Every morning at 5:00 AM, millions of elderly micro-vendors across the Global South set up their roadside tea and food stalls. They work 14-hour days, handling pure cash. They don't have smartphones, accounting software, or digital literacy. Their only device is a basic $10 button phone.*
  >
  > *At the wholesale mandi, suppliers take advantage of this opacity. When cooking oil creeps up by ₹100 or milk goes up by ₹5, vendors rarely notice until their month-end cash is gone. They are silently price-gouged out of business.*
  >
  > *Meet **HisaabDost (हिसाब दोस्त)**—the world's first zero-tech, voice-first daily bookkeeper and wholesale price-gouging auditor."*

---

### Scene 2: The Zero-Tech Outbound Call (0:35 – 1:15)
* **Visual**: Click **"📞 Dial Simulated Call"** in `demo.html` with Scenario 1 (*Sharmaji Chai & Snacks - Cooking Oil Gouging*).
* **Speaker**:
  > *"Every evening at 8:30 PM closing time, HisaabDost calls the vendor's phone. No app to open, no typing required.*
  >
  > *(Play simulated audio prompt: 'Namaste Sharmaji! Aaj dukan ka hisaab batayein.')*
  >
  > *Sharmaji simply answers and speaks naturally in his daily street dialect:  
  > 'Haan beta, doodh liya tha 10 liter 600 rupay ka. Kisan traders se 2 dabba sarson ka tel liya 1900 ka. Mandi se sabzi aayi 450 ki. Total bikri 4200 hui hai.'*
  >
  > *Within seconds, HisaabDost parses the conversation, runs an instant audit, and speaks back in a warm, respectful elder-friendly voice."*

---

### Scene 3: The AI Power Trio Under the Hood (1:15 – 2:00)
* **Visual**: Highlight the live dashboard in `demo.html`—show the itemized receipt, the TabPFN Gouging Alert badge, and Sentry latency traces.
* **Speaker**:
  > *"Behind this simple phone call operates an advanced open-source AI pipeline:
  >
  > 1. **Gemma 2 (2B / 9B)** parses unstructured colloquial Hindi and Hinglish. It understands street measures like 'dabba', 'paav', and 'peti'. Crucially, if a vendor mentions a supplier left a sample without a bill, Gemma ignores the cost so false deficits aren't recorded.
  >
  > 2. **TabPFN-3.5 from Prior Labs**: Rather than naive hardcoded averages, TabPFN is a tabular foundation model that performs in-context Bayesian anomaly detection against the vendor's 30-day purchase history. Here, it instantly catches that ₹950/can for mustard oil is an 11.8% spike over his ₹849 baseline, computing an exact overcharge of ₹200.90!
  >
  > 3. **ElevenLabs Bilingual TTS**: Synthesizes warm, elder-friendly audio in Hindi and Hinglish, empowering Sharmaji with the exact number to contest at the mandi tomorrow morning."*

---

### Scene 4: Temporal Durable Resilience & Caregiver Guardrails (2:00 – 2:30)
* **Visual**: Switch to terminal showing Temporal workflow logs (`python -m unittest tests.test_temporal_workflow`) and caregiver SMS alert preview.
* **Speaker**:
  > *"Real street retail is messy. What if the line is busy or the vendor is serving a customer?
  >
  > We orchestrate every single call using **Temporal Python SDK**. If a call drops or returns busy, Temporal's durable saga schedules intelligent exponential retries without losing call state.
  >
  > Simultaneously, a clean SMS audit is dispatched to the vendor's tech-literate caregiver or son, giving the entire family financial transparency."*

---

### Scene 5: Scalable Micro-SaaS & Social Impact (2:30 – 3:00)
* **Visual**: Scroll through open-source GitHub repo, architecture diagram, and DevRelay session embed.
* **Speaker**:
  > *"By utilizing open-weight Gemma 2 and TabPFN in-context inference, our server cost is under $0.02 per closing call—enabling a sustainable $1.50/month micro-SaaS model that pays for itself on day one.
  >
  > HisaabDost transforms an ordinary button phone into a Wall Street-grade auditor for the people who keep our cities fed.
  >
  > The code, data, and reusable Agent Skill are 100% open source under Apache-2.0. Thank you!"*

---

## 🛠️ Step-by-Step Live Demo Runbook

If presenting live or recording screen capture:
```bash
# 1. Start the backend server
uvicorn app.main:app --port 8000

# 2. In another terminal, run the CLI verification
python scripts/mock_call.py --scenario 1

# 3. Run the full unit test suite (35/35 tests in <0.3s)
python -m unittest discover tests

# 4. Open http://localhost:8000 in your browser and toggle Scenarios 1 & 2
```
