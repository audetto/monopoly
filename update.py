import json
from typing import List, Dict

import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate


def pay(game: Dict,
        pay_player: str, receive_player: str, pay_amount: str):

    if pay_player != receive_player and pay_amount:
        game[pay_player]['money'] -= float(pay_amount)
        game[receive_player]['money'] += float(pay_amount)


def go(game: Dict,
       extra_player: str, bank: str):

    if extra_player:
        game[extra_player]['money'] += 200
        game[bank]['money'] -= 200


def income_tax(game: Dict,
               extra_player: str, bank: str):

    if extra_player:
        game[extra_player]['money'] -= 200
        game[bank]['money'] += 200


def super_tax(game: Dict,
              extra_player: str, bank: str):

    if extra_player:
        game[extra_player]['money'] -= 100
        game[bank]['money'] += 100


def out_of_jail(game: Dict,
                extra_player: str, bank: str):

    if extra_player:
        game[extra_player]['money'] -= 50
        game[bank]['money'] += 50


def trade(game: Dict,
          trade_seller: str, trade_buyer: str, trade_property: str, trade_price: str):

    if trade_seller != trade_buyer and trade_price:
        seller_properties = game[trade_seller]['properties']
        if trade_property in seller_properties:
            game[trade_seller]['money'] += float(trade_price)
            game[trade_seller]['properties'] = [prop for prop in seller_properties if prop != trade_property]
            game[trade_buyer]['money'] -= float(trade_price)
            game[trade_buyer]['properties'].append(trade_property)


def update_callbacks(app, bank: str):

    @app.callback(
        Output('game-state', 'data'),
        [
            Input('pay-button', 'n_clicks'),
            Input('trade-button', 'n_clicks'),
            Input('go-button', 'n_clicks'),
            Input('income-tax-button', 'n_clicks'),
            Input('super-tax-button', 'n_clicks'),
            Input('out-of-jail-button', 'n_clicks'),
        ],
        [
            State('game-state', 'data'),

            State('pay-player', 'value'),
            State('receive-player', 'value'),
            State('pay-amount', 'value'),

            State('trade-seller', 'value'),
            State('trade-buyer', 'value'),
            State('trade-property', 'value'),
            State('trade-price', 'value'),
            
            State('extra-player', 'value'),
            
            State('mortgage-player', 'value'),
            State('mortgage-property', 'value'),
        ]
    )
    def update_game(
            pay_n_clicks: int, trade_n_clicks: int, go_n_clicks: int, income_tax_n_clicks: int,
            super_tax_n_clicks: int, out_of_jail_n_clicks: int,
            data: str,
            pay_player: str, receive_player: str, pay_amount: str,
            trade_seller: str, trade_buyer: str, trade_property: str, trade_price: str,
            extra_player: str,
            mortgage_player: str, mortgage_property: str,
                    ):
        if not data:
            raise PreventUpdate

        game = json.loads(data)

        triggers = [t['prop_id'] for t in dash.callback_context.triggered]

        if 'pay-button.n_clicks' in triggers and pay_n_clicks:
            pay(game, pay_player, receive_player, pay_amount)
        elif 'trade-button.n_clicks' in triggers and trade_n_clicks:
            trade(game, trade_seller, trade_buyer, trade_property, trade_price)
        elif 'go-button.n_clicks' in triggers and go_n_clicks:
            go(game, extra_player, bank)
        elif 'income-tax-button.n_clicks' in triggers and income_tax_n_clicks:
            income_tax(game, extra_player, bank)
        elif 'super-tax-button.n_clicks' in triggers and super_tax_n_clicks:
            super_tax(game, extra_player, bank)
        elif 'out-of-jail-button.n_clicks' in triggers and out_of_jail_n_clicks:
            out_of_jail(game, extra_player, bank)

        return json.dumps(game)
