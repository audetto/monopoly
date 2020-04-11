from typing import Dict, List

import pandas as pd


FOREGROUND = {'Brown': 'white', 'Dark Blue': 'white'}


def get_properties() -> Dict:
    file_name = "properties.csv"
    df = pd.read_csv(file_name, index_col='name')
    result = df.to_dict(orient='index')
    return result


def get_color_style(definition: Dict, data: Dict) -> Dict:
    group = definition['color']
    background = group.replace(' ', '')
    foreground = FOREGROUND.get(group, 'black')
    style = {'background-color': background, 'color': foreground}

    if data['mortgage']:
        style['opacity'] = 0.2

    return style


def get_tradable_properties(player_data: Dict) -> Dict:
    # can only sell or mortgage properties with no houses
    properties = {k: v for k, v in player_data['properties'].items() if v['houses'] == 0}
    return properties


def get_property_value(prop: str, player_data: Dict, definitions: Dict) -> int:
    is_mortgaged = player_data['properties'][prop]['mortgage']
    price = definitions[prop]['price']
    if is_mortgaged:
        # deduct interests
        price = price * 45 // 100
    return price


def get_redemption_cost(prop: str, definitions: Dict) -> int:
    value = definitions[prop]['price'] * 11 // 20
    return value


def get_mortgage_value(prop: str, definitions: Dict) -> int:
    value = definitions[prop]['price'] // 2
    return value


def get_sorted_properties(properties: Dict, definitions: Dict) -> List[str]:
    def value(prop: str) -> int:
        return definitions[prop]['price']
    s = sorted(properties.keys(), key=value)
    return s
