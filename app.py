import os
from random import randint

import dash
import dash_bootstrap_components as dbc
import flask
from flask_caching import Cache

from monopoly.init import populate_game

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp/monopoly',
    'CACHE_THRESHOLD': 10,
}

cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)

populate_game(app, cache)

if __name__ == "__main__":
    app.server.run()
