from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator

class ExpenseItem(BaseModel):
    """
    Represents an itemized inventory or supply expense parsed from vendor speech.
    """
    item: str = Field(description="Normalized English name of commodity or ingredient")
    raw_name: str = Field(description="Exact phrase or colloquial word spoken by vendor")
    quantity: float = Field(gt=0.0, description="Quantity of items purchased")
    unit: str = Field(description="Unit of measurement (liters, kg, cans, packets, pieces, basket)")
    total_cost: float = Field(ge=0.0, description="Total amount paid in INR")
    unit_price: float = Field(ge=0.0, description="Derived unit price (total_cost / quantity)")

    @model_validator(mode="before")
    @classmethod
    def compute_unit_price(cls, values: Any) -> Any:
        if isinstance(values, dict):
            qty = values.get("quantity")
            cost = values.get("total_cost")
            if qty and cost is not None and "unit_price" not in values:
                try:
                    q_val = float(qty)
                    values["unit_price"] = round(float(cost) / q_val, 2) if q_val > 0 else 0.0
                except (ValueError, ZeroDivisionError):
                    values["unit_price"] = 0.0
        return values

class VendorProfile(BaseModel):
    """
    Vendor identity, stall metadata, and contact configuration.
    """
    vendor_id: str = Field(default="VEND_001", description="Unique identifier for the micro-merchant")
    vendor_name: str = Field(default="Sharmaji", description="Name of the vendor")
    stall_id: str = Field(default="STALL_004", description="Stall code or license")
    stall_name: str = Field(default="Sharmaji Chai & Snacks", description="Commercial trade name")
    phone_number: str = Field(default="+919876543210", description="Vendor's basic PSTN phone number")
    caregiver_phone: Optional[str] = Field(default="+919811122233", description="Child / caregiver phone for SMS alerts")
    language: str = Field(default="hi", description="Primary dialect ('hi', 'hinglish', 'en')")
    daily_closing_time: str = Field(default="20:30", description="Local closing time for automated check-in")
    currency: str = Field(default="INR", description="Operational currency code")

class CustomerCreditItem(BaseModel):
    """
    Records an entry in the vendor's credit ledger (Udhar / Khata).
    """
    customer_name: str = Field(description="Name or nickname of customer")
    amount: float = Field(ge=0.0, description="Credit amount added or cleared in INR")
    action: str = Field(default="add", description="'add' (new credit) or 'settle' (paid back)")
    days_unpaid: int = Field(default=0, ge=0, description="Days outstanding")
    note: Optional[str] = Field(default=None, description="Optional context (e.g. 'mechanic', 'auto driver')")

class GougingAlert(BaseModel):
    """
    Alert generated when TabPFN flags an anomalous price hike.
    """
    item: str = Field(description="Commodity flagged for price spike")
    raw_name: Optional[str] = Field(default=None, description="Spoken commodity term")
    baseline_price: float = Field(description="Historical moving average unit price")
    current_price: float = Field(description="Today's unit price charged by supplier")
    pct_increase: float = Field(description="Percentage spike above historical baseline")
    extra_cost: float = Field(description="Extra amount overpaid across purchased quantity")
    supplier: Optional[str] = Field(default="Wholesale Supplier", description="Wholesaler name")
    warning_message: str = Field(description="Elderly-friendly explanation of overcharge")

class DailyAuditSummary(BaseModel):
    """
    Complete daily financial reconciliation and audit outcome.
    """
    call_id: Optional[str] = Field(default="CALL_DEMO", description="Unique identifier for telephony session")
    vendor_name: str = Field(default="Sharmaji Chai & Snacks", description="Vendor name")
    stall_id: str = Field(default="STALL_004", description="Stall code")
    revenue: float = Field(ge=0.0, description="Total cash and digital sales recorded")
    expenses: List[ExpenseItem] = Field(default_factory=list, description="Itemized expense entries")
    total_expenses: float = Field(ge=0.0, description="Sum of all supply expenses")
    net_profit: float = Field(description="Calculated take-home profit (revenue - expenses)")
    profit_margin_pct: float = Field(description="Net profit percentage (net_profit / revenue * 100)")
    gouging_alerts: List[GougingAlert] = Field(default_factory=list, description="List of price anomaly alerts")
    spoken_confirmation_en: str = Field(default="", description="Warm English confirmation for ElevenLabs voice output")
    spoken_confirmation_hi: str = Field(default="", description="Warm Hindi confirmation for telephone speaker")
    unresolved_text: Optional[str] = Field(default=None, description="Any portion of speech that could not be parsed")

    @model_validator(mode="before")
    @classmethod
    def compute_totals(cls, values: Any) -> Any:
        if isinstance(values, dict):
            expenses = values.get("expenses", [])
            tot_exp = sum(
                e.get("total_cost", 0.0) if isinstance(e, dict) else getattr(e, "total_cost", 0.0)
                for e in expenses
            )
            values["total_expenses"] = round(tot_exp, 2)
            rev = float(values.get("revenue", 0.0))
            profit = rev - tot_exp
            values["net_profit"] = round(profit, 2)
            values["profit_margin_pct"] = round((profit / rev * 100.0), 1) if rev > 0 else 0.0
        return values

class CallSimulationRequest(BaseModel):
    transcript_id: Optional[str] = None
    custom_speech: Optional[str] = None
    stall_id: Optional[str] = "STALL_004"
    language: Optional[str] = "en"  # "en" for English, "hi" for Hindi

class CallSimulationResponse(BaseModel):
    status: str
    transcript: str
    audit: DailyAuditSummary
    audio_stream_url: Optional[str] = None
