from typing import List, Dict

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from game import Game
from properties import get_color_style


def register_callbacks(app, definitions: Dict, human_players: List[str], bank: str):
    all_players = human_players + [bank]
    outputs = []
    for player in all_players:
        outputs.append(Output(f'{player}-money', 'value'))
        outputs.append(Output(f'{player}-properties', 'children'))

    @app.callback(
        outputs + [Output('game-progress', 'value'), Output('game-progress', 'children')],
        [
            Input('game-state', 'data')
        ]
    )
    def draw_state(data: str):
        if not data:
            raise PreventUpdate

        game_state = Game.from_json(data)
        game = game_state.get_current_game()

        results = []
        for player in all_players:
            player_data = game[player]
            money = player_data['money']
            results.append(f'{money:,}')

            rows = [html.Tr(html.Td(
                prop,
                style=get_color_style(definitions[prop], prop_data))) for prop, prop_data in player_data['properties'].items()]
            table = dbc.Table(html.Tbody(rows), size='sm')
            results.append(table)

        progress, msg = game_state.get_progress()

        return results + [progress * 100, msg]

    @app.callback(
        [
            Output('trade-property', 'options'),
            Output('trade-price', 'value'),
        ],
        [
            Input('game-state', 'data'),
            Input('trade-seller', 'value'),
            Input('trade-property', 'value'),
        ]
    )
    def update_trade_property_price(data: str, seller: str, prop: str):
        if not seller or not data:
            raise PreventUpdate

        game_state = Game.from_json(data)
        game = game_state.get_current_game()

        properties = game[seller]['properties']
        options = [{'label': p} for p, d in properties.items() if d['houses'] == 0]

        if prop in properties:
            is_mortgaged = properties[prop]['mortgage']
            price = definitions[prop]['price']
            if is_mortgaged:
                price = price * 45 / 100
        else:
            price = ''

        return options, price

    @app.callback(
        [
            Output('mortgage-property', 'options'),
            Output('mortgage-button', 'disabled'),
            Output('unmortgage-button', 'disabled'),
        ],
        [
            Input('game-state', 'data'),
            Input('mortgage-player', 'value'),
            Input('mortgage-property', 'value'),
        ]
    )
    def update_mortgage_property(data: str, player: str, property: str):
        if not player or not data:
            raise PreventUpdate

        game_state = Game.from_json(data)
        game = game_state.get_current_game()

        properties = game[player]['properties']
        options = [{'label': p} for p, d in properties.items() if d['houses'] == 0]

        mortgage = False
        unmortgage = False
        if property and property in properties:
            mortgage = properties[property]['mortgage']
            unmortgage = not mortgage

        return options, mortgage, unmortgage
