import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache

from callbacks import register_callbacks
from layout import create_layout
from properties import Properties
from update import update_callbacks

CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp/monopoly',
    'CACHE_THRESHOLD': 10,
}


def create_app():
    the_app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    # cache = Cache()
    # cache.init_app(the_app.server, config=CACHE_CONFIG)
    cache = None

    human_players = ['Amelie', 'Sofia', 'Andrea']
    bank = 'Bank'
    property_definitions = Properties()

    the_app.title = 'Monopoly'
    the_app.layout = lambda: create_layout(cache, property_definitions, human_players, bank)
    register_callbacks(cache, the_app, property_definitions, human_players, bank)
    update_callbacks(cache, the_app, property_definitions, human_players, bank)
    return the_app


app = create_app()
server = app.server


if __name__ == "__main__":
    app.run_server(host='0.0.0.0')
