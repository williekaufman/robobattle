from square import Square
from unit import UnitType, EmptyUnit
from enum import Enum
import random

class Enemy():
    def __init__(self, name, robot):
        self.type = UnitType.ENEMY
        self.name = name
        self.robot = robot

    def empty(self):
        return False

    def to_json(self):
        return {
            'type': self.type.value,
            'name': self.name,
            'robot': self.robot.to_json(),
        }
    
    def describe(self):
        return {
            'name': self.name,
            'robot': self.robot.describe(),
        }

    def of_json(j):
        enemy = get_enemy(j['name'])
        enemy.current_health = j['current_health']
        return enemy

    def location(self, state):
        return state.board.location_of(self)        

    def describe_turn(self, state):
        location = self.location(state)
        return {'location': location.value if location else None, **(self.moves[self.move_index].describe(state, location)).to_json()}

    def resolve_turn(self, state):
        move = self.moves[self.move_index]
        move.resolve(state, self.location(state))
        self.transition(self, state)

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)

    def lose_life(self, amount):
        self.take_damage(amount)

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)

    def copy(self):
        return Enemy(self.name, self.current_health, self.max_health, self.moves, self.transition, self.move_index, self.prevent_win)

def next_move(enemy, state):
    enemy.move_index = (enemy.move_index + 1) % len(enemy.moves)

def random_move(enemy, state):
    enemy.move_index = random.randint(0, len(enemy.moves) - 1)

def prevent_win_until_turn(n):
    return lambda state: f"Must live until turn {n}" if state.game_info.turn < n else False

damage_terrain = moves['damage_terrain']
transform = moves['transform']
move = moves['move']
random_direction = moves['random_direction']
cross_attack = moves['cross_attack']
move_then_cross_attack = moves['move_then_cross_attack']
damage_all = moves['damage_all']
pass_turn = moves['pass_turn']

def win_preventer(n):
    return Enemy(f'Win Preventer {n}', 1, 1, [pass_turn()], next_move, prevent_win=prevent_win_until_turn(n))

# You need to make a copy if you interact with this! So probably use get_enemy.
enemies = {
    'Orc': Enemy('Orc', 5, 5, [damage_terrain(Terrain.PLAINS, 2), transform(Terrain.FOREST, Terrain.PLAINS)], random_move),
    'Goblin': Enemy('Goblin', 3, 3, [move(Square('A1'))], random_move),
    'Skeleton': Enemy('Skeleton', 2, 2, [random_direction()], next_move),
    'Rook Man': Enemy('Rook Man', 7, 7, [cross_attack(), move_then_cross_attack()], next_move),
    'Trap Room': Enemy('Trap Room', 1, 1, [damage_all(1), pass_turn()], next_move, prevent_win=prevent_win_until_turn(6)),
    **{f'Win Preventer {i}': win_preventer(i) for i in range(1, 10)},
}

def get_enemy(name):
    try:
        return enemies[name].copy()
    except KeyError:
        raise Exception(f'No enemy named {name}')

def all_enemies():
    return [enemy.copy() for enemy in enemies.values()]