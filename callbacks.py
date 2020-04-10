import json
from typing import List

import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


def register_callbacks(app, definitions: pd.DataFrame, human_players: List[str], bank: str):
    all_players = human_players + [bank]
    outputs = []
    for player in all_players:
        outputs.append(Output(f'{player}-money', 'value'))
        outputs.append(Output(f'{player}-properties', 'children'))

    @app.callback(
        outputs,
        [
            Input('game-state', 'data')
        ]
    )
    def draw_state(data: str):
        if not data:
            raise PreventUpdate

        game = json.loads(data)
        results = []
        for player in all_players:
            player_data = game[player]
            results.append(player_data['money'])

            rows = [html.Tr(html.Td(prop)) for prop in player_data['properties']]
            table = dbc.Table(html.Tbody(rows), striped=True, size='sm')
            results.append(table)

        return results

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

        game = json.loads(data)

        properties = game[seller]['properties']
        options = [{'label': p} for p in properties]

        df = definitions[definitions['Name'] == prop]
        if not df.empty:
            price = float(definitions[definitions['Name'] == prop]['Price'])
        else:
            price = ''

        return options, price

    @app.callback(
        Output('mortgage-property', 'options'),
        [
            Input('game-state', 'data'),
            Input('mortgage-player', 'value'),
        ]
    )
    def update_trade_property_price(data: str, player: str):
        if not player or not data:
            raise PreventUpdate

        game = json.loads(data)

        properties = game[player]['properties']
        options = [{'label': p} for p in properties]

        return options
