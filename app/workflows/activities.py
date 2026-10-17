import logging
from typing import Dict, Any, Optional
from datetime import datetime
from app.agent.gemma_parser import gemma_parser
from app.audit.tabpfn_engine import tabpfn_engine
from app.audit.ledger_manager import ledger_manager
from app.agent.schemas import DailyAuditSummary, ExpenseItem, GougingAlert

logger = logging.getLogger(__name__)

class CallPlacementException(Exception):
    """Raised when phone line is busy or unanswered, signaling Temporal to retry with backoff."""
    pass

async def initiate_closing_call_activity(
    vendor_id: str,
    phone_number: str,
    simulated_status: str = "completed",
    transcript: Optional[str] = None
) -> Dict[str, Any]:
    """
    Temporal Activity 1: Initiates the automated outbound phone call to the vendor.
    """
    logger.info(f"Temporal Activity: Initiating 8:30 PM closing call to {phone_number} for vendor {vendor_id}")

    if simulated_status in ("busy", "no-answer"):
        logger.warning(f"Phone line {phone_number} returned '{simulated_status}' signal.")
        raise CallPlacementException(f"Call attempt failed: line is {simulated_status}")

    default_speech = (
        "Haan beta, aaj ka hisaab likh lo. Doodh liya tha 10 liter 600 rupay ka. "
        "Kisan traders se 2 dabba sarson ka tel liya 1900 ka. "
        "Aur Mandi se sabzi aayi thi 450 ki. "
        "Din bhar mein gullak aur scanner mila ke total 4200 rupay ki bikri hui hai."
    )

    return {
        "completed": True,
        "call_id": f"CALL_{vendor_id}_{int(datetime.now().timestamp())}",
        "vendor_id": vendor_id,
        "phone_number": phone_number,
        "status": "completed",
        "transcript": transcript or default_speech
    }

async def execute_audit_activity(vendor_id: str, transcript: str) -> Dict[str, Any]:
    """
    Temporal Activity 2: Executes Gemma 2 extraction and TabPFN price audit on the phone transcript.
    """
    logger.info(f"Temporal Activity: Auditing speech transcript for vendor {vendor_id}")
    parsed = gemma_parser.parse_speech(transcript)

    expenses = [
        ExpenseItem(**e) for e in parsed.get("expenses", [])
    ]
    revenue = float(parsed.get("revenue", 0.0))

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

    summary = DailyAuditSummary(
        call_id=f"CALL_AUDIT_{vendor_id}",
        vendor_name="Sharmaji Chai & Snacks",
        stall_id="STALL_004",
        revenue=revenue,
        expenses=expenses,
        gouging_alerts=gouging_alerts,
        spoken_confirmation_en=(
            f"Namaste, recorded! Today's sales were ₹{revenue:,.0f}, "
            f"expenses ₹{sum(e.total_cost for e in expenses):,.0f}, leaving ₹{revenue - sum(e.total_cost for e in expenses):,.0f} profit."
        ),
        spoken_confirmation_hi=(
            f"नमस्ते, सब दर्ज हो गया। आज का मुनाफ़ा ₹{revenue - sum(e.total_cost for e in expenses):,.0f} है।"
        ),
        unresolved_text=parsed.get("unresolved_text")
    )

    return summary.model_dump()

async def send_caregiver_summary_activity(
    vendor_id: str,
    audit_data: Any,
    caregiver_phone: str = "+919811122233"
) -> Dict[str, Any]:
    """
    Temporal Activity 3: Dispatches SMS or WhatsApp alerts to the family caregiver.
    """
    logger.info(f"Temporal Activity: Sending summary to caregiver at {caregiver_phone}")

    if audit_data == "MISSED_CLOSING_CALL":
        message = (
            f"[HisaabDost Alert] Your parent at stall {vendor_id} could not be reached "
            f"after 3 call attempts. Please check in on them."
        )
        status = "MISSED_CALL_NOTIFICATION_SENT"
    else:
        profit = audit_data.get("net_profit", 0.0) if isinstance(audit_data, dict) else 0.0
        alerts = audit_data.get("gouging_alerts", []) if isinstance(audit_data, dict) else []

        if alerts:
            gouging_items = ", ".join(f"{a['item']} (+{a['pct_increase']}%)" for a in alerts)
            message = (
                f"[HisaabDost Alert] Today's Profit: ₹{profit:,.0f}. "
                f"⚠️ PRICE GOUGING DETECTED: {gouging_items}. Overpaid: ₹{sum(a['extra_cost'] for a in alerts):,.0f}."
            )
            status = "GOUGING_ALERT_SMS_DISPATCHED"
        else:
            message = f"[HisaabDost Summary] Today's Profit: ₹{profit:,.0f}. All supplier prices healthy."
            status = "DAILY_SUMMARY_SMS_DISPATCHED"

    return {
        "status": status,
        "caregiver_phone": caregiver_phone,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
