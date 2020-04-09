import json
from typing import List, Dict

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


EMPTY_SELECT = [{'label': 'empty'}]


def create_layout(human_players: List[str], bank: str, game: Dict):
    player_columns = []
    player_selects = []
    for player in human_players + [bank]:
        color = 'danger' if player == bank else 'primary'
        label = dbc.Alert(player, color=color)
        money = dbc.Input(id=f'{player}-money', type='numeric', disabled=True)
        properties = dbc.Table(id=f'{player}-properties')
        col = dbc.Col([label, money, html.Br(), properties])
        player_columns.append(col)
        player_selects.append({'label': player})

    player_selects.append({'label': 'ALL'})
    actual_players_selects = [{'label': player} for player in human_players + [bank]]

    pay_receive_tab = dbc.Card(dbc.CardBody(dbc.Form([
        dbc.FormGroup([
            dbc.Label('Pay', html_for='pay-player'),
            dbc.Select(id='pay-player', options=player_selects)
        ]),
        dbc.FormGroup([
            dbc.Label('Receive', html_for='receive-player'),
            dbc.Select(id='receive-player', options=player_selects)
        ]),
        dbc.FormGroup([
            dbc.Label('Amount', html_for='amount-pay'),
            dbc.Input(id='pay-amount', type='numeric')
        ]),
        dbc.Button('Pay', id='pay-button')
    ])))

    property_dealing_tab = dbc.Card(dbc.CardBody(dbc.Form([
        dbc.FormGroup([
            dbc.Label('Seller', html_for='trade-seller'),
            dbc.Select(id='trade-seller', options=actual_players_selects)
        ]),
        dbc.FormGroup([
            dbc.Label('Buyer', html_for='trade-buyer'),
            dbc.Select(id='trade-buyer', options=actual_players_selects)
        ]),
        dbc.FormGroup([
            dbc.Label('Property', html_for='trade-property'),
            dbc.Select(id='trade-property', options=EMPTY_SELECT)
        ]),
        dbc.FormGroup([
            dbc.Label('Price', html_for='trade-price'),
            dbc.Input(id='trade-price', type='numeric')
        ]),
        dbc.Button('Trade', id='trade-button'),
    ])))

    navbar = dbc.NavbarSimple(
        brand="Monopoly",
        brand_href="#",
        color="primary",
        dark=True,
    )

    game_layout = dbc.Container([
        dbc.Row(navbar),
        html.Br(),
        dbc.Row(player_columns),
        html.Br(),
        dbc.Row(dbc.Col(
            dbc.Tabs([
                dbc.Tab(pay_receive_tab, label="Money"),
                dbc.Tab(property_dealing_tab, label="Trading"),
            ])
        ))
    ])

    store = dcc.Store(id='game-state', data=json.dumps(game))

    layout = html.Div([store, game_layout])

    return layout
