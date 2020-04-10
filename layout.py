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
    human_players_selects = [{'label': player} for player in human_players]

    pay_receive_tab = dbc.Card(dbc.CardBody(dbc.Form([
        dbc.FormGroup([
            dbc.Label('Pay', html_for='pay-player'),
            dbc.Col(dbc.Select(id='pay-player', options=player_selects))
        ], row=True),
        dbc.FormGroup([
            dbc.Label('Receive', html_for='receive-player'),
            dbc.Col(dbc.Select(id='receive-player', options=player_selects))
        ], row=True),
        dbc.FormGroup([
            dbc.Label('Amount', html_for='amount-pay'),
            dbc.Col(dbc.Input(id='pay-amount', type='numeric'))
        ], row=True),
        dbc.Button('Pay', id='pay-button', color="danger", className="mr-1")
    ])))

    property_dealing_tab = dbc.Card(dbc.CardBody(dbc.Form([
        dbc.FormGroup([
            dbc.Label('Seller', html_for='trade-seller'),
            dbc.Col(dbc.Select(id='trade-seller', options=actual_players_selects))
        ], row=True),
        dbc.FormGroup([
            dbc.Label('Buyer', html_for='trade-buyer'),
            dbc.Col(dbc.Select(id='trade-buyer', options=actual_players_selects))
        ], row=True),
        dbc.FormGroup([
            dbc.Label('Property', html_for='trade-property'),
            dbc.Col(dbc.Select(id='trade-property', options=EMPTY_SELECT))
        ], row=True),
        dbc.FormGroup([
            dbc.Label('Price', html_for='trade-price'),
            dbc.Col(dbc.Input(id='trade-price', type='numeric'))
        ], row=True),
        dbc.Button('Trade', id='trade-button', color="success", className="mr-1"),
    ])))

    extra_tab = dbc.Card(dbc.CardBody(dbc.Form([
        dbc.FormGroup([
            dbc.Label('Player', html_for='extra-player'),
            dbc.Col(dbc.Select(id='extra-player', options=human_players_selects))
        ], row=True),
        dbc.Button('Go', id='go-button', color="success", className="mr-1"),
        dbc.Button('Income Tax', id='income-tax-button', color="dark", className="mr-1"),
        dbc.Button('Super tax', id='super-tax-button', color="secondary", className="mr-1"),
        dbc.Button('Out of Jail', id='out-of-jail-button', color="danger", className="mr-1"),
    ])))

    mortgage_tab = dbc.Card(dbc.CardBody(dbc.Form([
        dbc.FormGroup([
            dbc.Label('Player', html_for='mortgage-player'),
            dbc.Col(dbc.Select(id='mortgage-player', options=human_players_selects))
        ], row=True),
        dbc.FormGroup([
            dbc.Label('Property', html_for='mortgage-property'),
            dbc.Col(dbc.Select(id='mortgage-property', options=EMPTY_SELECT))
        ], row=True),
        dbc.Button('Mortgage', id='mortgage-button', color="danger", className="mr-1"),
        dbc.Button('Unmortgage', id='unmortgage-button', color="success", className="mr-1"),
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
        dbc.Row(dbc.Col(
            dbc.Tabs([
                dbc.Tab(pay_receive_tab, label="Money"),
                dbc.Tab(property_dealing_tab, label="Trading"),
                dbc.Tab(extra_tab, label="Extra"),
                dbc.Tab(mortgage_tab, label="Mortgage"),    
            ])
        )),
        html.Br(),
        dbc.Row(player_columns),
    ])

    store = dcc.Store(id='game-state', data=json.dumps(game))

    layout = html.Div([store, game_layout])

    return layout
