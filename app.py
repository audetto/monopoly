import dash
import dash_bootstrap_components as dbc

from callbacks import register_callbacks
from game import Game
from layout import create_layout
from properties import Properties
from update import update_callbacks


def create_app():
    the_app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    human_players = ['Amelie', 'Sofia', 'Jackie', 'Andrea']
    bank = 'Bank'
    property_definitions = Properties()

    game_state = Game()
    game_state.initialise(property_definitions, human_players, bank)

    the_app.title = 'Monopoly'
    the_app.layout = create_layout(human_players, bank, game_state)
    register_callbacks(the_app, property_definitions, human_players, bank)
    update_callbacks(the_app, property_definitions, human_players, bank)
    return the_app


app = create_app()
server = app.server


if __name__ == "__main__":
    app.run_server(host='0.0.0.0')
