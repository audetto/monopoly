from typing import List, Dict

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from game import Game
from layout import EMPTY_SELECT
from properties import get_color_style, get_tradable_properties, get_property_value, get_sorted_properties


def get_options_for_player_tradable_properties(properties: Dict, definitions: Dict) -> List[Dict]:
    sorted_props = get_sorted_properties(properties, definitions)
    options = EMPTY_SELECT + [{'label': p} for p in sorted_props]
    return options


def register_callbacks(app, definitions: Dict, human_players: List[str], bank: str):
    all_players = human_players + [bank]
    outputs = []
    for player in all_players:
        outputs.append(Output(f'{player}-money', 'value'))
        outputs.append(Output(f'{player}-total', 'value'))
        outputs.append(Output(f'{player}-properties', 'children'))

    @app.callback(
        outputs + [
            Output('game-progress', 'value'),
            Output('game-progress', 'children'),
            Output('history-table', 'children'),
            Output('history-charts', 'figure'),
        ],
        [
            Input('game-state', 'data')
        ]
    )
    def draw_state(data: str):
        if not data:
            raise PreventUpdate

        game_state = Game.from_json(data)
        game = game_state.get_current_game()

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        results = []
        for player in all_players:
            player_data = game[player]
            money = player_data['money']
            results.append(f'{money:,}')
            total = player_data['total']
            results.append(f'{total:,}')
            ts = game_state.get_player_value_history(player)
            if player == bank:
                fig.add_trace(go.Scatter(y=ts, mode='markers', name=player), secondary_y=True)
            else:
                fig.add_trace(go.Scatter(y=ts, mode='markers+lines', name=player))

            player_properties = player_data['properties']
            sorted_props = get_sorted_properties(player_properties, definitions)

            rows = [html.Tr(html.Td(
                prop,
                style=get_color_style(definitions[prop], player_properties[prop]))) for prop in sorted_props]
            table = dbc.Table(html.Tbody(rows), size='sm')
            results.append(table)

        progress, msg = game_state.get_progress()

        history, pointer = game_state.get_history()
        highlight = {'background-color': 'yellow', 'color': 'red'}
        rows = [html.Tr(html.Td(msg, style=(highlight if i == pointer else None))) for i, msg in enumerate(history)]
        rows.insert(0, html.Tr(html.Th('History')))
        history_table = dbc.Table(html.Tbody(rows), size='sm')

        return results + [progress * 100, msg, history_table, fig]

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

        player_data = game[seller]
        tradable_properties = get_tradable_properties(player_data)
        options = get_options_for_player_tradable_properties(tradable_properties, definitions)

        if prop in tradable_properties:
            price = get_property_value(prop, player_data, definitions)
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
    def update_mortgage_property(data: str, player: str, prop: str):
        if not player or not data:
            raise PreventUpdate

        game_state = Game.from_json(data)
        game = game_state.get_current_game()

        player_data = game[player]
        tradable_properties = get_tradable_properties(player_data)
        options = get_options_for_player_tradable_properties(tradable_properties, definitions)

        if prop and prop in tradable_properties:
            mortgage = tradable_properties[prop]['mortgage']
            unmortgage = not mortgage
        else:
            mortgage = False
            unmortgage = False

        return options, mortgage, unmortgage
