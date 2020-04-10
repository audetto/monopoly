from typing import Dict

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
