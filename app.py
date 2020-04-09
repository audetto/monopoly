import dash
import dash_bootstrap_components as dbc

from callbacks import register_callbacks
from layout import create_layout
from update import update_callbacks


def main():
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    human_players = ['Amelie', 'Sofia', 'Jackie', 'Andrea']
    bank = 'Bank'

    game = {player: {'money': 1500, 'properties': []} for player in human_players}
    game[bank] = {'money': 10000, 'properties': ['a', 'b', 'c', 'd', 'e', 'f']}

    app.title = 'Monopoly'
    app.layout = create_layout(human_players, bank, game)
    register_callbacks(app, human_players, bank)
    update_callbacks(app)

    app.run_server(host='192.168.0.30')


if __name__ == "__main__":
    main()
