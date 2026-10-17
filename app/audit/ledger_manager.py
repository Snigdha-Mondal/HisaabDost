import csv
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import date
from app.config import settings

class LedgerManager:
    """
    Manages the CSV ledger of historical vendor commodity purchases.
    Provides querying, statistical summaries, and atomic appending of new records.
    """

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or settings.SAMPLE_HISTORY_PATH

    def load_all_records(self) -> List[Dict[str, Any]]:
        if not self.csv_path.exists():
            return []

        records = []
        with open(self.csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    records.append({
                        "date": row.get("date"),
                        "item_id": row.get("item_id"),
                        "item": (row.get("item") or "").strip().lower(),
                        "supplier_name": row.get("supplier_name", "Wholesale Supplier"),
                        "unit_price": float(row.get("unit_price", 0.0)),
                        "quantity": float(row.get("quantity", 0.0)),
                        "unit": row.get("unit", "units"),
                        "total_amount": float(row.get("total_amount", 0.0))
                    })
                except (ValueError, TypeError):
                    continue
        return records

    def get_item_records(self, item_name: str) -> List[Dict[str, Any]]:
        clean_name = item_name.strip().lower()
        records = self.load_all_records()
        return [r for r in records if r["item"] == clean_name]

    def get_stats(self, item_name: str) -> Dict[str, Any]:
        item_records = self.get_item_records(item_name)
        if not item_records:
            return {"count": 0, "mean": 0.0, "min": 0.0, "max": 0.0}

        prices = [r["unit_price"] for r in item_records]
        mean_val = sum(prices) / len(prices)
        return {
            "count": len(prices),
            "mean": round(mean_val, 2),
            "min": min(prices),
            "max": max(prices)
        }

    def append_transaction(
        self,
        item: str,
        unit_price: float,
        quantity: float,
        unit: str,
        total_amount: float,
        item_id: Optional[str] = None,
        supplier_name: str = "Wholesale Supplier",
        txn_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Appends a newly confirmed and audited transaction to the historical ledger.
        """
        new_row = {
            "date": txn_date or date.today().isoformat(),
            "item_id": item_id or f"ITEM_{item.upper()[:3]}_{int(quantity)}",
            "item": item.strip().lower(),
            "supplier_name": supplier_name,
            "unit_price": round(unit_price, 2),
            "quantity": round(quantity, 2),
            "unit": unit,
            "total_amount": round(total_amount, 2)
        }

        has_header = self.csv_path.exists() and self.csv_path.stat().st_size > 0
        with open(self.csv_path, mode="a", encoding="utf-8", newline="") as f:
            fieldnames = ["date", "item_id", "item", "supplier_name", "unit_price", "quantity", "unit", "total_amount"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not has_header:
                writer.writeheader()
            writer.writerow(new_row)

        return new_row

ledger_manager = LedgerManager()
