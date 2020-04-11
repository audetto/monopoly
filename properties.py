from typing import Dict, List

import pandas as pd


class Properties:

    FOREGROUND = {'Brown': 'white', 'Dark Blue': 'white'}

    def __init__(self):
        file_name = "properties.csv"
        static = pd.read_csv(file_name, index_col='name')
        self.data = static.to_dict(orient='index')
        self.groups = static.groupby('color')['rule'].count().to_dict()

    def get_color_style(self, prop: str, data: Dict) -> Dict:
        group = self.data[prop]['color']
        background = group.replace(' ', '')
        foreground = self.FOREGROUND.get(group, 'black')
        style = {'background-color': background, 'color': foreground}
    
        if data[prop]['mortgage']:
            style['opacity'] = 0.2
    
        return style
    
    @staticmethod
    def get_tradable_properties(player_data: Dict) -> Dict:
        # can only sell or mortgage properties with no houses
        properties = {k: v for k, v in player_data['properties'].items() if v['houses'] == 0}
        return properties
    
    def get_buildable_properties(self, player_data: Dict) -> Dict:
        owned = {}
        for prop, prop_data in player_data['properties'].items():
            rule = self.data[prop]['rule']
            if rule == 'Normal':
                if not prop_data['mortgage']:
                    color = self.data[prop]['color']
                    if color not in owned:
                        owned[color] = 0
                    owned[color] += 1

        buildable_groups = {color for color, count in owned.items() if count == self.groups[color]}

        # can only sell or mortgage properties with no houses
        properties = {k: v for k, v in player_data['properties'].items() if self.data[k]['color'] in buildable_groups}
        return properties
    
    def get_property_value(self, prop: str, player_data: Dict) -> int:
        is_mortgaged = player_data['properties'][prop]['mortgage']
        price = self.data[prop]['price']
        if is_mortgaged:
            # deduct interests
            price = price * 45 // 100
        return int(price)
    
    def get_redemption_cost(self, prop: str) -> int:
        value = self.data[prop]['price'] * 11 // 20
        return int(value)
    
    def get_mortgage_value(self, prop: str) -> int:
        value = self.data[prop]['price'] // 2
        return int(value)

    def get_house_price(self, prop: str) -> int:
        price = self.data[prop]['house price']
        return int(price)

    def get_sorted_properties(self, properties: Dict) -> List[str]:
        def value(prop: str) -> int:
            return self.data[prop]['price']
        s = sorted(properties.keys(), key=value)
        return s
