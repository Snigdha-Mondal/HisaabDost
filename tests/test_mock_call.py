import unittest
from app.agent.schemas import VendorProfile
from scripts.mock_call import run_simulation, load_transcripts

class TestMockTelephonyCLI(unittest.TestCase):
    def setUp(self):
        self.vendor = VendorProfile()
        self.transcripts = load_transcripts()

    def test_load_transcripts_has_scenarios(self):
        self.assertGreaterEqual(len(self.transcripts), 2)
        scenario_ids = [s["id"] for s in self.transcripts]
        self.assertIn("sharmaji_closing_gouging", scenario_ids)
        self.assertIn("sharmaji_closing_normal", scenario_ids)

    def test_run_simulation_gouging_scenario(self):
        scenario = next(s for s in self.transcripts if s["id"] == "sharmaji_closing_gouging")
        summary = run_simulation(scenario["spoken_text"], self.vendor)

        self.assertEqual(summary.revenue, 4200.0)
        self.assertEqual(summary.total_expenses, 2950.0)
        self.assertEqual(summary.net_profit, 1250.0)
        
        # Verify gouging alert on mustard oil
        self.assertEqual(len(summary.gouging_alerts), 1)
        alert = summary.gouging_alerts[0]
        self.assertEqual(alert.item, "mustard oil")
        self.assertGreaterEqual(alert.pct_increase, 8.0)
        self.assertEqual(alert.current_price, 950.0)

    def test_run_simulation_normal_scenario(self):
        scenario = next(s for s in self.transcripts if s["id"] == "sharmaji_closing_normal")
        summary = run_simulation(scenario["spoken_text"], self.vendor)

        self.assertEqual(summary.revenue, 3800.0)
        self.assertEqual(summary.total_expenses, 1260.0)
        self.assertEqual(summary.net_profit, 2540.0)
        
        # Verify no price gouging alerts triggered
        self.assertEqual(len(summary.gouging_alerts), 0)

if __name__ == "__main__":
    unittest.main()
