import dash
import dash_bootstrap_components as dbc

from callbacks import register_callbacks
from game import Game
from layout import create_layout
from properties import get_properties
from update import update_callbacks


def main():
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    human_players = ['Amelie', 'Sofia', 'Jackie', 'Andrea']
    bank = 'Bank'
    property_definitions = get_properties()

    game_state = Game()
    game_state.initialise(property_definitions, human_players, bank)

    app.title = 'Monopoly'
    app.layout = create_layout(human_players, bank, game_state)
    register_callbacks(app, property_definitions, human_players, bank)
    update_callbacks(app, property_definitions, human_players, bank)

    app.run_server(host='0.0.0.0')


if __name__ == "__main__":
    main()
