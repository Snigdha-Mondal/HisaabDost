import unittest
import asyncio
from app.workflows.closing_workflow import DailyClosingWorkflow

class TestTemporalClosingWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = DailyClosingWorkflow()

    def test_successful_closing_workflow_with_gouging_alert(self):
        result = asyncio.run(self.workflow.run(
            vendor_id="VEND_001",
            phone_number="+919876543210",
            caregiver_phone="+919811122233",
            simulated_call_status="completed"
        ))

        self.assertEqual(result["status"], "COMPLETED_RECONCILED")
        self.assertEqual(result["vendor_id"], "VEND_001")
        self.assertIn("CALL_VEND_001", result["call_id"])

        audit = result["audit"]
        self.assertEqual(audit["revenue"], 4200.0)
        self.assertEqual(audit["total_expenses"], 2950.0)
        self.assertEqual(audit["net_profit"], 1250.0)

        # Mustard oil price gouging detected
        self.assertEqual(len(audit["gouging_alerts"]), 1)
        alert = audit["gouging_alerts"][0]
        self.assertEqual(alert["item"], "mustard oil")
        self.assertGreaterEqual(alert["pct_increase"], 8.0)

        # Caregiver SMS dispatched with price gouging warning
        notification = result["notification"]
        self.assertEqual(notification["status"], "GOUGING_ALERT_SMS_DISPATCHED")
        self.assertIn("PRICE GOUGING DETECTED", notification["message"])
        self.assertEqual(notification["caregiver_phone"], "+919811122233")

    def test_telephony_busy_signal_retry_and_escalation(self):
        # Simulates telephone line busy (vendor serving a customer rush)
        result = asyncio.run(self.workflow.run(
            vendor_id="VEND_001",
            phone_number="+919876543210",
            caregiver_phone="+919811122233",
            simulated_call_status="busy"
        ))

        self.assertEqual(result["status"], "FAILED_CALL_MISSED")
        self.assertEqual(result["attempts"], 3)
        self.assertIn("busy", result["reason"])

        # Escalates to family caregiver
        escalation = result["escalation"]
        self.assertEqual(escalation["status"], "MISSED_CALL_NOTIFICATION_SENT")
        self.assertIn("could not be reached after 3 call attempts", escalation["message"])

    def test_normal_routine_closing_workflow(self):
        normal_speech = (
            "Namaste, aaj 12 liter doodh liya tha 720 ka, "
            "chai patti aayi 1 kilo 320 rupaye, aur 5 kilo cheeni 220 rupaye ki. "
            "Aaj gullek mein total bikri 3800 rupaye hui hai."
        )
        result = asyncio.run(self.workflow.run(
            vendor_id="VEND_001",
            phone_number="+919876543210",
            caregiver_phone="+919811122233",
            simulated_call_status="completed",
            custom_transcript=normal_speech
        ))

        self.assertEqual(result["status"], "COMPLETED_RECONCILED")
        audit = result["audit"]
        self.assertEqual(audit["revenue"], 3800.0)
        self.assertEqual(audit["net_profit"], 2540.0)
        self.assertEqual(len(audit["gouging_alerts"]), 0)

        notification = result["notification"]
        self.assertEqual(notification["status"], "DAILY_SUMMARY_SMS_DISPATCHED")
        self.assertIn("All supplier prices healthy", notification["message"])

if __name__ == "__main__":
    unittest.main()
