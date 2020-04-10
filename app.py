import dash
import dash_bootstrap_components as dbc

from callbacks import register_callbacks
from layout import create_layout
from properties import get_properties
from update import update_callbacks


def main():
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    human_players = ['Amelie', 'Sofia', 'Jackie', 'Andrea']
    bank = 'Bank'
    property_definitions = get_properties()

    game = {player: {'money': 1500, 'properties': {}} for player in human_players}
    total_money = 30 * (500 + 100 + 50 + 20 + 10 + 5 + 1)
    bank_money = total_money - len(human_players) * 1500
    game[bank] = {'money': bank_money,
                  'properties': {prop: {'mortgage': False, 'houses': 0} for prop in property_definitions}}

    app.title = 'Monopoly'
    app.layout = create_layout(human_players, bank, game)
    register_callbacks(app, property_definitions, human_players, bank)
    update_callbacks(app, property_definitions, bank)

    app.run_server(host='0.0.0.0')


if __name__ == "__main__":
    main()
