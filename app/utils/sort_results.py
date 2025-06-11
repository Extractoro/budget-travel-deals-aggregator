from app.schemas.schemas import FilteringParams, SortOrder
from app.utils.parse_fields import parse_duration, parse_price, parse_time


def sort_results(data: dict, filtering: FilteringParams):
    if not isinstance(data, dict) or 'results' not in data or not isinstance(data['results'], list):
        return

    if filtering.hotel_sort is not None:
        hotel_key = filtering.hotel_sort.value
        reverse = filtering.hotel_sort_order == SortOrder.desc

        if hotel_key == 'price':
            hotel_key = 'current_price'

        def safe_sort_key(x):
            value = x.get(hotel_key)
            if hotel_key in ['rating', 'current_price']:
                try:
                    return float(value) if value is not None else 0
                except (ValueError, TypeError):
                    return 0
            return str(value).lower() if value is not None else ""

        data['results'] = sorted(data['results'], key=safe_sort_key, reverse=reverse)

    elif filtering.airline_sort is not None:
        airline_key = filtering.airline_sort.value
        reverse = filtering.airline_sort_order == SortOrder.desc

        for item in data['results']:
            for direction in ['outbound', 'inbound']:
                if direction in item:
                    if airline_key == 'departure_time':
                        item[direction] = sorted(
                            item[direction],
                            key=lambda x: parse_time(x.get('departure_time', '00:00')),
                            reverse=reverse
                        )
                    elif airline_key == 'price':
                        item[direction] = sorted(
                            item[direction],
                            key=lambda x: parse_price(x.get('price', '$0')),
                            reverse=reverse
                        )
                    elif airline_key == 'duration':
                        item[direction] = sorted(
                            item[direction],
                            key=lambda x: parse_duration(x.get('duration', '0h 0m')),
                            reverse=reverse
                        )
