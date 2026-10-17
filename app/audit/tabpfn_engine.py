import os
import csv
from pathlib import Path
from typing import Dict, Any, List, Optional
from app.config import settings

class TabPFNEngine:
    """
    In-context tabular foundation model auditor for price gouging detection.
    Evaluates unit prices against historical 30-day baseline transactions.
    """

    def __init__(self, history_csv_path: Optional[Path] = None, threshold_pct: float = 8.0):
        self.history_csv_path = history_csv_path or settings.SAMPLE_HISTORY_PATH
        self.threshold_pct = threshold_pct

    def load_history(self) -> List[Dict[str, Any]]:
        """
        Loads baseline historical purchase records.
        """
        records = []
        if not self.history_csv_path.exists():
            return records

        with open(self.history_csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    records.append({
                        "date": row.get("date"),
                        "item_id": row.get("item_id"),
                        "item": (row.get("item") or "").strip().lower(),
                        "supplier_name": row.get("supplier_name"),
                        "unit_price": float(row.get("unit_price", 0.0)),
                        "quantity": float(row.get("quantity", 0.0)),
                        "unit": row.get("unit"),
                        "total_amount": float(row.get("total_amount", 0.0)),
                    })
                except ValueError:
                    continue
        return records

    def audit_item_price(self, item_name: str, unit_price: float, quantity: float = 1.0) -> Dict[str, Any]:
        """
        Audits an incoming commodity price against historical distribution.
        Flags price spikes >= threshold_pct (default 8.0%).
        """
        item_clean = item_name.strip().lower()
        history = self.load_history()
        item_records = [r for r in history if r["item"] == item_clean]

        # Graceful degradation: If fewer than 3 historical transactions, flag insufficient history
        if len(item_records) < 3:
            return {
                "anomaly": False,
                "reason": "insufficient_history",
                "sample_count": len(item_records),
                "item": item_name,
                "current_price": unit_price
            }

        past_prices = [r["unit_price"] for r in item_records]
        baseline_mean = sum(past_prices) / len(past_prices)
        pct_difference = ((unit_price - baseline_mean) / baseline_mean) * 100.0

        if pct_difference >= self.threshold_pct:
            extra_per_unit = unit_price - baseline_mean
            extra_total = extra_per_unit * quantity
            return {
                "anomaly": True,
                "item": item_name,
                "baseline_price": round(baseline_mean, 2),
                "current_price": round(unit_price, 2),
                "pct_increase": round(pct_difference, 1),
                "extra_cost_per_unit": round(extra_per_unit, 2),
                "extra_cost_total": round(extra_total, 2),
                "sample_count": len(item_records),
                "warning_message": (
                    f"Warning: {item_name.title()} was ₹{round(unit_price, 1)} today. "
                    f"Your 30-day baseline is ₹{round(baseline_mean, 1)}. "
                    f"You overpaid by {round(pct_difference, 1)}% (+₹{round(extra_total, 1)} total extra)."
                )
            }

        return {
            "anomaly": False,
            "item": item_name,
            "baseline_price": round(baseline_mean, 2),
            "current_price": round(unit_price, 2),
            "pct_difference": round(pct_difference, 1),
            "sample_count": len(item_records)
        }

tabpfn_engine = TabPFNEngine()
