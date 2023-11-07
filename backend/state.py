from redis_utils import rget, rget_json, rset_json, rset, recurse_to_json
from board import Board, Square
from enum import Enum

class Result(Enum):
    WIN = 'win'
    LOSE = 'lose'

class GameInfo():
    def __init__(self, id, turn):
        self.id = id
        self.turn = turn

    def of_game_id(game_id):
        try:
            turn = int(rget('turn', game_id))
        except:
            raise Exception('Invalid game id')
        return GameInfo(game_id, turn)
    
    def seed(self):
        return self.id + str(self.turn)
    
    def to_json(self):
        return {'id': self.id, 'turn': self.turn}

class State():
    def __init__(self, game_info, board):
        self.game_info = game_info
        self.board = board

    def of_game_id(game_id):
        game_info = GameInfo.of_game_id(game_id)
        board = Board.of_json(rget_json('board', game_id))
        return State(game_info, board)

    def roll_turn(self):
        pass

    def check_game_over(self):
        board = self.board
        if board.player().current_health <= 0:
            return Result.LOSE
        if [enemy for enemy in board.enemies() if enemy.current_health > 0]:
            return None
        return Result.WIN


    def to_frontend(self):
        result = self.check_game_over()
        result = {} if result is None else {'result': result.value}
        return {'game_info': self.game_info.to_json(), **self.board.to_frontend(self)}

    def write(self):
        rset('turn', self.game_info.turn, self.game_info.id)
        rset_json('board', recurse_to_json(self.board.to_json()), self.game_info.id)