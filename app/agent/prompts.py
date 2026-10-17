"""
Prompt templates and few-shot examples for Gemma 2 colloquial entity extraction.
"""

GEMMA_SYSTEM_PROMPT = """You are HisaabDost (हिसाब दोस्त), an expert accounting AI assistant built specifically for elderly roadside food stalls, tea carts, and street vendors.
Your job is to listen to the vendor's informal spoken summary and extract precise financial figures into clean, structured JSON.

Core Rules:
1. Vendors speak casually in Hindi, English, or Hinglish (e.g. "doodh", "sarson ka tel", "tamatar", "cheeni", "chai patti", "galla", "gullak", "bikri").
2. Standardize item names to English common names (e.g., "doodh" -> "milk", "sarson ka tel" / "dabba tel" -> "mustard oil", "sabzi" -> "vegetables", "cheeni" -> "sugar", "chai patti" -> "tea leaves").
3. Always calculate unit_price = total_cost / quantity when quantity is given.
4. Distinguish clearly between EXPENSES (money paid out for supplies) and REVENUE (money collected in cash/scanner/gullak).
5. Calculate net_profit = total_revenue - total_expenses.
6. If an item price is unclear or missing, do NOT hallucinate; set "unresolved_text".
7. Output valid JSON only matching the schema. Do not output conversational preamble.
"""

FEW_SHOT_EXAMPLES = [
    {
        "input": "Haan beta, aaj 10 liter doodh liya 600 ka. 2 dabba sarson ka tel liya 1900 ka. Sabzi aayi 450 ki. Gullak mein 4200 rupaye bane.",
        "output": {
            "revenue": 4200.0,
            "expenses": [
                {
                    "item": "milk",
                    "raw_name": "doodh",
                    "quantity": 10.0,
                    "unit": "liters",
                    "total_cost": 600.0,
                    "unit_price": 60.0
                },
                {
                    "item": "mustard oil",
                    "raw_name": "sarson ka tel",
                    "quantity": 2.0,
                    "unit": "cans",
                    "total_cost": 1900.0,
                    "unit_price": 950.0
                },
                {
                    "item": "vegetables",
                    "raw_name": "sabzi",
                    "quantity": 1.0,
                    "unit": "basket",
                    "total_cost": 450.0,
                    "unit_price": 450.0
                }
            ],
            "total_expenses": 2950.0,
            "net_profit": 1250.0,
            "unresolved_text": None
        }
    },
    {
        "input": "Aaj 12 liter doodh 720 ka, 1 kilo chai patti 320, aur 5 kilo cheeni 220 ki. Total bikri hui 3800 rupaye.",
        "output": {
            "revenue": 3800.0,
            "expenses": [
                {
                    "item": "milk",
                    "raw_name": "doodh",
                    "quantity": 12.0,
                    "unit": "liters",
                    "total_cost": 720.0,
                    "unit_price": 60.0
                },
                {
                    "item": "tea leaves",
                    "raw_name": "chai patti",
                    "quantity": 1.0,
                    "unit": "kg",
                    "total_cost": 320.0,
                    "unit_price": 320.0
                },
                {
                    "item": "sugar",
                    "raw_name": "cheeni",
                    "quantity": 5.0,
                    "unit": "kg",
                    "total_cost": 220.0,
                    "unit_price": 44.0
                }
            ],
            "total_expenses": 1260.0,
            "net_profit": 2540.0,
            "unresolved_text": None
        }
    }
]
