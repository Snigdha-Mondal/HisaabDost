from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ExpenseItem(BaseModel):
    item: str = Field(description="Normalized name of commodity or ingredient in English")
    raw_name: str = Field(description="Exact phrase or colloquial word spoken by vendor")
    quantity: float = Field(ge=0.0, description="Quantity of items purchased")
    unit: str = Field(description="Unit of measurement (liters, kg, cans, packets, pieces, basket)")
    total_cost: float = Field(ge=0.0, description="Total amount paid in INR")
    unit_price: float = Field(ge=0.0, description="Derived unit price (total_cost / quantity)")

class CustomerCreditItem(BaseModel):
    customer_name: str = Field(description="Name or nickname of customer")
    amount: float = Field(ge=0.0, description="Credit amount added or cleared")
    action: str = Field(description="'add' or 'settle'")
    note: Optional[str] = None

class GougingAlert(BaseModel):
    item: str = Field(description="Commodity flagged for price spike")
    raw_name: Optional[str] = None
    baseline_price: float = Field(description="Historical moving average unit price")
    current_price: float = Field(description="Today's unit price charged by supplier")
    pct_increase: float = Field(description="Percentage spike above historical baseline")
    extra_cost: float = Field(description="Extra amount overpaid across the purchased quantity")
    supplier: Optional[str] = "Wholesale Supplier"
    warning_message: str = Field(description="Elderly-friendly explanation of the overcharge")

class DailyAuditSummary(BaseModel):
    call_id: Optional[str] = "CALL_DEMO"
    vendor_name: str = "Sharmaji Chai & Snacks"
    stall_id: str = "STALL_004"
    revenue: float = Field(ge=0.0, description="Total cash and digital sales recorded")
    expenses: List[ExpenseItem] = Field(default_factory=list)
    total_expenses: float = Field(ge=0.0, description="Sum of all supply expenses")
    net_profit: float = Field(description="Calculated take-home profit (revenue - expenses)")
    profit_margin_pct: float = Field(description="Net profit divided by revenue percentage")
    gouging_alerts: List[GougingAlert] = Field(default_factory=list)
    spoken_confirmation_en: str = Field(description="Warm English confirmation for ElevenLabs voice output")
    spoken_confirmation_hi: str = Field(description="Warm Hindi confirmation for telephone speaker")
    unresolved_text: Optional[str] = None

class CallSimulationRequest(BaseModel):
    transcript_id: Optional[str] = None
    custom_speech: Optional[str] = None
    stall_id: Optional[str] = "STALL_004"

class CallSimulationResponse(BaseModel):
    status: str
    transcript: str
    audit: DailyAuditSummary
    audio_stream_url: Optional[str] = None
