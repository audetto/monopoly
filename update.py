import json
from typing import Dict

import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate


def pay(game: Dict,
        pay_player: str, receive_player: str, pay_amount: int):
    if pay_player != receive_player and pay_amount:
        game[pay_player]['money'] -= pay_amount
        game[receive_player]['money'] += pay_amount


def go(game: Dict, bank: str,
       extra_player: str):
    if extra_player:
        game[extra_player]['money'] += 200
        game[bank]['money'] -= 200


def income_tax(game: Dict, bank: str,
               extra_player: str):
    if extra_player:
        game[extra_player]['money'] -= 200
        game[bank]['money'] += 200


def super_tax(game: Dict, bank: str,
              extra_player: str):
    if extra_player:
        game[extra_player]['money'] -= 100
        game[bank]['money'] += 100


def out_of_jail(game: Dict, bank: str,
                extra_player: str):
    if extra_player:
        game[extra_player]['money'] -= 50
        game[bank]['money'] += 50


def trade(game: Dict,
          trade_seller: str, trade_buyer: str, trade_property: str, trade_price: int):
    if trade_seller != trade_buyer and trade_price:
        seller_properties = game[trade_seller]['properties']
        if trade_property in seller_properties:
            game[trade_seller]['money'] += trade_price
            game[trade_buyer]['properties'][trade_property] = game[trade_seller]['properties'][trade_property]
            del game[trade_seller]['properties'][trade_property]
            game[trade_buyer]['money'] -= trade_price


def mortgage(game: Dict, definitions: Dict, bank: str,
             mortgage_player: str, mortgage_property: str):
    if mortgage_player and mortgage_property:
        player_data = game[mortgage_player]
        if not player_data['properties'][mortgage_property]['mortgage']:
            definition = definitions[mortgage_property]
            price = definition['price'] / 2
            player_data['properties'][mortgage_property]['mortgage'] = True
            player_data['money'] += price
            game[bank]['money'] -= price


def unmortgage(game: Dict, definitions: Dict, bank: str,
               mortgage_player: str, mortgage_property: str):
    if mortgage_player and mortgage_property:
        player_data = game[mortgage_player]
        if player_data['properties'][mortgage_property]['mortgage']:
            definition = definitions[mortgage_property]
            price = definition['price'] * 11 / 20
            player_data['properties'][mortgage_property]['mortgage'] = False
            player_data['money'] -= price
            game[bank]['money'] += price


def update_callbacks(app, definitions: Dict, bank: str):
    @app.callback(
        Output('game-state', 'data'),
        [
            Input('pay-button', 'n_clicks'),
            Input('trade-button', 'n_clicks'),
            Input('go-button', 'n_clicks'),
            Input('income-tax-button', 'n_clicks'),
            Input('super-tax-button', 'n_clicks'),
            Input('out-of-jail-button', 'n_clicks'),
            Input('mortgage-button', 'n_clicks'),
            Input('unmortgage-button', 'n_clicks'),
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
            super_tax_n_clicks: int, out_of_jail_n_clicks: int, mortgage_n_clicks: int, unmortgage_n_clicks: int,
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
            go(game, bank, extra_player)
        elif 'income-tax-button.n_clicks' in triggers and income_tax_n_clicks:
            income_tax(game, bank, extra_player)
        elif 'super-tax-button.n_clicks' in triggers and super_tax_n_clicks:
            super_tax(game, bank, extra_player)
        elif 'out-of-jail-button.n_clicks' in triggers and out_of_jail_n_clicks:
            out_of_jail(game, bank, extra_player)
        elif 'mortgage-button.n_clicks' in triggers and mortgage_n_clicks:
            mortgage(game, definitions, bank, mortgage_player, mortgage_property)
        elif 'unmortgage-button.n_clicks' in triggers and unmortgage_n_clicks:
            unmortgage(game, definitions, bank, mortgage_player, mortgage_property)

        return json.dumps(game)
