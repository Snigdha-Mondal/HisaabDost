import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import settings
from app.agent.schemas import (
    CallSimulationRequest,
    CallSimulationResponse,
    DailyAuditSummary,
    ExpenseItem,
    GougingAlert,
    CustomerCreditItem,
    VendorProfile
)
from app.agent.gemma_parser import gemma_parser
from app.audit.tabpfn_engine import tabpfn_engine
from app.audit.ledger_manager import ledger_manager
from app.voice.elevenlabs_client import elevenlabs_client
from app.telephony.sentry_tracer import tracer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="HisaabDost (हिसाब दोस्त)",
    description="Zero-tech, voice-first daily bookkeeper and wholesale price-gouging shield for roadside food stalls.",
    version=settings.VERSION
)

# Enable CORS for browser simulator
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Mock Customer Credit (Udhar) database
SAMPLE_UDHAR = [
    {"customer_name": "Ramesh (Mechanic)", "amount": 110.0, "days_unpaid": 3, "action": "add", "note": "Morning tea & bun maska"},
    {"customer_name": "Sharmaji (Tailor)", "amount": 65.0, "days_unpaid": 1, "action": "settle", "note": "Special masala chai"},
    {"customer_name": "Suresh (Autodriver)", "amount": 240.0, "days_unpaid": 7, "action": "add", "note": "Weekly evening snacks (Overdue)"}
]

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "HisaabDost",
        "version": settings.VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }

@app.get("/api/scenarios")
def list_scenarios():
    """
    Returns pre-recorded street vendor audio scenarios.
    """
    transcript_file = BASE_DIR / "data" / "sample_audio_transcripts.json"
    if not transcript_file.exists():
        return []
    with open(transcript_file, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/api/ledger")
def get_historical_ledger():
    """
    Returns the 30-day baseline historical purchase ledger.
    """
    records = ledger_manager.load_all_records()
    commodities = ["milk", "mustard oil", "tea leaves", "sugar", "vegetables", "commercial gas"]
    stats = {c: ledger_manager.get_stats(c) for c in commodities}
    return {
        "total_records": len(records),
        "commodity_stats": stats,
        "recent_purchases": records[-15:]
    }

@app.get("/api/udhar")
def get_customer_credit():
    """
    Returns customer credit tabs (उधार खाता).
    """
    return {
        "total_outstanding": sum(c["amount"] for c in SAMPLE_UDHAR),
        "accounts": SAMPLE_UDHAR
    }

@app.post("/api/call/simulate", response_model=CallSimulationResponse)
def simulate_phone_call(req: CallSimulationRequest):
    """
    Simulates an 8:30 PM vendor phone call end-to-end:
      1. Sentry trace initiation
      2. Gemma 2 entity extraction
      3. TabPFN price gouging audit
      4. ElevenLabs voice synthesis
    """
    with tracer.trace_span("telephony.simulate", f"Simulate call for stall {req.stall_id}"):
        spoken_text = req.custom_speech

        # If a scenario ID was provided, resolve spoken text
        if not spoken_text and req.transcript_id:
            scenarios = list_scenarios()
            matched = next((s for s in scenarios if s["id"] == req.transcript_id), None)
            if matched:
                spoken_text = matched["spoken_text"]

        if not spoken_text:
            scenarios = list_scenarios()
            spoken_text = scenarios[0]["spoken_text"] if scenarios else (
                "Haan beta, doodh liya 10 liter 600 ka aur 2 dabba sarson ka tel 1900 ka. Bikri 4200."
            )

        # Step 1: Gemma 2 Entity Extraction
        with tracer.trace_span("gemma.extraction", "Extract entities from spoken dialect"):
            parsed_data = gemma_parser.parse_speech(spoken_text)

        expenses = [
            ExpenseItem(**e) for e in parsed_data.get("expenses", [])
        ]
        revenue = float(parsed_data.get("revenue", 0.0))

        # Step 2: TabPFN Price Anomaly Audit
        with tracer.trace_span("tabpfn.audit", "Audit prices against 30-day baseline"):
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

        # Step 3: Compile Financial Summary
        tot_exp = sum(e.total_cost for e in expenses)
        profit = revenue - tot_exp
        spoken_en = (
            f"Namaste Uncle, recorded! Today's sales were ₹{revenue:,.0f}, "
            f"expenses ₹{tot_exp:,.0f}, leaving ₹{profit:,.0f} net profit."
        )
        spoken_hi = f"नमस्ते शर्माजी, सब दर्ज हो गया। आज का मुनाफ़ा ₹{profit:,.0f} है।"
        if gouging_alerts:
            first_alert = gouging_alerts[0]
            spoken_en += f" Warning: {first_alert.item.title()} was ₹{first_alert.extra_cost:,.0f} extra."
            spoken_hi += f" चेतावनी: {first_alert.item} पर ₹{first_alert.extra_cost:,.0f} ज़्यादा लिए गए।"

        summary = DailyAuditSummary(
            call_id=f"CALL_WEB_{req.stall_id}",
            vendor_name="Sharmaji Chai & Snacks",
            stall_id=req.stall_id or "STALL_004",
            revenue=revenue,
            expenses=expenses,
            gouging_alerts=gouging_alerts,
            spoken_confirmation_en=spoken_en,
            spoken_confirmation_hi=spoken_hi,
            unresolved_text=parsed_data.get("unresolved_text")
        )

        # Step 4: ElevenLabs Voice Synthesis
        with tracer.trace_span("elevenlabs.tts", "Synthesize audio response"):
            voice_res = elevenlabs_client.synthesize(spoken_hi, language="hi")

        return CallSimulationResponse(
            status="completed",
            transcript=spoken_text,
            audit=summary,
            audio_stream_url=voice_res.get("audio_data_uri")
        )

class SynthesizeRequest(BaseModel):
    text: str
    language: str = "hi"

@app.post("/api/voice/synthesize")
def synthesize_voice(req: SynthesizeRequest):
    return elevenlabs_client.synthesize(req.text, language=req.language)

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """
    Serves the interactive HisaabDost Web Dashboard & Phone Simulator.
    """
    demo_file = BASE_DIR / "demo.html"
    if not demo_file.exists():
        demo_file = BASE_DIR / "docs" / "demo.html"

    if demo_file.exists():
        return HTMLResponse(content=demo_file.read_text(encoding="utf-8"))

    return HTMLResponse("<h1>HisaabDost API is Running</h1>")
