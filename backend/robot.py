from square import Direction
from action import Action
from sensor import Sensor
from square import Direction

class Robot():
    def __init__(self, current_health=10, max_health=10, energy=10, sensors={direction: None for direction in Direction}, actions=[]):
        self.current_health = current_health
        self.max_health = max_health
        self.energy = energy 
        self.sensors = sensors
        self.actions = actions

    def to_json(self):
        return {
            'current_health': self.current_health,
            'max_health': self.max_health,
            'energy': self.energy,
            'sensors': [s.to_json() for s in self.sensors],
            'actions': [a.to_json() for a in self.actions],
        }
    
    def of_json(j):
        j['sensors'] = [Sensor.of_json(s) for s in j['sensors']]
        j['actions'] = [Action.of_json(a) for a in j['actions']]
        return Robot(**j)

    def set_sensor(self, direction, sensor):
        self.sensors[direction] = sensor

    def add_action(self, action):
        self.actions.append(action)

    def location(self, state):
        return state.board.location_of(self)

    def check(self, state):
        for action in self.actions:
            action.do(self, self.location(state), state)