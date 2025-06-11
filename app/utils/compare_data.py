from decimal import Decimal
from typing import List, Dict, Any

from app.models.models import DataTypeEnum


def parse_price(price) -> Decimal | None:
    if price is None:
        return None
    try:
        clean = str(price).replace("$", "").replace("€", "").replace(",", "").strip()
        return Decimal(clean)
    except Exception:
        return None


def compare_flight_lists(old_list: List[Dict], new_list: List[Dict]) -> List[Dict]:
    differences = []
    old_dict = {f["flight_number"]: f for f in old_list}
    new_dict = {f["flight_number"]: f for f in new_list}

    for flight_number in old_dict:
        if flight_number in new_dict:
            old_price = parse_price(old_dict[flight_number]["price"])
            new_price = parse_price(new_dict[flight_number]["price"])
            if old_price != new_price:
                differences.append({
                    "flight_number": flight_number,
                    "price_old": f"{old_price:.2f}",
                    "price_new": f"{new_price:.2f}",
                    "price_diff": f"{'+' if new_price > old_price else '-'}"
                                  f"{abs(new_price - old_price):.2f}"
                })
    return differences


def compare_oneway_flights(old_list: List[Dict], new_list: List[Dict]) -> List[Dict]:
    differences = []
    for old, new in zip(old_list, new_list):
        old_price = parse_price(old.get("price"))
        new_price = parse_price(new.get("price"))
        if old_price != new_price:
            differences.append({
                "departure": old.get("departure"),
                "arrival": old.get("arrival"),
                "departureDate": old.get("departureDate"),
                "price_old": f"{old_price:.2f}",
                "price_new": f"{new_price:.2f}",
                "price_diff": f"{'+' if new_price > old_price else '-'}"
                              f"{abs(new_price - old_price):.2f}",
                "currency": old.get("currency", "EUR")
            })
    return differences


def compare_hotels(old_list: List[Dict], new_list: List[Dict]) -> List[Dict]:
    differences = []
    old_dict = {h["title"]: h for h in old_list}
    new_dict = {h["title"]: h for h in new_list}

    for title in old_dict:
        if title in new_dict:
            old_price = parse_price(old_dict[title].get("current_price"))
            new_price = parse_price(new_dict[title].get("current_price"))
            if old_price is not None and new_price is not None and old_price != new_price:
                differences.append({
                    "title": title,
                    "price_old": f"{old_price:.2f}",
                    "price_new": f"{new_price:.2f}",
                    "price_diff": f"{'+' if new_price > old_price else '-'}"
                                  f"{abs(new_price - old_price):.2f}"
                })
    return differences


def compare_data(
        data_type: DataTypeEnum,
        old_data: List[Dict],
        new_data: List[Dict]
) -> Dict[str, Any]:
    result = {
        "type": data_type.value,
        "differences": {},
        "has_changes": False
    }

    if data_type == DataTypeEnum.FLIGHT:
        outbound_diff = compare_flight_lists(old_data[0].get("outbound", []),
                                             new_data[0].get("outbound", []))
        inbound_diff = compare_flight_lists(old_data[0].get("inbound", []),
                                            new_data[0].get("inbound", []))
        total_diff = new_data[0].get("total_flights", 0) - old_data[0].get("total_flights", 0)

        result["differences"] = {
            "outbound": outbound_diff,
            "inbound": inbound_diff,
            "total_flights_diff": total_diff
        }
        result["has_changes"] = bool(outbound_diff or inbound_diff or total_diff != 0)

    elif data_type == DataTypeEnum.ONEWAY_FLIGHT:
        oneway_diff = compare_oneway_flights(old_data, new_data)
        result["differences"] = oneway_diff
        result["has_changes"] = bool(oneway_diff)

    elif data_type == DataTypeEnum.HOTEL:
        hotel_diff = compare_hotels(old_data, new_data)
        result["differences"] = hotel_diff
        result["has_changes"] = bool(hotel_diff)

    else:
        raise NotImplementedError(f"Comparison not implemented for {data_type}")

    return result
