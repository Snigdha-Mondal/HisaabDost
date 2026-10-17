#!/usr/bin/env python3
"""
HisaabDost (हिसाब दोस्त) — Telephony CLI Mock Simulator
Simulates the automated 8:30 PM closing phone call for developers & testing.
"""

import sys
import json
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.agent.gemma_parser import gemma_parser
from app.audit.tabpfn_engine import tabpfn_engine
from app.agent.schemas import DailyAuditSummary, ExpenseItem, GougingAlert, VendorProfile

def load_transcripts():
    transcript_file = BASE_DIR / "data" / "sample_audio_transcripts.json"
    if not transcript_file.exists():
        return []
    with open(transcript_file, "r", encoding="utf-8") as f:
        return json.load(f)

def run_simulation(spoken_text: str, vendor: VendorProfile) -> DailyAuditSummary:
    print("\n" + "=" * 70)
    print(f"📞 OUTBOUND CALL INITIATED BY TEMPORAL AT {vendor.daily_closing_time} IST")
    print(f"   Destination: {vendor.phone_number} ({vendor.stall_name})")
    print("=" * 70)
    print("🔔 Ringing... Ringing... [CALL ANSWERED]")
    print(f"🤖 ElevenLabs Audio: 'Namaste {vendor.vendor_name}! Aaj dukan ka hisaab batayein.'")
    print("-" * 70)
    print(f"🗣️  Vendor Speaks into Phone Microphone:")
    print(f"   \"{spoken_text}\"")
    print("-" * 70)

    # Step 1: Gemma 2 Entity Extraction
    print("⚡ Parsing with Gemma 2...")
    parsed_data = gemma_parser.parse_speech(spoken_text)

    expenses = [
        ExpenseItem(**exp_dict) for exp_dict in parsed_data.get("expenses", [])
    ]
    revenue = float(parsed_data.get("revenue", 0.0))

    # Step 2: TabPFN Price Anomaly Auditing
    print("📊 Auditing prices against 30-day baseline with TabPFN...")
    gouging_alerts = []
    for exp in expenses:
        audit_res = tabpfn_engine.audit_item_price(
            item_name=exp.item,
            unit_price=exp.unit_price,
            quantity=exp.quantity
        )
        if audit_res.get("anomaly"):
            gouging_alerts.append(GougingAlert(
                item=exp.item,
                raw_name=exp.raw_name,
                baseline_price=audit_res["baseline_price"],
                current_price=audit_res["current_price"],
                pct_increase=audit_res["pct_increase"],
                extra_cost=audit_res["extra_cost_total"],
                supplier="Kisan Traders",
                warning_message=audit_res["warning_message"]
            ))

    # Step 3: Compile Daily Audit Summary
    summary = DailyAuditSummary(
        call_id="CALL_SIM_830PM",
        vendor_name=vendor.stall_name,
        stall_id=vendor.stall_id,
        revenue=revenue,
        expenses=expenses,
        gouging_alerts=gouging_alerts,
        spoken_confirmation_en=(
            f"Namaste {vendor.vendor_name}, recorded! Today's sales were ₹{revenue:,.0f}, "
            f"expenses ₹{sum(e.total_cost for e in expenses):,.0f}, leaving ₹{revenue - sum(e.total_cost for e in expenses):,.0f} profit."
        ),
        spoken_confirmation_hi=(
            f"नमस्ते {vendor.vendor_name}, सब दर्ज हो गया। आज का मुनाफ़ा ₹{revenue - sum(e.total_cost for e in expenses):,.0f} है।"
        )
    )

    # Step 4: Display Visual Receipt
    print("\n" + "🧾" + " DAILY FINANCIAL RECEIPT ".center(68, "="))
    print(f" Stall: {summary.vendor_name} ({summary.stall_id})")
    print(f" Sales (बिक्री):     ₹{summary.revenue:>10,.2f}")
    print(f" Expenses (ख़र्चा):   ₹{summary.total_expenses:>10,.2f}")
    print(f" Net Profit (मुनाफ़ा): ₹{summary.net_profit:>10,.2f}  [Margin: {summary.profit_margin_pct}%]")
    print("-" * 70)
    print(" Itemized Ledger:")
    for e in summary.expenses:
        print(f"  • {e.item.title():<18} : {e.quantity:>4.1f} {e.unit:<7} @ ₹{e.unit_price:>7.2f} = ₹{e.total_cost:>8.2f}")

    if summary.gouging_alerts:
        print("\n" + "⚠️ " + " TABPFN WHOLESALE PRICE-GOUGING ALERT ".center(67, "!"))
        for g in summary.gouging_alerts:
            print(f"   {g.warning_message}")
            print(f"   -> Action: Automated alert sent to caregiver at {vendor.caregiver_phone}")
        print("!" * 70)
    else:
        print("\n✅ All unit prices match 30-day baseline historical ranges. No overcharging detected.")

    print("\n🔊 Spoken ElevenLabs Response over Phone:")
    print(f"   Hindi:   \"{summary.spoken_confirmation_hi}\"")
    print(f"   English: \"{summary.spoken_confirmation_en}\"")
    print("=" * 70)
    print("📞 Call successfully logged & terminated.\n")

    return summary

def main():
    parser = argparse.ArgumentParser(description="HisaabDost Telephony CLI Simulator")
    parser.add_argument("--transcript", "-t", type=str, default="sharmaji_closing_gouging", help="Scenario ID from sample transcripts")
    parser.add_argument("--speech", "-s", type=str, help="Custom spoken text string to test")
    parser.add_argument("--list", "-l", action="store_true", help="List all available sample scenarios")

    args = parser.parse_args()
    samples = load_transcripts()

    if args.list:
        print("\nAvailable Pre-Recorded Street Scenarios:")
        for idx, s in enumerate(samples, 1):
            print(f" {idx}. [{s['id']}] {s['vendor_name']}: {s['scenario']}")
        return

    vendor = VendorProfile()

    if args.speech:
        spoken_text = args.speech
    else:
        matched = next((s for s in samples if s["id"] == args.transcript), None)
        if matched:
            spoken_text = matched["spoken_text"]
        else:
            print(f"Scenario '{args.transcript}' not found. Using default scenario.")
            spoken_text = samples[0]["spoken_text"] if samples else "10 liter doodh 600 ka aur 2 dabba tel 1900 ka. Bikri 4200."

    run_simulation(spoken_text, vendor)

if __name__ == "__main__":
    main()
