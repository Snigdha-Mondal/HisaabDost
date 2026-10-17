import re
import json
import logging
from typing import Dict, Any, List, Optional
from app.config import settings
from app.agent.schemas import ExpenseItem
from app.agent.prompts import GEMMA_SYSTEM_PROMPT, FEW_SHOT_EXAMPLES

logger = logging.getLogger(__name__)

# Expanded street slang vocabulary mappings
COMMODITY_MAPPINGS = {
    # Dairy
    "doodh": ("milk", "liters"),
    "milk": ("milk", "liters"),
    "paneer": ("paneer", "kg"),
    "dahi": ("curd", "kg"),
    "makkhan": ("butter", "kg"),
    # Oils
    "sarson ka tel": ("mustard oil", "cans"),
    "sarson tel": ("mustard oil", "cans"),
    "dabba tel": ("mustard oil", "cans"),
    "refined tel": ("cooking oil", "cans"),
    "tel": ("mustard oil", "cans"),
    "oil": ("cooking oil", "cans"),
    "mustard oil": ("mustard oil", "cans"),
    # Vegetables & Produce
    "sabzi": ("vegetables", "basket"),
    "subzi": ("vegetables", "basket"),
    "vegetables": ("vegetables", "basket"),
    "tamatar": ("tomatoes", "kg"),
    "aloo": ("potatoes", "kg"),
    "pyaz": ("onions", "kg"),
    "adrak": ("ginger", "kg"),
    "mirchi": ("green chilies", "kg"),
    "matar": ("green peas", "kg"),
    # Fruits
    "santra": ("oranges", "crates"),
    "mosambi": ("sweet lime", "crates"),
    "seb": ("apples", "crates"),
    "kela": ("bananas", "dozens"),
    "barf": ("ice", "block"),
    # Dry Groceries & Spices
    "chai patti": ("tea leaves", "kg"),
    "patti": ("tea leaves", "kg"),
    "tea leaves": ("tea leaves", "kg"),
    "cheeni": ("sugar", "kg"),
    "chini": ("sugar", "kg"),
    "shakkar": ("sugar", "kg"),
    "sugar": ("sugar", "kg"),
    "atta": ("flour", "kg"),
    "maida": ("refined flour", "kg"),
    "besan": ("gram flour", "kg"),
    "chawal": ("rice", "kg"),
    "dal": ("lentils", "kg"),
    # Utilities & Rent
    "gas cylinder": ("commercial gas", "cylinder"),
    "cylinder": ("commercial gas", "cylinder"),
    "gas": ("commercial gas", "cylinder"),
    "thele ka bhada": ("cart rent", "day"),
    "bhada": ("transport rent", "trip")
}

COLLOQUIAL_QUANTITIES = {
    "aadha kilo": 0.5,
    "adha kilo": 0.5,
    "aadha liter": 0.5,
    "dedh kilo": 1.5,
    "dedh liter": 1.5,
    "dhai kilo": 2.5,
    "dhai liter": 2.5,
    "ek pao": 0.25,
    "pao kilo": 0.25,
    "pao": 0.25,
}

class GemmaParser:
    """
    Adapter for open-weight Gemma 2 inference.
    Executes colloquial street entity extraction with:
      1. Local Ollama inference (if USE_LOCAL_GEMMA is set)
      2. Cloud Generative AI endpoint (if GEMMA_API_KEY is set)
      3. Specialized offline street dialect linguistic rules (zero-latency, 100% deterministic)
    """

    def __init__(self):
        self.api_key = settings.GEMMA_API_KEY
        self.model_name = settings.GEMMA_MODEL_NAME
        self.use_local = settings.USE_LOCAL_GEMMA

    def parse_speech(self, spoken_text: str) -> Dict[str, Any]:
        """
        Parses informal street vendor speech into structured JSON.
        """
        # 1. Local Ollama execution
        if self.use_local:
            try:
                return self._parse_with_ollama(spoken_text)
            except Exception as e:
                logger.warning(f"Ollama execution failed ({e}). Falling back to street rules.")

        # 2. Remote Gemma API execution
        if self.api_key:
            try:
                return self._parse_with_api(spoken_text)
            except Exception as e:
                logger.warning(f"Gemma API execution failed ({e}). Falling back to street rules.")

        # 3. Deterministic offline street dialect extractor
        return self._parse_with_street_rules(spoken_text)

    def _parse_with_ollama(self, spoken_text: str) -> Dict[str, Any]:
        import httpx
        url = "http://localhost:11434/api/generate"
        prompt = f"{GEMMA_SYSTEM_PROMPT}\n\nVendor Speech: \"{spoken_text}\"\n\nJSON Output:"
        payload = {
            "model": "gemma2:9b",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        res = httpx.post(url, json=payload, timeout=12.0)
        res.raise_for_status()
        raw_out = res.json().get("response", "{}")
        return json.loads(raw_out)

    def _parse_with_api(self, spoken_text: str) -> Dict[str, Any]:
        import httpx
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        prompt = f"{GEMMA_SYSTEM_PROMPT}\n\nInput speech: \"{spoken_text}\"\n\nJSON output:"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
        }
        response = httpx.post(url, json=payload, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        raw_json_str = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(raw_json_str)

    def _parse_with_street_rules(self, spoken_text: str) -> Dict[str, Any]:
        """
        Deterministic, offline rule-based extractor engineered for street Hindi & Hinglish.
        Accurately identifies quantities, commodity variants, revenues, and ambiguous clauses.
        """
        text_lower = spoken_text.lower()
        expenses: List[ExpenseItem] = []
        unresolved_text = None

        # 1. Detect and separate Ambiguous / Pending Clauses
        # Phrases like: "tel ka dabba udhar pe aaya hai uska bill kal milega"
        ambiguity_pattern = r'(?:lekin|par|magar|aur)?\s*([a-zA-Z\s]+?(?:bill\s+kal|udhar\s+pe|baad\s+mein)[^.]+)'
        amb_match = re.search(ambiguity_pattern, text_lower)
        if amb_match:
            unresolved_text = amb_match.group(1).strip()
            # Remove ambiguous clause from expense processing text
            clean_text = text_lower.replace(amb_match.group(0), " ")
        else:
            clean_text = text_lower

        # 2. Extract Revenue / Total Sales
        revenue = 0.0
        revenue_match = re.search(
            r'(?:total\s+)?(?:gullak|galla|galle|gallay|gulle|scanner|bikri|kamai|sales|collection|bache\s+hain|bane)[^\d]*(\d+(?:,\d+)*(?:\.\d+)?)',
            clean_text
        )
        if not revenue_match:
            revenue_match = re.search(r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:rupay|rs|inr)?\s*(?:ki\s+)?(?:bikri|kamai|sales)', clean_text)

        if revenue_match:
            revenue = float(revenue_match.group(1).replace(",", ""))
        else:
            # Fallback to trailing amount
            end_match = re.search(r'(\d{3,6})\s*(?:rupay|rs|cash)?$', clean_text.strip())
            if end_match:
                revenue = float(end_match.group(1))

        # 3. Extract Itemized Commodities
        sorted_phrases = sorted(COMMODITY_MAPPINGS.keys(), key=len, reverse=True)

        for raw_phrase in sorted_phrases:
            normalized_name, default_unit = COMMODITY_MAPPINGS[raw_phrase]
            if raw_phrase in clean_text and not any(e.item == normalized_name for e in expenses):
                # Check for colloquial quantity prefix like "dedh kilo", "aadha kilo"
                colloquial_qty = None
                for col_word, val in COLLOQUIAL_QUANTITIES.items():
                    if f"{col_word} {raw_phrase}" in clean_text or f"{raw_phrase} {col_word}" in clean_text:
                        colloquial_qty = val
                        break

                # Pattern A: Quantity + Unit + Item + Cost ("10 liter doodh 600 ka", "2 dabba sarson ka tel 1900 ka")
                regex_q_first = rf'(\d+(?:\.\d+)?)\s*(liter|litres|kilo|kg|dabba|can|cans|crate|peti|packet|packets|basket|cylinder)?\s*(?:of\s+)?\b{re.escape(raw_phrase)}\b[^\d]*(\d+(?:\.\d+)?)'

                # Pattern B: Item + Quantity + Unit + Cost ("doodh liya tha 10 liter 600 ka")
                regex_item_first = rf'\b{re.escape(raw_phrase)}\b[^\d]*(\d+(?:\.\d+)?)\s*(liter|litres|kilo|kg|dabba|can|cans|crate|peti|packet|packets|basket|cylinder)?[^\d]*(\d+(?:\.\d+)?)'

                match_q = re.search(regex_q_first, clean_text)
                match_i = re.search(regex_item_first, clean_text)

                matched = None
                if match_q and match_q.group(3) and float(match_q.group(3)) != revenue:
                    matched = match_q
                elif match_i and match_i.group(3) and float(match_i.group(3)) != revenue:
                    matched = match_i

                if matched:
                    qty = colloquial_qty or float(matched.group(1))
                    unit = matched.group(2) or default_unit
                    # Standardize units
                    if unit in ("dabba", "can", "cans"):
                        unit = "cans"
                    elif unit in ("liter", "litres"):
                        unit = "liters"
                    elif unit in ("kilo", "kg"):
                        unit = "kg"
                    elif unit in ("peti", "crate", "crates"):
                        unit = "crates"
                    elif unit in ("cylinder",):
                        unit = "cylinder"

                    cost = float(matched.group(3))
                    unit_price = cost / qty if qty > 0 else cost
                    expenses.append(ExpenseItem(
                        item=normalized_name,
                        raw_name=raw_phrase,
                        quantity=qty,
                        unit=unit,
                        total_cost=cost,
                        unit_price=round(unit_price, 2)
                    ))
                    # Blank out matched text to avoid re-matching sub-phrases (e.g. "tel" after "refined tel")
                    start_pos, end_pos = matched.span()
                    clean_text = clean_text[:start_pos] + (" " * (end_pos - start_pos)) + clean_text[end_pos:]
                else:
                    # Pattern C: Item + Cost without explicit quantity (e.g. "sabzi aayi 450 ki", "barf 150 ki")
                    cost_match = re.search(rf'\b{re.escape(raw_phrase)}\b[^\d]*(\d+(?:\.\d+)?)', clean_text)
                    if cost_match:
                        cost = float(cost_match.group(1))
                        if cost != revenue and cost < 15000:
                            qty = colloquial_qty or 1.0
                            expenses.append(ExpenseItem(
                                item=normalized_name,
                                raw_name=raw_phrase,
                                quantity=qty,
                                unit=default_unit,
                                total_cost=cost,
                                unit_price=round(cost / qty, 2)
                            ))
                            start_pos, end_pos = cost_match.span()
                            clean_text = clean_text[:start_pos] + (" " * (end_pos - start_pos)) + clean_text[end_pos:]

        total_expenses = sum(e.total_cost for e in expenses)
        net_profit = revenue - total_expenses

        return {
            "revenue": revenue,
            "expenses": [e.model_dump() for e in expenses],
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "unresolved_text": unresolved_text
        }

gemma_parser = GemmaParser()
