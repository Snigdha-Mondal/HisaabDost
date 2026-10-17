"""Verification test script for the voice-ledger-audit Agent Skill.

Tests:
1. Colloquial street transcript parsing (Hindi/Hinglish).
2. Unbilled sample & deferred delivery guardrails (unresolved_text capture).
3. TabPFN price gouging anomaly detection against historical ledger.
4. Deterministic financial arithmetic.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app.agent.gemma_parser import GemmaParser
from app.audit.tabpfn_engine import TabPFNEngine
from app.audit.ledger_manager import LedgerManager

def run_skill_verification() -> bool:
    print("=" * 60)
    print("  HisaabDost — voice-ledger-audit Skill Verification")
    print("=" * 60)

    parser = GemmaParser()
    history_csv = root_dir / "data" / "sample_history.csv"
    manager = LedgerManager(csv_path=history_csv)
    engine = TabPFNEngine(manager=manager)

    # Test Case 1: Street slang with price gouging
    transcript_1 = (
        "Bhaiya aaj galle mein 4200 rupaye the. "
        "Subah mandi se 2 dabba sarson ka tel 1900 mein liya, "
        "aur 20 liter doodh 1200 rupaye ka aaya."
    )
    print(f"\n[Test 1] Parsing transcript:\n  '{transcript_1}'")
    parsed_1 = parser.parse_speech(transcript_1)

    print(f"  -> Total Revenue Extracted: ₹{parsed_1['revenue']}")
    print(f"  -> Total Expenses: ₹{parsed_1['total_expenses']}")
    print(f"  -> Net Profit: ₹{parsed_1['net_profit']}")
    print(f"  -> Expense Items ({len(parsed_1['expenses'])}):")
    for exp in parsed_1["expenses"]:
        print(f"     - {exp['item']} ({exp['raw_name']}): {exp['quantity']} {exp['unit']} @ ₹{exp['total_cost']} (Unit: ₹{exp['unit_price']:.2f})")

    assert parsed_1["revenue"] == 4200.0, f"Expected revenue 4200.0, got {parsed_1['revenue']}"
    assert len(parsed_1["expenses"]) >= 2, f"Expected at least 2 expenses, got {len(parsed_1['expenses'])}"
    assert parsed_1["net_profit"] == parsed_1["revenue"] - parsed_1["total_expenses"], "Deterministic profit math violated!"

    # Audit expenses with TabPFN engine
    anomalies = []
    print("\n  -> Auditing with TabPFN Engine:")
    for exp in parsed_1["expenses"]:
        res = engine.audit_item_price(exp["item"], exp["unit_price"], exp["quantity"])
        if res.get("anomaly"):
            anomalies.append(res)
            print(
                f"     ⚠️ [GOUGING ALERT] {res['item']}: Paid ₹{res['current_price']:.2f} "
                f"vs Baseline ₹{res['baseline_price']:.2f} (+{res['pct_increase']}%). "
                f"Extra Overcharge: ₹{res['extra_cost_total']:.2f}"
            )
        else:
            print(f"     ✅ [FAIR PRICE] {res['item']}: Paid ₹{res['current_price']:.2f} (Within normal baseline range)")

    assert len(anomalies) > 0, "Expected at least 1 price gouging alert for cooking oil!"

    # Test Case 2: Ambiguity and unbilled delivery protection
    transcript_2 = (
        "Aaj galle mein 3500 rupaye the. Dudh 20 liter 1200 ka aaya, "
        "lekin bakery wala 10 bread packet de gaya uska bill kal milega."
    )
    print(f"\n[Test 2] Testing unbilled delivery guardrail:\n  '{transcript_2}'")
    parsed_2 = parser.parse_speech(transcript_2)

    print(f"  -> Revenue: ₹{parsed_2['revenue']}")
    print(f"  -> Expenses Recorded: {len(parsed_2['expenses'])}")
    print(f"  -> Ambiguous / Pending Clause: '{parsed_2.get('unresolved_text')}'")

    assert parsed_2.get("unresolved_text") is not None, "Expected unbilled clause to be captured!"
    # Ensure unbilled bread did NOT add false cash deductions
    bread_expenses = [e for e in parsed_2["expenses"] if "bread" in e["item"].lower()]
    assert len(bread_expenses) == 0, "Unbilled delivery must not be counted as cash expense!"

    print("\n" + "=" * 60)
    print("  🎉 [SUCCESS] All voice-ledger-audit skill tests passed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = run_skill_verification()
    sys.exit(0 if success else 1)
