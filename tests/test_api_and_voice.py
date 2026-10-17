import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.voice.elevenlabs_client import elevenlabs_client
from app.telephony.sentry_tracer import tracer

client = TestClient(app)

class TestAPIAndVoice(unittest.TestCase):
    def test_health_check(self):
        res = client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "HisaabDost")

    def test_get_scenarios(self):
        res = client.get("/api/scenarios")
        self.assertEqual(res.status_code, 200)
        scenarios = res.json()
        self.assertIsInstance(scenarios, list)
        self.assertGreaterEqual(len(scenarios), 2)

    def test_get_ledger(self):
        res = client.get("/api/ledger")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_records", data)
        self.assertGreaterEqual(data["total_records"], 30)
        self.assertIn("commodity_stats", data)
        self.assertIn("mustard oil", data["commodity_stats"])

    def test_get_udhar(self):
        res = client.get("/api/udhar")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_outstanding", data)
        self.assertGreater(data["total_outstanding"], 0)
        self.assertIsInstance(data["accounts"], list)

    def test_simulate_phone_call_endpoint(self):
        payload = {"transcript_id": "sharmaji_closing_gouging"}
        res = client.post("/api/call/simulate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "completed")
        self.assertIn("audio_stream_url", data)

        audit = data["audit"]
        self.assertEqual(audit["revenue"], 4200.0)
        self.assertEqual(audit["total_expenses"], 2950.0)
        self.assertEqual(audit["net_profit"], 1250.0)
        self.assertEqual(len(audit["gouging_alerts"]), 1)
        self.assertEqual(audit["gouging_alerts"][0]["item"], "mustard oil")

    def test_elevenlabs_voice_client_synthesis(self):
        res = elevenlabs_client.synthesize("Namaste Uncle, sab darj ho gaya.", language="hi")
        self.assertEqual(res["status"], "success")
        self.assertIn("audio_base64", res)
        self.assertIn("audio_data_uri", res)
        self.assertTrue(res["audio_data_uri"].startswith("data:audio/"))

    def test_sentry_tracer_span(self):
        with tracer.trace_span("test.operation", "Testing tracer span") as span:
            self.assertEqual(span["op"], "test.operation")
        self.assertIn("elapsed_ms", span)
        self.assertGreaterEqual(span["elapsed_ms"], 0.0)

if __name__ == "__main__":
    unittest.main()
