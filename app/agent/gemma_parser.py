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
    "bhada": ("transport rent", "trip"),
    # Eggs & Bakery
    "eggs": ("eggs", "tray"),
    "egg": ("eggs", "tray"),
    "ande": ("eggs", "tray"),
    "anda": ("eggs", "tray"),
    "bread": ("bread", "packets"),
    "bun": ("bun", "packets"),
    "buns": ("bun", "packets"),
    "pav": ("pav", "packets"),
    "paav": ("pav", "packets")
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

ENGLISH_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}

HINDI_NUMBERS = {
    "ek": 1, "do": 2, "teen": 3, "char": 4, "chaar": 4, "paanch": 5, "panch": 5,
    "chhe": 6, "che": 6, "saat": 7, "aath": 8, "nau": 9, "das": 10,
    "gyarah": 11, "barah": 12, "terah": 13, "chaudah": 14, "pandrah": 15,
    "solah": 16, "satrah": 17, "atharah": 18, "unnis": 19, "bees": 20,
    "pachees": 25, "tees": 30, "paintees": 35, "chalis": 40, "pachaas": 50,
    "pachas": 50, "saath": 60, "sattar": 70, "pachattar": 75, "assi": 80, "nabbe": 90,
    # Devanagari numerals
    "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पाँच": 5, "पांच": 5, "छह": 6,
    "सात": 7, "आठ": 8, "नौ": 9, "दस": 10, "पचास": 50, "पचहत्तर": 75,
}

NUMBER_SCALES = {
    "hundred": 100, "sau": 100, "सौ": 100,
    "thousand": 1000, "hazaar": 1000, "hazar": 1000, "हज़ार": 1000, "हजार": 1000,
    "lakh": 100000, "lac": 100000, "लाख": 100000,
}

ALL_NUM_WORDS = {**ENGLISH_NUMBERS, **HINDI_NUMBERS, **NUMBER_SCALES}

def parse_number_phrase(tokens: List[str]) -> int:
    total = 0
    current = 0
    for tok in tokens:
        if tok in ("and", "aur", "और"):
            continue
        if tok in NUMBER_SCALES:
            scale = NUMBER_SCALES[tok]
            if current == 0:
                current = 1
            current *= scale
            if scale >= 1000:
                total += current
                current = 0
        elif tok in ALL_NUM_WORDS:
            val = ALL_NUM_WORDS[tok]
            current += val
        elif tok.isdigit():
            val = int(tok)
            if val < 100 and current >= 100:
                current += val
            else:
                total += current
                current = val
    total += current
    return total

def normalize_spoken_numbers(text: str) -> str:
    # 0. Replace Devanagari digits (०-९) with ASCII (0-9)
    dev_digits = str.maketrans("०१२३४५६७८९", "0123456789")
    text = text.translate(dev_digits)

    # 0b. Multi-word colloquial expressions (dedh sau -> 150, dhai sau -> 250)
    for phrase, num_val in [
        ("dedh hazaar", "1500"), ("dedh hazar", "1500"),
        ("dhai hazaar", "2500"), ("dhai hazar", "2500"),
        ("dedh sau", "150"), ("dhai sau", "250"),
        ("sawa sau", "125"), ("paune do sau", "175"),
    ]:
        text = re.sub(rf'\b{phrase}\b', num_val, text, flags=re.IGNORECASE)

    # 1. Fix STT concatenation artifact like '30075' -> '375', '10050' -> '150', '20045' -> '245'
    text = re.sub(r'\b([1-9])00([1-9]\d)\b', r'\g<1>\g<2>', text)
    text = re.sub(r'\b([1-9])00([1-9])\b', r'\g<1>0\g<2>', text)

    # 2. Fix spaced compound numbers from STT like '300 75' -> '375', '1000 500' -> '1500'
    def sum_two_nums(m):
        return str(int(m.group(1)) + int(m.group(2)))
    text = re.sub(r'\b([1-9]\d*00)\s+([1-9]\d?)\b', sum_two_nums, text)
    text = re.sub(r'\b([1-9]\d*000)\s+([1-9]\d{1,2})\b', sum_two_nums, text)

    # 3. Parse sequences of word numbers
    tokens = text.lower().split()
    i = 0
    out_tokens = []
    while i < len(tokens):
        tok = tokens[i].strip('.,!?:;')
        if tok in ALL_NUM_WORDS:
            num_seq = [tok]
            j = i + 1
            while j < len(tokens):
                next_tok = tokens[j].strip('.,!?:;')
                if next_tok in ALL_NUM_WORDS or (next_tok in ("and", "aur", "और") and j + 1 < len(tokens) and tokens[j+1].strip('.,!?:;') in ALL_NUM_WORDS):
                    num_seq.append(next_tok)
                    j += 1
                else:
                    break
            val = parse_number_phrase(num_seq)
            out_tokens.append(str(val))
            i = j
        else:
            out_tokens.append(tokens[i])
            i += 1

    result = " ".join(out_tokens)
    result = re.sub(r'\b([1-9]\d*00)\s+([1-9]\d?)\b', sum_two_nums, result)
    result = re.sub(r'\b([1-9]\d*000)\s+([1-9]\d{1,2})\b', sum_two_nums, result)
    result = re.sub(r'\b([1-9])00([1-9]\d)\b', r'\g<1>\g<2>', result)
    return result

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
        # 0. Pre-normalize spoken numbers and speech-to-text artifacts
        normalized_text = normalize_spoken_numbers(spoken_text)
        text_lower = normalized_text.lower()
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
        rev_forward_regex = (
            r'(?:total\s+|today\'?s\s+|meri\s+|mera\s+|my\s+)?'
            r'(?:gullak|galla|galle|gallay|gulle|scanner|bikri|kamai|kamaye|aamdani|sales|sale|revenue|collection|intake|income|turnover|bache\s+hain|bane|aaye)'
            r'[^\d]{0,35}?'
            r'(\d+(?:,\d+)*(?:\.\d+)?)'
        )
        rev_reverse_regex = (
            r'(\d+(?:,\d+)*(?:\.\d+)?)\s*'
            r'(?:rs\.?|rupees|rupay|rupaye|inr|₹)?\s*'
            r'(?:ki|in|of|ke)?\s*'
            r'(?:bikri|kamai|kamaye|aamdani|sales|sale|revenue|collection|intake|turnover)'
        )

        rev_match = re.search(rev_forward_regex, clean_text)
        if not rev_match:
            rev_match = re.search(rev_reverse_regex, clean_text)

        if rev_match:
            revenue = float(rev_match.group(1).replace(",", ""))
            # Blank out matched revenue span to avoid cross-contaminating expense costs
            start_pos, end_pos = rev_match.span()
            clean_text = clean_text[:start_pos] + (" " * (end_pos - start_pos)) + clean_text[end_pos:]
        else:
            # Fallback to trailing amount
            end_match = re.search(r'(\d{3,6})\s*(?:rupay|rupees|rs\.?|inr|₹|cash)?$', clean_text.strip())
            if end_match:
                revenue = float(end_match.group(1))
                start_pos, end_pos = end_match.span()
                clean_text = clean_text[:start_pos] + (" " * (end_pos - start_pos)) + clean_text[end_pos:]

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
                regex_q_first = rf'(\d+(?:\.\d+)?)\s*(liter|litres|kilo|kg|dabba|can|cans|crate|peti|packet|packets|basket|cylinder|tray|dozens?)?\s*(?:of\s+)?\b{re.escape(raw_phrase)}\b[^\d]*?(\d+(?:\.\d+)?)'

                # Pattern B: Item + Quantity + Unit + Cost ("doodh liya tha 10 liter 600 ka")
                # Unit is required so item doesn't eat the next commodity
                regex_item_first = rf'\b{re.escape(raw_phrase)}\b[^\d,;.]*?(\d+(?:\.\d+)?)\s+(liter|litres|kilo|kg|dabba|can|cans|crate|peti|packet|packets|basket|cylinder|tray|dozens?)\b[^\d,;.]*?(\d+(?:\.\d+)?)'

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
                    elif unit in ("tray", "dozens", "dozen"):
                        unit = "tray"

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
                    # Pattern C: Item + Cost without explicit quantity (e.g. "sabzi aayi 450 ki", "barf 150 ki", "milk for 200", "eggs for 150")
                    cost_match = re.search(rf'\b{re.escape(raw_phrase)}\b\s*(?:ka|ki|ke|liya|aayi|aaya|for|cost|worth|of)?\s*(?:rs\.?|rupees|rupay|rupaye|inr|₹)?\s*[:=]?\s*(\d+(?:\.\d+)?)', clean_text)
                    if not cost_match:
                        cost_match = re.search(rf'\b{re.escape(raw_phrase)}\b[^\d,;.]*?(\d+(?:\.\d+)?)', clean_text)

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
