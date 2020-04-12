import json
import uuid
from typing import List, Dict, Tuple, Optional

from flask_caching import Cache

from properties import Properties
from value import get_player_total_value


class Game:

    def __init__(self):
        self.state: Dict = {}

    def initialise(self, definitions: Properties, human_players: List[str], bank: str):
        self.state = {'pointer': -1, 'stack': []}

        initial_player_money = 1500
        game = {player: {'money': initial_player_money, 'properties': {}} for player in human_players}
        total_money = 30 * (500 + 100 + 50 + 20 + 10 + 5 + 1)
        bank_money = total_money - len(human_players) * initial_player_money
        game[bank] = {'money': bank_money,
                      'properties': {
                          prop: {'mortgage': False, 'houses': 0} for prop in definitions.data
                      }
                      }
        self.add_state(game, 'Start', definitions)

    def get_current_game(self) -> Dict:
        pointer = self.state['pointer']
        current = self.state['stack'][pointer]
        return current[0]

    def add_state(self, game: Dict, msg: str, definitions: Properties):
        pointer = self.state['pointer']
        del self.state['stack'][pointer + 1:]
        for player, data in game.items():
            data['total'] = get_player_total_value(data, definitions)
        self.state['stack'].append((game, msg))
        self.state['pointer'] += 1

    def move(self, steps: int):
        pointer = self.state['pointer']
        upper_bound = len(self.state['stack']) - 1
        lower_bound = 0
        self.state['pointer'] = max(lower_bound, min(pointer + steps, upper_bound))

    def get_progress(self) -> Tuple[float, str]:
        pointer = self.state['pointer']
        upper_bound = len(self.state['stack']) - 1
        progress = (pointer + 1) / (upper_bound + 1)
        return progress, f'{pointer + 1} / {upper_bound + 1}'

    def get_history(self, width: int) -> Tuple[List[Tuple[int, str]], int]:
        pointer = self.state['pointer']
        lower = pointer - width
        upper = pointer + width
        history = [(i, msg) for i, (_, msg) in enumerate(self.state['stack']) if lower <= i <= upper]
        return history, pointer

    def get_player_value_history(self, player: str) -> List[int]:
        result = [data[player]['total'] for data, _ in self.state['stack']]
        return result

    @staticmethod
    def from_cache(cache: Optional[Cache], data) -> 'Game':
        if cache:
            session_id = data[0]
            state = cache.get(session_id)
        else:
            state = json.loads(data)

        game = Game()
        game.state = state
        return game

    def to_cache(self, cache: Optional[Cache], data):
        if cache:
            if not data:
                data = [str(uuid.uuid4()), 0]

            session_id = data[0]
            cache.set(session_id, self.state)
            return [session_id, data[1] + 1]
        else:
            return json.dumps(self.state)
