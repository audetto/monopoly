from typing import List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from game import Game

EMPTY_SELECT = [{'label': ''}]


def create_layout(human_players: List[str], bank: str, game_state: Game):
    player_columns = []
    player_selects = []
    for player in human_players + [bank]:
        color = 'danger' if player == bank else 'primary'
        label = dbc.Alert(player, color=color)
        total = dbc.Input(id=f'{player}-total', disabled=True)
        money = dbc.Input(id=f'{player}-money', disabled=True)
        properties = dbc.Table(id=f'{player}-properties')
        col = dbc.Col([label, total, money, html.Br(), properties])
        player_columns.append(col)
        player_selects.append({'label': player})

    player_selects.append({'label': 'ALL'})
    actual_players_selects = [{'label': player} for player in human_players + [bank]]
    human_players_selects = [{'label': player} for player in human_players]

    pay_receive_tab = dbc.Card(dbc.CardBody(dbc.Form([
        dbc.FormGroup([
            dbc.Label('From', html_for='pay-player'),
            dbc.Col(dbc.Select(id='pay-player', options=player_selects))
        ], row=True),
        dbc.FormGroup([
            dbc.Label('To', html_for='receive-player'),
            dbc.Col(dbc.Select(id='receive-player', options=player_selects, value=bank))
        ], row=True),
        dbc.FormGroup([
            dbc.Label('Amount', html_for='amount-pay'),
            dbc.Col(dbc.Input(id='pay-amount', type='number'))
        ], row=True),
        dbc.Button('Pay', id='pay-button', color="danger", className="mr-1")
    ])))

    property_dealing_tab = dbc.Card(dbc.CardBody(dbc.Form([
        dbc.FormGroup([
            dbc.Label('Seller', html_for='trade-seller'),
            dbc.Col(dbc.Select(id='trade-seller', options=actual_players_selects, value=bank))
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
            dbc.Col(dbc.Input(id='trade-price', type='number'))
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
        dbc.Button('Super Tax', id='super-tax-button', color="secondary", className="mr-1"),
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

    buildings_tab = dbc.Card(dbc.CardBody(dbc.Form([
        dbc.FormGroup([
            dbc.Label('Player', html_for='houses-player'),
            dbc.Col(dbc.Select(id='houses-player', options=human_players_selects))
        ], row=True),
        dbc.FormGroup([
            dbc.Label('Property', html_for='houses-property'),
            dbc.Col(dbc.Select(id='houses-property', options=EMPTY_SELECT))
        ], row=True),
        dbc.Button('Buy house', id='buy-house-button', color="success", className="mr-1"),
        dbc.Button('Sell house', id='sell-house-button', color="danger", className="mr-1"),
    ])))

    charts_tab = dbc.Card(dbc.CardBody(
        dcc.Graph(id='history-charts')
    ))

    control_panel = [
        dbc.Row(dbc.Col(dbc.Alert('Monopoly @ Cratbree'))),
        dbc.Row(dbc.Col(dbc.Input(id='json-size', disabled=True))),
        html.Br(),
        dbc.Row(dbc.Col(dbc.ButtonGroup([
            dbc.Button('Backward', id='backward-button', color='danger', className="mr-1"),
            dbc.Button('Forward', id='forward-button', color='success', className="mr-1"),
        ], vertical=True))),
        html.Br(),
        dbc.Row(dbc.Col(dbc.Progress(id='game-progress'))),
        html.Br(),
        dbc.Row(dbc.Col(dbc.Table(id='history-table'))),
    ]

    game_layout = dbc.Container([
        html.Br(),
        dbc.Row([
            dbc.Col(control_panel, width=2),
            dbc.Col([
                dbc.Row(dbc.Col(dbc.Tabs([
                    dbc.Tab(charts_tab, label="Charts"),  # must be first due to a dash bug
                    dbc.Tab(pay_receive_tab, label="Money"),
                    dbc.Tab(property_dealing_tab, label="Trading"),
                    dbc.Tab(extra_tab, label="Extra"),
                    dbc.Tab(mortgage_tab, label="Mortgage"),
                    dbc.Tab(buildings_tab, label="Buildings"),
                ]))),
                html.Br(),
                dbc.Row(player_columns),
            ], width=10)
        ])
    ], fluid=True)

    store = dcc.Store(id='game-state', data=game_state.to_json())

    layout = html.Div([store, game_layout])

    return layout
