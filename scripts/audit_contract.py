"""Static contract helpers only; no producer, features, training or scoring.

Parser and endpoint helper are retained from V1 as historical semantic evidence.
Their existence does not freeze V2 business-hour parsing. Complete eligibility
still requires agreed sample/history/quality checks in DELTA's future producer.
"""
import re


def parse_stock_status(text):
    """Parse the exported NumPy-like binary vector without eval or code execution."""
    text = text.strip()
    if not (text.startswith("[") and text.endswith("]")):
        raise ValueError("Stock-status vector must be bracketed")
    tokens = re.split(r"[\s,]+", text[1:-1].strip())
    if len(tokens) != 24 or any(token not in {"0", "1"} for token in tokens):
        raise ValueError("Stock-status vector must have 24 binary hour entries")
    return [int(token) for token in tokens]


def business_stockout_hours(status):
    """Business interval is 06:00 inclusive to 22:00 exclusive (16 entries)."""
    return sum(status[6:22])


def candidate_history_reason(day_number, history_days=14):
    """Check only the approved candidate-history boundary, never target stockouts.

    This is not a complete eligibility implementation. Callers must not interpret
    'candidate' as data-quality/sample acceptance.
    """
    if history_days != 14:
        raise ValueError("Primary V2 history is 14 days; sensitivities need a separate policy")
    if isinstance(day_number, bool) or not isinstance(day_number, int) or not 1 <= day_number <= 90:
        raise ValueError("Expected project day 1 through 90")
    return "insufficient_14_day_history" if day_number <= history_days else "candidate"
