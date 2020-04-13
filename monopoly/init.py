from typing import Optional

from flask_caching import Cache

from monopoly.callbacks import register_callbacks
from monopoly.layout import create_layout
from monopoly.properties import Properties
from monopoly.update import update_callbacks


def populate_game(app, cache: Optional[Cache]):
    human_players = ['Amelie', 'Sofia', 'Andrea']
    bank = 'Bank'
    property_definitions = Properties()

    app.title = 'Monopoly'
    app.layout = lambda: create_layout(cache, property_definitions, human_players, bank)
    register_callbacks(cache, app, property_definitions, human_players, bank)
    update_callbacks(cache, app, property_definitions, human_players, bank)
