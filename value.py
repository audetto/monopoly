from typing import Dict

from properties import get_property_value


def get_player_total_value(player_data: Dict, definitions: Dict) -> int:
    value = player_data['money']
    for prop in player_data['properties']:
        value += get_property_value(prop, player_data, definitions)
    return value
