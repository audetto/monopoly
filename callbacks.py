import json
from typing import List

import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.exceptions import PreventUpdate


def register_callbacks(app, human_players: List[str], bank: str):

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
            Output('trade-property', 'value'),
            Output('trade-price', 'value'),
        ],
        [
            Input('trade-seller', 'value'),
            Input('game-state', 'data')
        ]
    )
    def update_trade_property_price(seller: str, data: str):
        if not seller or not data:
            raise PreventUpdate

        game = json.loads(data)
        properties = game[seller]['properties']
        options = [{'label': prop} for prop in properties]
        price = 1234 + len(properties)
        return options, '', price
