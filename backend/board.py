from enum import Enum
from square import Square, Contents
from unit import UnitType, EmptyUnit
from enemy import Enemy, get_enemy
from player import Player
from helpers import unit_of_json
from boards import board_configs, make_board
import random


class Board():
    def __init__(self, initialize_board=True, name=None):
        self.board = {}
        self.non_board_enemies = []
        if not initialize_board:
            return
        self.board = {square: Contents(EmptyUnit()) for square in Square}
        self.board.setunit(Square('A1'), Player())

    def get(self, square):
        return self.board[square]

    def set(self, square, contents):
        self.board[square] = contents

    def set_unit(self, square, unit):
        self.board[square].unit = unit

    def set_terrain(self, square, terrain):
        self.board[square].terrain = terrain

    def cleanup_dead_enemies(self):
        for square, contents in self.board.items():
            if contents.unit.type == UnitType.ENEMY and contents.unit.current_health <= 0:
                self.set_unit(square, EmptyUnit())

    def player_location(self):
        for square, contents in self.board.items():
            if contents.unit.type == UnitType.PLAYER:
                return square

    def player(self):
        return self.board[self.player_location()].unit
    
    def location_of(self, unit):
        for square, contents in self.board.items():
            if contents.unit == unit:
                return square

    def enemies(self):
        return [contents.unit for contents in self.board.values() if contents.unit.type == UnitType.ENEMY]

    def orbs(self):
        return [contents.unit for contents in self.board.values() if contents.unit.type == UnitType.ORB]

    def move(self, square, target):
        if not target or not self.get(target).empty():
            return False
        if self.get(target).unit.type == UnitType.ORB:
            self.get(target).unit.pickup(self.get(square).unit)
        self.set_unit(target, self.get(square).unit)
        self.set_unit(square, EmptyUnit())

    def move_direction(self, square, direction):
        return self.move(square, square.direction(direction))

    def to_json(self):
        return {k.value: v.to_json() for k, v in self.board.items()}

    def of_json(j):
        b = Board(False)
        b.board = {Square(k): Contents(
            unit_of_json(v['unit']), Terrain(v['terrain'])) for k, v in j['board'].items()}
        return b

    def to_frontend(self, state):
        return {
            'board': self.to_json(),
            'player': self.player().to_json(),
            'enemies': [enemy.to_json() for enemy in self.enemies()],
        }
