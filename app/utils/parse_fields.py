from datetime import datetime


def parse_time(t: str):
    try:
        return datetime.strptime(t, "%H:%M").time()
    except Exception:
        return datetime.min.time()


def parse_duration(duration_str: str) -> int:
    try:
        parts = duration_str.lower().split()
        minutes = 0
        for part in parts:
            if 'h' in part:
                minutes += int(part.replace('h', '')) * 60
            elif 'm' in part:
                minutes += int(part.replace('m', ''))
        return minutes
    except Exception:
        return 0


def parse_price(price_str):
    if not price_str:
        return None
    digits = ''.join(ch for ch in price_str if ch.isdigit())
    return float(digits) if digits else None
