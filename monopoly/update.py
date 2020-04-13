import copy
from typing import Dict, List, Optional

import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from flask_caching import Cache

from monopoly.game import Game
from monopoly.properties import Properties


def pay(game: Dict, human_players: List[str],
        pay_player: str, receive_player: str, pay_amount: int) -> str:
    if pay_player != receive_player and pay_amount:
        if pay_player == 'ALL':
            for player in human_players:
                game[player]['money'] -= pay_amount
                game[receive_player]['money'] += pay_amount
        elif receive_player == 'ALL':
            for player in human_players:
                game[pay_player]['money'] -= pay_amount
                game[player]['money'] += pay_amount
        else:
            game[pay_player]['money'] -= pay_amount
            game[receive_player]['money'] += pay_amount
        return f'{pay_player} give {receive_player} {pay_amount}M$'


def go(game: Dict, bank: str,
       extra_player: str):
    if extra_player:
        game[extra_player]['money'] += 200
        game[bank]['money'] -= 200
        return f'{extra_player} passes GO'


def income_tax(game: Dict, bank: str,
               extra_player: str):
    if extra_player:
        game[extra_player]['money'] -= 200
        game[bank]['money'] += 200
        return f'{extra_player} pays Income Tax'


def super_tax(game: Dict, bank: str,
              extra_player: str):
    if extra_player:
        game[extra_player]['money'] -= 100
        game[bank]['money'] += 100
        return f'{extra_player} pays Super Tax'


def out_of_jail(game: Dict, bank: str,
                extra_player: str):
    if extra_player:
        game[extra_player]['money'] -= 50
        game[bank]['money'] += 50
        return f'{extra_player} gets out of jail'


def trade(game: Dict,
          trade_seller: str, trade_buyer: str, trade_property: str, trade_price: int):
    if trade_seller != trade_buyer and trade_price:
        seller_properties = game[trade_seller]['properties']
        if trade_property in seller_properties:
            game[trade_seller]['money'] += trade_price
            game[trade_buyer]['properties'][trade_property] = game[trade_seller]['properties'][trade_property]
            del game[trade_seller]['properties'][trade_property]
            game[trade_buyer]['money'] -= trade_price
            return f'{trade_seller} sells {trade_property} to {trade_buyer} for {trade_price}M$'


def mortgage(game: Dict, definitions: Properties, bank: str,
             mortgage_player: str, mortgage_property: str):
    if mortgage_player and mortgage_property:
        player_data = game[mortgage_player]
        if not player_data['properties'][mortgage_property]['mortgage']:
            price = definitions.get_mortgage_value(mortgage_property)
            player_data['properties'][mortgage_property]['mortgage'] = True
            player_data['money'] += price
            game[bank]['money'] -= price
            return f'{mortgage_player} mortgages {mortgage_property} for {price}M$'


def buy_house(game: Dict, definitions: Properties, bank: str,
              houses_player: str, houses_property: str):
    if houses_player and houses_property:
        player_data = game[houses_player]
        if player_data['properties'][houses_property]['houses'] < 5:
            price = definitions.get_house_price(houses_property)
            player_data['properties'][houses_property]['houses'] += 1
            player_data['money'] -= price
            game[bank]['money'] += price
            return f'{houses_player} buys a house on {houses_property} for {price}M$'


def sell_house(game: Dict, definitions: Properties, bank: str,
               houses_player: str, houses_property: str):
    if houses_player and houses_property:
        player_data = game[houses_player]
        if player_data['properties'][houses_property]['houses'] > 0:
            price = definitions.get_house_price(houses_property) // 2
            player_data['properties'][houses_property]['houses'] -= 1
            player_data['money'] += price
            game[bank]['money'] -= price
            return f'{houses_player} buys a house on {houses_property} for {price}M$'


def pay_rent(game: Dict, definitions: Properties,
             rent_player: str, rent_property: str, rent_dice: int):
    if rent_player and rent_property:
        owner, price = definitions.get_rent_for_property(rent_property, rent_dice, game)
        if rent_player != owner and price:
            game[rent_player]['money'] -= price
            game[owner]['money'] += price
            return f'{rent_player} pays rent on {rent_property} to {owner} for {price}M$'


def unmortgage(game: Dict, definitions: Properties, bank: str,
               mortgage_player: str, mortgage_property: str):
    if mortgage_player and mortgage_property:
        player_data = game[mortgage_player]
        if player_data['properties'][mortgage_property]['mortgage']:
            price = definitions.get_redemption_cost(mortgage_property)
            player_data['properties'][mortgage_property]['mortgage'] = False
            player_data['money'] -= price
            game[bank]['money'] += price
            return f'{mortgage_player} unmortgages {mortgage_property} for {price}M$'


def update_callbacks(cache: Optional[Cache], app, definitions: Properties, human_players: List[str], bank: str):
    @app.callback(
        Output('game-state', 'data'),
        [
            Input('backward-button', 'n_clicks'),
            Input('forward-button', 'n_clicks'),
            Input('pay-button', 'n_clicks'),
            Input('trade-button', 'n_clicks'),
            Input('go-button', 'n_clicks'),
            Input('income-tax-button', 'n_clicks'),
            Input('super-tax-button', 'n_clicks'),
            Input('out-of-jail-button', 'n_clicks'),
            Input('mortgage-button', 'n_clicks'),
            Input('unmortgage-button', 'n_clicks'),
            Input('buy-house-button', 'n_clicks'),
            Input('sell-house-button', 'n_clicks'),
            Input('pay-rent-button', 'n_clicks'),
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

            State('houses-player', 'value'),
            State('houses-property', 'value'),

            State('rent-player', 'value'),
            State('rent-property', 'value'),
            State('rent-dice', 'value')
        ]
    )
    def update_game(
            backward_n_clicks: int, forward_n_clicks: int,
            pay_n_clicks: int, trade_n_clicks: int, go_n_clicks: int, income_tax_n_clicks: int,
            super_tax_n_clicks: int, out_of_jail_n_clicks: int, mortgage_n_clicks: int, unmortgage_n_clicks: int,
            buy_house_n_clicks: int, sell_house_n_clicks: int,
            pay_rent_n_clicks: int,
            data: str,
            pay_player: str, receive_player: str, pay_amount: int,
            trade_seller: str, trade_buyer: str, trade_property: str, trade_price: int,
            extra_player: str,
            mortgage_player: str, mortgage_property: str,
            houses_player: str, houses_property: str,
            rent_player: str, rent_property: str, rent_dice: int,
    ):
        if not data:
            raise PreventUpdate

        game_state = Game.from_cache(cache, data)

        triggers = [t['prop_id'] for t in dash.callback_context.triggered]

        if 'backward-button.n_clicks' in triggers and backward_n_clicks:
            game_state.move(-1)
        elif 'forward-button.n_clicks' in triggers and forward_n_clicks:
            game_state.move(1)
        else:
            org_game = game_state.get_current_game()
            game = copy.deepcopy(org_game)

            if 'pay-button.n_clicks' in triggers and pay_n_clicks:
                msg = pay(game, human_players, pay_player, receive_player, pay_amount)
            elif 'trade-button.n_clicks' in triggers and trade_n_clicks:
                msg = trade(game, trade_seller, trade_buyer, trade_property, trade_price)
            elif 'go-button.n_clicks' in triggers and go_n_clicks:
                msg = go(game, bank, extra_player)
            elif 'income-tax-button.n_clicks' in triggers and income_tax_n_clicks:
                msg = income_tax(game, bank, extra_player)
            elif 'super-tax-button.n_clicks' in triggers and super_tax_n_clicks:
                msg = super_tax(game, bank, extra_player)
            elif 'out-of-jail-button.n_clicks' in triggers and out_of_jail_n_clicks:
                msg = out_of_jail(game, bank, extra_player)
            elif 'mortgage-button.n_clicks' in triggers and mortgage_n_clicks:
                msg = mortgage(game, definitions, bank, mortgage_player, mortgage_property)
            elif 'unmortgage-button.n_clicks' in triggers and unmortgage_n_clicks:
                msg = unmortgage(game, definitions, bank, mortgage_player, mortgage_property)
            elif 'buy-house-button.n_clicks' in triggers and buy_house_n_clicks:
                msg = buy_house(game, definitions, bank, houses_player, houses_property)
            elif 'sell-house-button.n_clicks' in triggers and sell_house_n_clicks:
                msg = sell_house(game, definitions, bank, houses_player, houses_property)
            elif 'pay-rent-button.n_clicks' in triggers and pay_rent_n_clicks:
                msg = pay_rent(game, definitions, rent_player, rent_property, rent_dice)
            else:
                # this is the first time when all n_clicks are 0
                return game_state.to_cache(cache, data)

            if not msg:
                raise PreventUpdate

            game_state.add_state(game, msg, definitions)

        return game_state.to_cache(cache, data)
