from typing import List, Dict, Optional

import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from flask_caching import Cache
from plotly.subplots import make_subplots

from game import Game
from layout import EMPTY_SELECT
from properties import Properties


def get_options_for_player_properties(properties: Dict, definitions: Properties) -> List[Dict]:
    sorted_props = definitions.get_sorted_properties(properties)
    options = EMPTY_SELECT + [{'label': p} for p in sorted_props]
    return options


def register_callbacks(cache: Optional[Cache], app, definitions: Properties, human_players: List[str], bank: str):
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
            Output('json-size', 'children'),
        ],
        [
            Input('game-state', 'data')
        ]
    )
    def draw_state(data: str):
        if not data:
            raise PreventUpdate

        game_state = Game.from_cache(cache, data)
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
            sorted_props = definitions.get_sorted_properties(player_properties)

            rows = [html.Tr([
                html.Td(prop),
                html.Td(player_properties[prop]['houses']),
            ], style=definitions.get_color_style(prop, player_properties)) for prop in sorted_props]
            table = dbc.Table(html.Tbody(rows), size='sm')
            results.append(table)

        progress, msg = game_state.get_progress()

        history, pointer = game_state.get_history(10)
        highlight = {'background-color': 'yellow', 'color': 'red'}
        rows = [html.Tr(html.Td(msg, style=(highlight if i == pointer else None))) for i, msg in history]
        rows.insert(0, html.Tr(html.Th('History')))
        history_table = dbc.Table(html.Tbody(rows), size='sm')

        if cache:
            json_size = f'Game: {data}'
        else:
            json_size = f'Game: {len(data)} bytes'

        return results + [progress * 100, msg, history_table, fig, json_size]

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

        game_state = Game.from_cache(cache, data)
        game = game_state.get_current_game()

        player_data = game[seller]
        tradable_properties = definitions.get_tradable_properties(player_data)
        options = get_options_for_player_properties(tradable_properties, definitions)

        if prop in tradable_properties:
            price = definitions.get_property_value(prop, player_data)
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

        game_state = Game.from_cache(cache, data)
        game = game_state.get_current_game()

        player_data = game[player]
        tradable_properties = definitions.get_tradable_properties(player_data)
        options = get_options_for_player_properties(tradable_properties, definitions)

        if prop and prop in tradable_properties:
            mortgage = tradable_properties[prop]['mortgage']
            unmortgage = not mortgage
        else:
            mortgage = False
            unmortgage = False

        return options, mortgage, unmortgage

    @app.callback(
        [
            Output('houses-property', 'options'),
            Output('buy-house-button', 'disabled'),
            Output('sell-house-button', 'disabled'),
        ],
        [
            Input('game-state', 'data'),
            Input('houses-player', 'value'),
            Input('houses-property', 'value'),
        ]
    )
    def update_houses_property(data: str, player: str, prop: str):
        if not player or not data:
            raise PreventUpdate

        game_state = Game.from_cache(cache, data)
        game = game_state.get_current_game()

        player_data = game[player]
        buildable_properties = definitions.get_buildable_properties(player_data)
        options = get_options_for_player_properties(buildable_properties, definitions)

        if prop and prop in buildable_properties:
            houses = buildable_properties[prop]['houses']
            buy = houses == 5
            sell = houses == 0
        else:
            buy = False
            sell = False

        return options, buy, sell

    @app.callback(
        [
            Output('rent-property', 'options'),
            Output('rent-price', 'value'),
        ],
        [
            Input('game-state', 'data'),
            Input('rent-player', 'value'),
            Input('rent-property', 'value'),
            Input('rent-dice', 'value')
        ]
    )
    def update_rent_property(data: str, player: str, prop: str, dice: int):
        if not player or not data:
            raise PreventUpdate

        game_state = Game.from_cache(cache, data)
        game = game_state.get_current_game()

        rent_properties = definitions.get_rent_properties(player, human_players, game)
        options = get_options_for_player_properties(rent_properties, definitions)

        if prop and prop in rent_properties:
            _, price = definitions.get_rent_for_property(prop, dice, game)
        else:
            price = ''

        return options, price
