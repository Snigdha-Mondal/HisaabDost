import unittest
import tempfile
from pathlib import Path
from app.audit.tabpfn_engine import TabPFNEngine
from app.audit.ledger_manager import LedgerManager

class TestTabPFNAnomalyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TabPFNEngine()

    def test_mustard_oil_price_spike_detected(self):
        # Baseline in sample_history.csv is ~849.5
        # Vendor charged ₹950 for 2 cans
        res = self.engine.audit_item_price("mustard oil", unit_price=950.0, quantity=2.0)

        self.assertTrue(res["anomaly"], "Expected price gouging anomaly to be flagged")
        self.assertAlmostEqual(res["baseline_price"], 849.5, delta=1.5)
        self.assertEqual(res["current_price"], 950.0)
        self.assertGreater(res["pct_increase"], 8.0)
        self.assertAlmostEqual(res["extra_cost_total"], 200.0, delta=2.5)
        self.assertIn("Warning: Mustard Oil was ₹950.0", res["warning_message"])

    def test_milk_normal_price_no_anomaly(self):
        # Baseline in sample_history.csv is ~59.9
        # Vendor charged ₹60 for 10 liters
        res = self.engine.audit_item_price("milk", unit_price=60.0, quantity=10.0)

        self.assertFalse(res["anomaly"], "Normal price should not be flagged as anomaly")
        self.assertAlmostEqual(res["baseline_price"], 60.0, delta=0.5)
        self.assertLess(abs(res["pct_difference"]), 8.0)

    def test_insufficient_history_graceful_degradation(self):
        # Item with no records in history
        res = self.engine.audit_item_price("exotic_saffron", unit_price=500.0, quantity=1.0)

        self.assertFalse(res["anomaly"])
        self.assertEqual(res["reason"], "insufficient_history")
        self.assertEqual(res["sample_count"], 0)

    def test_mathematical_precision(self):
        unit_price = 950.0
        quantity = 2.0
        res = self.engine.audit_item_price("mustard oil", unit_price=unit_price, quantity=quantity)

        baseline = res["baseline_price"]
        expected_pct = round(((unit_price - baseline) / baseline) * 100.0, 1)
        expected_extra = round((unit_price - baseline) * quantity, 2)

        self.assertEqual(res["pct_increase"], expected_pct)
        self.assertEqual(res["extra_cost_total"], expected_extra)

    def test_ledger_manager_isolated_append_and_stats(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv") as tmp:
            tmp_path = Path(tmp.name)

        try:
            manager = LedgerManager(csv_path=tmp_path)
            # Append 3 transactions
            manager.append_transaction("tea leaves", unit_price=300.0, quantity=2.0, unit="kg", total_amount=600.0)
            manager.append_transaction("tea leaves", unit_price=320.0, quantity=1.5, unit="kg", total_amount=480.0)
            manager.append_transaction("tea leaves", unit_price=310.0, quantity=1.0, unit="kg", total_amount=310.0)

            stats = manager.get_stats("tea leaves")
            self.assertEqual(stats["count"], 3)
            self.assertEqual(stats["mean"], 310.0)
            self.assertEqual(stats["min"], 300.0)
            self.assertEqual(stats["max"], 320.0)

            # Audit against this custom isolated ledger
            custom_engine = TabPFNEngine(manager=manager, threshold_pct=8.0)
            # Spiked price at ₹360 (+16.1%)
            spike_res = custom_engine.audit_item_price("tea leaves", unit_price=360.0, quantity=2.0)
            self.assertTrue(spike_res["anomaly"])
            self.assertEqual(spike_res["baseline_price"], 310.0)
            self.assertEqual(spike_res["extra_cost_total"], 100.0)  # (360 - 310) * 2 = 100.0

        finally:
            if tmp_path.exists():
                tmp_path.unlink()

if __name__ == "__main__":
    unittest.main()
