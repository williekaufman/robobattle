from unit import UnitType
from enum import Enum

class Orb():
    def __init__(self, name, description, pickup=lambda self, unit, state: None):
        self.type = UnitType.ORB
        self.name = name
        self.description = description
        self.pickup = pickup

    def empty(self):
        return True

    def copy(self):
        return Orb(self.name, self.description, self.pickup)

    def to_json(self):
        return {
            'type': self.type.value,
            'name': self.name,
        }

    def of_json(json):
        return orbs(json['name'])

    def describe(self):
        return {
            'name': self.name,
            'description': self.description,
        }
    
    def take_damage(self, damage):
        pass

    def lose_life(self, damage):
        pass

    def heal(self, amount):
        pass

orbs = {
    'Orb': Orb('Orb', 'A basic orb. Does nothing.', pickup=lambda self, unit, state: None),
}

def get_orb(name):
    try:
        return orbs[name].copy()
    except:
        return None

def all_orbs():
    return [orb.copy() for orb in orbs.values()]