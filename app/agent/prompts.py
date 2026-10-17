"""
Prompt templates and few-shot examples for Gemma 2 colloquial entity extraction.
Crafted for Indian roadside food stall and micro-merchant dialect parsing.
"""

GEMMA_SYSTEM_PROMPT = """You are HisaabDost (हिसाब दोस्त), an expert accounting AI assistant built specifically for elderly roadside food stalls, tea carts, and street vendors.
Your job is to listen to the vendor's informal spoken summary and extract precise financial figures into clean, structured JSON.

Core Linguistic & Accounting Rules:
1. Vendors speak casually in Hindi, English, or Hinglish:
   - Slang Commodities: "doodh" -> "milk", "sarson ka tel" / "dabba tel" -> "mustard oil", "sabzi" -> "vegetables", "cheeni" / "shakkar" -> "sugar", "chai patti" / "patti" -> "tea leaves", "tamatar" -> "tomatoes", "aloo" -> "potatoes", "atta" -> "flour", "maida" -> "refined flour", "gas" -> "commercial gas", "bhada" -> "stall rent / transport".
   - Slang Units: "liter" -> liters, "kilo" -> kg, "dabba" -> cans, "crate" / "peti" -> crates/boxes, "pao" -> 0.25 kg, "aadha kilo" -> 0.5 kg, "dedh kilo" -> 1.5 kg, "dhai kilo" -> 2.5 kg.
   - Slang Sales Terms: "galla", "gullak", "scanner", "kamai", "bikri", "sales", "collection".
2. Standardize all item names to lowercase English common names (e.g., "mustard oil", "milk", "vegetables", "tea leaves", "sugar").
3. Preserve the vendor's exact spoken word in "raw_name" for transparency and ledger auditability.
4. Calculate derived unit_price = total_cost / quantity.
5. Distinguish clearly between EXPENSES (money paid out for supplies) and REVENUE (money collected in cash/scanner/gullak).
6. Calculate net_profit = total_revenue - total_expenses.
7. Ambiguity Safety Guardrail: If an item or price is mentioned without necessary quantity or cost (e.g., "tel liya tha lekin bill kal aayega"), do NOT hallucinate numbers; capture it under "unresolved_text".
8. Output valid JSON only matching the schema without conversational preamble.
"""

FEW_SHOT_EXAMPLES = [
    {
        "scenario": "Evening tea stall closing with oil price spike",
        "input": "Haan beta, aaj 10 liter doodh liya 600 ka. 2 dabba sarson ka tel liya 1900 ka. Mandi se sabzi aayi 450 ki. Gullak mein 4200 rupaye bache hain.",
        "output": {
            "revenue": 4200.0,
            "expenses": [
                {
                    "item": "mustard oil",
                    "raw_name": "sarson ka tel",
                    "quantity": 2.0,
                    "unit": "cans",
                    "total_cost": 1900.0,
                    "unit_price": 950.0
                },
                {
                    "item": "milk",
                    "raw_name": "doodh",
                    "quantity": 10.0,
                    "unit": "liters",
                    "total_cost": 600.0,
                    "unit_price": 60.0
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
        "scenario": "Routine morning chai & grocery restock",
        "input": "Namaste, aaj 12 liter doodh 720 ka, 1 kilo chai patti 320, aur 5 kilo cheeni 220 ki. Total bikri hui 3800 rupaye.",
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
    },
    {
        "scenario": "Street snack & samosa cart",
        "input": "Bhaiya aaj 20 kilo aloo liya 500 ka, 1 dabba refined tel 920 ka, aur 5 kilo maida 180 ka. Galla bana 3400.",
        "output": {
            "revenue": 3400.0,
            "expenses": [
                {
                    "item": "potatoes",
                    "raw_name": "aloo",
                    "quantity": 20.0,
                    "unit": "kg",
                    "total_cost": 500.0,
                    "unit_price": 25.0
                },
                {
                    "item": "cooking oil",
                    "raw_name": "refined tel",
                    "quantity": 1.0,
                    "unit": "cans",
                    "total_cost": 920.0,
                    "unit_price": 920.0
                },
                {
                    "item": "refined flour",
                    "raw_name": "maida",
                    "quantity": 5.0,
                    "unit": "kg",
                    "total_cost": 180.0,
                    "unit_price": 36.0
                }
            ],
            "total_expenses": 1600.0,
            "net_profit": 1800.0,
            "unresolved_text": None
        }
    },
    {
        "scenario": "Roadside roadside fruit juice cart",
        "input": "Aaj 3 peti santra 2100 ka, 2 peti mosambi 1600 ka, aur barf aayi 150 ki. Scanner aur cash mila ke 5200 ki kamai hui.",
        "output": {
            "revenue": 5200.0,
            "expenses": [
                {
                    "item": "oranges",
                    "raw_name": "santra",
                    "quantity": 3.0,
                    "unit": "crates",
                    "total_cost": 2100.0,
                    "unit_price": 700.0
                },
                {
                    "item": "sweet lime",
                    "raw_name": "mosambi",
                    "quantity": 2.0,
                    "unit": "crates",
                    "total_cost": 1600.0,
                    "unit_price": 800.0
                },
                {
                    "item": "ice",
                    "raw_name": "barf",
                    "quantity": 1.0,
                    "unit": "block",
                    "total_cost": 150.0,
                    "unit_price": 150.0
                }
            ],
            "total_expenses": 3850.0,
            "net_profit": 1350.0,
            "unresolved_text": None
        }
    },
    {
        "scenario": "Ambiguous input with unstated price",
        "input": "Doodh liya 5 liter 300 ka, par tel ka dabba udhar pe aaya hai uska bill kal milega. Gullak mein 2000 rupaye hain.",
        "output": {
            "revenue": 2000.0,
            "expenses": [
                {
                    "item": "milk",
                    "raw_name": "doodh",
                    "quantity": 5.0,
                    "unit": "liters",
                    "total_cost": 300.0,
                    "unit_price": 60.0
                }
            ],
            "total_expenses": 300.0,
            "net_profit": 1700.0,
            "unresolved_text": "tel ka dabba udhar pe aaya hai uska bill kal milega"
        }
    }
]
