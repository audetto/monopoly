import os.path
from typing import Dict, List, Tuple

import pandas as pd


class Properties:
    FOREGROUND = {'Brown': 'white', 'Dark Blue': 'white'}
    HOUSES = ['1 house', '2 houses', '3 houses', '4 houses', 'hotel']
    STATION_RENT = [1, 2, 4, 8]
    UTILITY_RENT = [4, 10]

    def __init__(self):
        file_name = "properties.csv"
        this_folder = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(this_folder, file_name)
        static = pd.read_csv(path, index_col='name')
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

    def get_tradable_properties(self, player_data: Dict) -> Dict:
        # can only sell or mortgage properties with no houses
        built_groups = {self.data[k]['color'] for k, v in player_data['properties'].items() if v['houses'] > 0}
        properties = {k: v for k, v in player_data['properties'].items() if self.data[k]['color'] not in built_groups}
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

    def get_rent_properties(self, player: str, humans: List[str], game: Dict) -> Dict:
        result = {}
        for human in humans:
            if human != player:
                human_data = game[human]
                for prop, data in human_data['properties'].items():
                    if not data['mortgage']:
                        result[prop] = self.data[prop]
        return result

    def get_rent_for_property(self, prop: str, dice: int, game: Dict) -> Tuple[str, int]:
        owner = None
        for player, data in game.items():
            if prop in data['properties']:
                owner = player
                break

        owner_properties = game[owner]['properties']
        if owner_properties[prop]['mortgage']:
            rent = 0
        else:
            prop_data = self.data[prop]
            number_of_houses = owner_properties[prop]['houses']
            if number_of_houses > 0:
                rent = prop_data[self.HOUSES[number_of_houses - 1]]
            else:
                owned = [k for k in owner_properties if self.data[k]['color'] == prop_data['color']]
                rent = prop_data['rent']
                if prop_data['rule'] == 'Normal':
                    if len(owned) == self.groups[prop_data['color']]:
                        rent *= 2
                elif prop_data['rule'] == 'Station':
                    rent *= self.STATION_RENT[len(owned) - 1]
                elif prop_data['rule'] == 'Utility':
                    rent = dice * self.UTILITY_RENT[len(owned) - 1]
        return owner, int(rent)
