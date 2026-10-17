import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from app.config import settings
from app.audit.ledger_manager import ledger_manager, LedgerManager

logger = logging.getLogger(__name__)

class TabPFNEngine:
    """
    In-context tabular foundation model auditor for wholesale price-gouging detection.
    Evaluates unit prices against the vendor's historical 30-day purchase distribution.
    Supports Prior Labs TabPFN API and high-speed statistical in-context audit.
    """

    def __init__(
        self,
        manager: Optional[LedgerManager] = None,
        threshold_pct: float = 8.0,
        api_key: Optional[str] = None
    ):
        self.ledger = manager or ledger_manager
        self.threshold_pct = threshold_pct or settings.TABPFN_ANOMALY_THRESHOLD_PCT
        self.api_key = api_key or settings.TABPFN_API_KEY

    def audit_item_price(
        self,
        item_name: str,
        unit_price: float,
        quantity: float = 1.0,
        supplier: str = "Wholesale Supplier"
    ) -> Dict[str, Any]:
        """
        Audits an incoming commodity unit price against the historical distribution.
        Flags price spikes >= threshold_pct (default 8.0%).
        """
        clean_name = item_name.strip().lower()
        records = self.ledger.get_item_records(clean_name)

        # Graceful degradation guardrail: If fewer than 3 historical transactions, flag insufficient history
        if len(records) < 3:
            return {
                "anomaly": False,
                "reason": "insufficient_history",
                "sample_count": len(records),
                "item": item_name,
                "current_price": unit_price,
                "warning_message": f"Recorded ₹{unit_price} for {item_name}. Not enough past purchase history to verify baseline."
            }

        # If Prior Labs TabPFN API key is configured, invoke TabPFN API
        if self.api_key:
            try:
                return self._audit_with_tabpfn_api(clean_name, unit_price, quantity, records)
            except Exception as e:
                logger.warning(f"TabPFN API call failed ({e}). Falling back to statistical tabular baseline.")

        # In-context statistical audit
        past_prices = [r["unit_price"] for r in records]
        baseline_mean = round(sum(past_prices) / len(past_prices), 2)
        pct_difference = round(((unit_price - baseline_mean) / baseline_mean) * 100.0, 1)

        if pct_difference >= self.threshold_pct:
            extra_per_unit = round(unit_price - baseline_mean, 2)
            extra_total = round(extra_per_unit * quantity, 2)
            return {
                "anomaly": True,
                "item": clean_name,
                "supplier": supplier,
                "baseline_price": baseline_mean,
                "current_price": round(unit_price, 2),
                "pct_increase": pct_difference,
                "extra_cost_per_unit": extra_per_unit,
                "extra_cost_total": extra_total,
                "sample_count": len(records),
                "warning_message": (
                    f"Warning: {item_name.title()} was ₹{round(unit_price, 1)} today. "
                    f"Your 30-day baseline is ₹{round(baseline_mean, 1)}. "
                    f"You overpaid by {pct_difference}% (+₹{round(extra_total, 1)} total extra)."
                )
            }

        return {
            "anomaly": False,
            "item": clean_name,
            "baseline_price": round(baseline_mean, 2),
            "current_price": round(unit_price, 2),
            "pct_difference": round(pct_difference, 1),
            "sample_count": len(records)
        }

    def _audit_with_tabpfn_api(
        self,
        item_name: str,
        unit_price: float,
        quantity: float,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calls Prior Labs TabPFN cloud inference endpoint for in-context tabular regression/outlier classification.
        """
        import httpx
        url = "https://api.priorlabs.ai/v1/predict"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        
        # Prepare tabular feature vectors [quantity, total_amount] -> unit_price
        x_train = [[r["quantity"], r["total_amount"]] for r in records]
        y_train = [r["unit_price"] for r in records]
        x_test = [[quantity, unit_price * quantity]]

        payload = {
            "model": "tabpfn-3.5",
            "x_train": x_train,
            "y_train": y_train,
            "x_test": x_test
        }
        res = httpx.post(url, json=payload, headers=headers, timeout=5.0)
        res.raise_for_status()
        predicted_baseline = res.json().get("predictions", [unit_price])[0]

        pct_difference = ((unit_price - predicted_baseline) / predicted_baseline) * 100.0
        is_anomaly = pct_difference >= self.threshold_pct

        extra_per_unit = max(0.0, unit_price - predicted_baseline)
        extra_total = extra_per_unit * quantity

        return {
            "anomaly": is_anomaly,
            "item": item_name,
            "baseline_price": round(predicted_baseline, 2),
            "current_price": round(unit_price, 2),
            "pct_increase": round(pct_difference, 1),
            "extra_cost_per_unit": round(extra_per_unit, 2),
            "extra_cost_total": round(extra_total, 2),
            "sample_count": len(records),
            "engine": "priorlabs-tabpfn-3.5"
        }

tabpfn_engine = TabPFNEngine()
