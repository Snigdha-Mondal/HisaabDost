# HisaabDost (हिसाब दोस्त) — Frontend UI/UX Design Specification (`design.md`)

> **Document Scope**: Frontend Architecture, UI/UX Design System, Component Hierarchy, User Journeys, and Interactive Telephony Simulator.  
> **Target Framework**: Next.js 14 (App Router) / React, Tailwind CSS, Framer Motion, Lucide Icons, Recharts.  
> **Design Theme**: *"Dukaan & Chai"* — Warm, trustworthy, high-contrast, accessible, and grounded in Indian street commerce.

---

## 1. UI/UX Vision & Core Purpose

While the elderly vendor experiences HisaabDost purely through **voice on a basic phone**, the frontend web application serves three critical purposes:

1. **The Interactive Hackathon Demo & Telephony Simulator**: Allows judges, reviewers, and developers to simulate a live phone call directly in the browser (mic in, audio out, live waveform, real-time Gemma parsing, and TabPFN anomaly detection).
2. **The Family / Caregiver Dashboard**: An ultra-clean, high-contrast dashboard where the vendor's son, daughter, or helper can review daily profits, verify supplier receipts, and inspect price-gouging alerts.
3. **The Micro-Bookkeeper Multi-Stall Manager**: A portal to switch between multiple stalls (e.g., *"Sharmaji Chai Stall"*, *"Ramesh Fruit Cart"*) with weekly exportable summaries.

---

## 2. Design System & Brand Identity

### 2.1 Color Palette

The color system draws inspiration from authentic street food stalls—brass chai kettles, terracotta cups, fresh mint, and traditional red ledger cloth (*Bahi-Khata*):

| Token | Hex Code | Role / Usage |
|---|---|---|
| **Chai Amber** | `#D97706` (`amber-600`) | Primary brand accent, active phone call buttons, warm highlights |
| **Bahi Saffron** | `#F59E0B` (`amber-500`) | Secondary brand accent, warning states, hover accents |
| **Galla Green** | `#10B981` (`emerald-500`) | Positive net profit, healthy price trends, call connected |
| **Khatra Red** | `#EF4444` (`red-500`) | Price-gouging alert, high expense spike, missed call state |
| **Slate Charcoal** | `#0F172A` (`slate-900`) | Deep neutral background, header bars, card containers |
| **Card Surface** | `#1E293B` (`slate-800`) | Elevated card surfaces, modal dialogs, phone casing |
| **Muted Cream** | `#F8FAFC` (`slate-50`) | Primary high-contrast typography, crisp numbers |
| **Subtle Stone** | `#94A3B8` (`slate-400`) | Secondary metadata, timestamps, Hindi subtitle translations |

### 2.2 Typography

* **Headings & Numbers**: `Inter` / `Plus Jakarta Sans` — bold, tabular numbers (`font-mono` for currency) so daily profit figures stand out crisply.
* **Devanagari / Hindi**: `Noto Sans Devanagari` — clean, legibly rendered script for dual-language labels (*हिसाब, मुनाफ़ा, ख़र्चा*).

---

## 3. Screen Architecture & User Flows

The web application is structured into four primary views:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Top Navigation Bar                              │
│  [Logo: HisaabDost]   [Stall Selector: Sharmaji Chai]   [Lang: HI/EN] │
└────────────────────────────────────────────────────────────────────────┘
┌───────────────────────────────────┬────────────────────────────────────┐
│   Left Pane: Telephony Simulator  │    Right Pane: Live Audit Dashboard│
│                                   │                                    │
│   ┌───────────────────────────┐   │   ┌────────────────────────────┐   │
│   │   Retro Phone Interface   │   │   │ Today's Financial Cards    │   │
│   │   - Dialpad / Speed Dial  │   │   │ Revenue | Expenses | Profit│   │
│   │   - Live Call Status      │   │   └────────────────────────────┘   │
│   │   - Audio Waveform Viz    │   │   ┌────────────────────────────┐   │
│   │   - Mic Audio Input       │   │   │ TabPFN Price Gouging Alert │   │
│   └───────────────────────────┘   │   │ (Mustard Oil +11.7% spike) │   │
│   ┌───────────────────────────┐   │   └────────────────────────────┘   │
│   │   Live Speech Transcript  │   │   ┌────────────────────────────┐   │
│   │   Raw audio -> Gemma JSON │   │   │ Itemized Expense Ledger    │   │
│   └───────────────────────────┘   │   │ Milk | Oil | Vegetables    │   │
│                                   │   └────────────────────────────┘   │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 4. Component Hierarchy & Wireframes

### 4.1 Component 1: The Interactive Phone Simulator (`PhoneSimulator.tsx`)

Designed like a retro feature phone so judges immediately grasp the zero-smartphone reality:

```text
┌───────────────────────────────┐
│       NOKIA 3310 CHASSIS      │
│  ┌─────────────────────────┐  │
│  │ 🟢 CONNECTED (00:42)    │  │
│  │ "Speaking with Gemma..." │  │
│  │  ▂▃▅▆▇▆▅▃▂ (Waveform)   │  │
│  └─────────────────────────┘  │
│                               │
│  [ Speed Dial: 1 (Hisab) ]    │
│  [ 🟢 Call ]   [ 🔴 End ]     │
│                               │
│  ┌───┬───┬───┐                │
│  │ 1 │ 2 │ 3 │                │
│  ├───┼───┼───┤                │
│  │ 4 │ 5 │ 6 │  Audio Toggle: │
│  ├───┼───┼───┤  [🎙️ Use Mic]  │
│  │ 7 │ 8 │ 9 │  [▶️ Play Demo]│
│  ├───┼───┼───┤                │
│  │ * │ 0 │ # │                │
│  └───┴───┴───┘                │
└───────────────────────────────┘
```

* **Interactive States**:
  * `IDLE`: Screen displays time and *"Press Speed Dial 1 to start check-in"*.
  * `CALLING`: Dial-tone plays, screen pulses amber (*"Connecting to HisaabDost..."*).
  * `LISTENING`: Green pulsing audio visualizer; records vendor's voice via Web Audio API.
  * `AUDITING`: Spinner with text *"Gemma parsing & TabPFN analyzing prices..."*.
  * `SPEAKING`: Speaker animation with synthesized ElevenLabs voice output.

---

### 4.2 Component 2: Live Metrics Cards (`MetricsCards.tsx`)

Three bold summary cards displayed prominently at the top of the dashboard:

```text
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│ DAILY REVENUE (बिक्री)│ │ TOTAL EXPENSES (ख़र्चा)│ │ NET PROFIT (मुनाफ़ा) │
│ ₹4,200.00            │ │ ₹2,950.00            │ │ ₹1,250.00            │
│ ↑ 12% vs last week   │ │ 3 supply purchases   │ │ 🟢 Healthy Margin    │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

* **Card Highlights**:
  * **Net Profit** features dynamic color shifts:
    * `emerald-500` (healthy margin > 25%).
    * `amber-500` (low margin 10–25%).
    * `red-500` (loss / negative take-home).

---

### 4.3 Component 3: The TabPFN Price-Gouging Alert Banner (`GougingAlertBanner.tsx`)

When TabPFN detects an anomalous price spike, this banner animates onto the screen:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ ⚠️ SUPPLIER PRICE GOUGING DETECTED (दाम में हेरफेर)                    │
│                                                                        │
│ Item: Mustard Oil (सरसों का तेल)                                        │
│ Today's Price:  ₹950 / can                                             │
│ 30-Day Average: ₹850 / can                                             │
│ Discrepancy:    +11.7% (+₹200 paid on 2 cans)                          │
│                                                                        │
│ [ 📊 View Price History ]   [ 📱 Send SMS to Son ]   [ Dismiss ]       │
└────────────────────────────────────────────────────────────────────────┘
```

* **Micro-interaction**:
  * Clicking *"View Price History"* expands an inline mini-chart (**Recharts**) showing the 30-day baseline line with today's red spike plotted above it.

---

### 4.4 Component 4: Live Transcript & Parser Inspector (`TranscriptInspector.tsx`)

Shows judges the exact transformation from informal speech to structured JSON:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 🎙️ Raw Spoken Audio (Audio -> Text)                                   │
│ "Maine 10 liter doodh 600 ka liya, aur 2 dabba tel 1900 ka..."        │
├────────────────────────────────────────────────────────────────────────┤
│ ⚡ Gemma 2 Extracted Entities (Structured Ledger)                      │
│ {                                                                      │
│   "expenses": [                                                        │
│     { "item": "milk", "qty": 10, "unit": "liters", "cost": 600 },      │
│     { "item": "mustard oil", "qty": 2, "unit": "cans", "cost": 1900 }  │
│   ],                                                                   │
│   "revenue": 4200                                                      │
│ }                                                                      │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 4.5 Component 5: Customer Credit Ledger (*Udhar / Khata*) (`CustomerTabs.tsx`)

Simple tabbed drawer listing neighborhood credit accounts:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 📖 Customer Credit Book (उधार खाता)                                    │
├───────────────────────┬──────────────┬──────────────┬──────────────────┤
│ Customer Name         │ Pending Debt │ Days Unpaid  │ Action           │
├───────────────────────┼──────────────┼──────────────┼──────────────────┤
│ Ramesh (Mechanic)     │ ₹110.00      │ 3 days       │ [ Send SMS Rem ] │
│ Sharmaji (Tailor)     │ ₹65.00       │ 1 day        │ [ Settle Cash ]  │
│ Suresh (Autodriver)   │ ₹240.00      │ 7 days ⚠️    │ [ Send SMS Rem ] │
└───────────────────────┴──────────────┴──────────────┴──────────────────┘
```

---

## 5. Responsive Design & Accessibility (a11y)

1. **Large Touch Targets**: Minimum button sizes of 48px $\times$ 48px to accommodate clumsy touch interactions.
2. **High Contrast Ratios**: Dark slate backgrounds (`#0F172A`) paired with bright chalk text (`#F8FAFC`) exceed WCAG AAA requirements (7:1 contrast ratio).
3. **Bilingual Dual-Text Labels**: Key accounting terms are rendered in both English and Hindi:
   * *Sales (बिक्री)*
   * *Expenses (ख़र्चा)*
   * *Net Profit (मुनाफ़ा)*
   * *Customer Debt (उधार)*
4. **Responsive Breakpoints**:
   * **Mobile (< 768px)**: Stacked single-column view. Phone simulator sits in a floating bottom sheet.
   * **Desktop ($\ge$ 1024px)**: Side-by-side split screen (Phone Simulator on the left, Real-time Dashboard on the right).

---

## 6. Frontend Tech Stack & Libraries

* **Framework**: Next.js 14 (App Router)
* **Styling**: Tailwind CSS + `@tailwindcss/typography`
* **Icons**: `lucide-react` (PhoneCall, TrendingUp, AlertTriangle, ShieldCheck, IndianRupee)
* **Animations**: `framer-motion` (for smooth waveform pulses and card transitions)
* **Charts**: `recharts` (for 30-day price trend lines)
* **Audio Playback**: Web Audio API / HTML5 Audio (to stream ElevenLabs demo audio directly in-browser)

---

## 7. Demo Flow Walkthrough (The User Experience)

1. **User Opens Web App**: Welcomed by the split screen showing Sharmaji's Chai Stall.
2. **User Clicks "Call StallVoice" (or presses 1 on the virtual phone)**:
   * The virtual phone screen illuminates and rings.
   * Audio plays: *"Namaste Uncle, closing time! What supplies did you buy today?"*
3. **User Speaks or Clicks "Play Sample Voice"**:
   * The audio waveform dances on the virtual phone screen.
   * The live transcript displays: *"Bought 10 liters milk for 600, 2 cans oil for 1900..."*
4. **The Audit Executes (< 800ms)**:
   * Financial metric cards update with real-time numbers.
   * The crimson **TabPFN Price Gouging Banner** slides in with sound: *"Warning: Mustard oil was ₹100 extra per can."*
5. **The Spoken Confirmation**:
   * The virtual phone's speaker plays the ElevenLabs voice reassuring the vendor and warning them about the oil supplier.
