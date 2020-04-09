import json
from typing import List, Dict

import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate


def pay(game: Dict,
        pay_player: str, receive_player: str, pay_amount: int):

    if pay_player != receive_player:
        game[pay_player]['money'] -= float(pay_amount)
        game[receive_player]['money'] += float(pay_amount)


def trade(game: Dict,
          trade_seller: str, trade_buyer: str, trade_property: str, trade_price: int):

    if trade_seller != trade_buyer:
        seller_properties = game[trade_seller]['properties']
        if trade_property in seller_properties:
            game[trade_seller]['money'] += float(trade_price)
            game[trade_seller]['properties'] = [prop for prop in seller_properties if prop != trade_property]
            game[trade_buyer]['money'] -= float(trade_price)
            game[trade_buyer]['properties'].append(trade_property)


def update_callbacks(app):

    @app.callback(
        Output('game-state', 'data'),
        [
            Input('pay-button', 'n_clicks'),
            Input('trade-button', 'n_clicks'),
        ],
        [
            State('game-state', 'data'),

            State('pay-player', 'value'),
            State('receive-player', 'value'),
            State('pay-amount', 'value'),

            State('trade-seller', 'value'),
            State('trade-buyer', 'value'),
            State('trade-property', 'value'),
            State('trade-price', 'value')
        ]
    )
    def update_game(
            pay_n_clicks: int, trade_n_clicks: int,
            data: str,
            pay_player: str, receive_player: str, pay_amount: int,
            trade_seller: str, trade_buyer: str, trade_property: str, trade_price: int
                    ):
        if not data:
            raise PreventUpdate

        game = json.loads(data)

        triggers = [t['prop_id'] for t in dash.callback_context.triggered]

        if 'pay-button.n_clicks' in triggers and pay_n_clicks:
            pay(game, pay_player, receive_player, pay_amount)
        elif 'trade-button.n_clicks' in triggers and trade_n_clicks:
            trade(game, trade_seller, trade_buyer, trade_property, trade_price)

        return json.dumps(game)
