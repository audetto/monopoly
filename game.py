import json
from typing import List, Dict, Tuple


class Game:

    def __init__(self):
        self.state: Dict = {}

    def initialise(self, definitions: Dict, human_players: List[str], bank: str):
        initial_player_money = 1500
        game = {player: {'money': initial_player_money, 'properties': {}} for player in human_players}
        total_money = 30 * (500 + 100 + 50 + 20 + 10 + 5 + 1)
        bank_money = total_money - len(human_players) * initial_player_money
        game[bank] = {'money': bank_money,
                      'properties': {
                          prop: {'mortgage': False, 'houses': 0} for prop in definitions
                      }
                      }

        self.state = {'pointer': 0, 'stack': [(game, 'Start')]}

    def get_current_game(self) -> Dict:
        pointer = self.state['pointer']
        current = self.state['stack'][pointer]
        return current[0]

    def add_state(self, game: Dict, msg: str):
        pointer = self.state['pointer']
        del self.state['stack'][pointer + 1:]
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

    def get_history(self) -> Tuple[List[str], int]:
        pointer = self.state['pointer']
        history = [msg for game, msg in self.state['stack']]
        return history, pointer

    @staticmethod
    def from_json(data: str) -> 'Game':
        game = Game()
        game.state = json.loads(data)
        return game

    def to_json(self) -> str:
        return json.dumps(self.state)
