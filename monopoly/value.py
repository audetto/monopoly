from typing import Dict

from monopoly.properties import Properties


def get_player_total_value(player_data: Dict, definitions: Properties) -> int:
    value = player_data['money']
    for prop, data in player_data['properties'].items():
        value += definitions.get_property_value(prop, player_data)
        houses = data['houses']
        if houses:
            value += houses * definitions.get_house_price(prop) // 2
    return value
