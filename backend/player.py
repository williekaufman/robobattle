from unit import UnitType
from robot import Robot

class Player():
    def __init__(self, robot=Robot()):
        self.type = UnitType.PLAYER
        self.robot = robot 

    def empty(self):
        return False

    def to_json(self):
        return {
            'type': self.type.value,
            'robot': self.robot.to_json(),
        }

    def of_json(j):
        return Player(robot=Robot.of_json(j['robot']))

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)

    def heal(self, amount):
        self.current_health = min(
            self.max_health, self.current_health + amount)