import unittest
from app.agent.gemma_parser import gemma_parser

class TestGemmaParserDialects(unittest.TestCase):
    def test_scenario_tea_stall_gouging(self):
        spoken = "Haan beta, aaj ka hisaab likh lo. Doodh liya tha 10 liter 600 rupay ka. Kisan traders se 2 dabba sarson ka tel liya 1900 ka. Aur Mandi se sabzi aayi thi 450 ki. Din bhar mein gullak aur scanner mila ke total 4200 rupay ki bikri hui hai."
        res = gemma_parser.parse_speech(spoken)

        self.assertEqual(res["revenue"], 4200.0)
        self.assertEqual(res["total_expenses"], 2950.0)
        self.assertEqual(res["net_profit"], 1250.0)
        
        items = {e["item"]: e for e in res["expenses"]}
        self.assertIn("mustard oil", items)
        self.assertEqual(items["mustard oil"]["quantity"], 2.0)
        self.assertEqual(items["mustard oil"]["unit_price"], 950.0)

        self.assertIn("milk", items)
        self.assertEqual(items["milk"]["quantity"], 10.0)
        self.assertEqual(items["milk"]["unit_price"], 60.0)

        self.assertIn("vegetables", items)
        self.assertEqual(items["vegetables"]["total_cost"], 450.0)

    def test_scenario_chai_and_groceries(self):
        spoken = "Namaste, aaj 12 liter doodh liya tha 720 ka, chai patti aayi 1 kilo 320 rupaye, aur 5 kilo cheeni 220 rupaye ki. Aaj gullek mein total bikri 3800 rupaye hui hai."
        res = gemma_parser.parse_speech(spoken)

        self.assertEqual(res["revenue"], 3800.0)
        self.assertEqual(res["total_expenses"], 1260.0)
        self.assertEqual(res["net_profit"], 2540.0)

        items = {e["item"]: e for e in res["expenses"]}
        self.assertIn("milk", items)
        self.assertIn("tea leaves", items)
        self.assertIn("sugar", items)
        self.assertEqual(items["tea leaves"]["unit_price"], 320.0)
        self.assertEqual(items["sugar"]["unit_price"], 44.0)

    def test_scenario_snack_samosa_cart(self):
        spoken = "Bhaiya aaj 20 kilo aloo liya 500 ka, 1 dabba refined tel 920 ka, aur 5 kilo maida 180 ka. Galla bana 3400."
        res = gemma_parser.parse_speech(spoken)

        self.assertEqual(res["revenue"], 3400.0)
        self.assertEqual(res["total_expenses"], 1600.0)
        self.assertEqual(res["net_profit"], 1800.0)

        items = {e["item"]: e for e in res["expenses"]}
        self.assertIn("potatoes", items)
        self.assertEqual(items["potatoes"]["quantity"], 20.0)
        self.assertEqual(items["potatoes"]["unit_price"], 25.0)

        self.assertIn("cooking oil", items)
        self.assertEqual(items["cooking oil"]["total_cost"], 920.0)

        self.assertIn("refined flour", items)
        self.assertEqual(items["refined flour"]["quantity"], 5.0)

    def test_scenario_fruit_juice_cart(self):
        spoken = "Aaj 3 peti santra 2100 ka, 2 peti mosambi 1600 ka, aur barf aayi 150 ki. Scanner aur cash mila ke 5200 ki kamai hui."
        res = gemma_parser.parse_speech(spoken)

        self.assertEqual(res["revenue"], 5200.0)
        self.assertEqual(res["total_expenses"], 3850.0)
        self.assertEqual(res["net_profit"], 1350.0)

        items = {e["item"]: e for e in res["expenses"]}
        self.assertIn("oranges", items)
        self.assertEqual(items["oranges"]["quantity"], 3.0)
        self.assertEqual(items["oranges"]["unit_price"], 700.0)

        self.assertIn("sweet lime", items)
        self.assertEqual(items["sweet lime"]["quantity"], 2.0)

        self.assertIn("ice", items)
        self.assertEqual(items["ice"]["total_cost"], 150.0)

    def test_scenario_ambiguous_and_pending_bill(self):
        spoken = "Doodh liya 5 liter 300 ka, par tel ka dabba udhar pe aaya hai uska bill kal milega. Gullak mein 2000 rupaye hain."
        res = gemma_parser.parse_speech(spoken)

        self.assertEqual(res["revenue"], 2000.0)
        self.assertEqual(res["total_expenses"], 300.0)
        self.assertEqual(res["net_profit"], 1700.0)

        # Check that ambiguity guardrail caught the unbilled item
        self.assertIsNotNone(res["unresolved_text"])
        self.assertIn("bill kal", res["unresolved_text"])

        # Check only milk was recorded as an expense, not the unbilled oil
        items = {e["item"]: e for e in res["expenses"]}
        self.assertIn("milk", items)
        self.assertNotIn("mustard oil", items)

    def test_spoken_number_words_and_stt_artifacts(self):
        # 1. Spoken English words
        res1 = gemma_parser.parse_speech("my sales were three hundred seventy five rupees")
        self.assertEqual(res1["revenue"], 375.0)
        self.assertEqual(res1["total_expenses"], 0.0)
        self.assertEqual(res1["net_profit"], 375.0)

        # 2. STT acoustic concatenation artifact (300 + 75 -> 30075)
        res2 = gemma_parser.parse_speech("my sales were 30075 rupees")
        self.assertEqual(res2["revenue"], 375.0)
        self.assertEqual(res2["net_profit"], 375.0)

        # 3. STT spaced numbers (300 + 75 -> 375)
        res3 = gemma_parser.parse_speech("my sales were 300 75 rupees")
        self.assertEqual(res3["revenue"], 375.0)
        self.assertEqual(res3["net_profit"], 375.0)

        # 4. Spoken Hindi number words
        res4 = gemma_parser.parse_speech("meri bikri teen sau pachattar rupaye thi")
        self.assertEqual(res4["revenue"], 375.0)
        self.assertEqual(res4["net_profit"], 375.0)

    def test_flexible_clause_ordering_expenses_before_revenue(self):
        # 1. Expenses mentioned BEFORE sales: "i bought milk for 200 and my sales were 500"
        res1 = gemma_parser.parse_speech("i bought milk for 200 and my sales were 500")
        self.assertEqual(res1["revenue"], 500.0)
        self.assertEqual(res1["total_expenses"], 200.0)
        self.assertEqual(res1["net_profit"], 300.0)
        items1 = {e["item"]: e for e in res1["expenses"]}
        self.assertIn("milk", items1)
        self.assertEqual(items1["milk"]["total_cost"], 200.0)

        # 2. Spoken number words with expenses first: "i bought milk for two hundred and my sales were five hundred"
        res2 = gemma_parser.parse_speech("i bought milk for two hundred and my sales were five hundred")
        self.assertEqual(res2["revenue"], 500.0)
        self.assertEqual(res2["total_expenses"], 200.0)
        self.assertEqual(res2["net_profit"], 300.0)

        # 3. Reverse order sales syntax: "i bought milk for 200 and 500 in sales"
        res3 = gemma_parser.parse_speech("i bought milk for 200 and 500 in sales")
        self.assertEqual(res3["revenue"], 500.0)
        self.assertEqual(res3["total_expenses"], 200.0)
        self.assertEqual(res3["net_profit"], 300.0)

        # 4. Hindi colloquial expenses before revenue
        res4 = gemma_parser.parse_speech("doodh liya do sau ka aur meri bikri paanch sau thi")
        self.assertEqual(res4["revenue"], 500.0)
        self.assertEqual(res4["total_expenses"], 200.0)
        self.assertEqual(res4["net_profit"], 300.0)

if __name__ == "__main__":
    unittest.main()

