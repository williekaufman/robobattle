class Action():
    def __init__(self, condition, action, cost):
        self.condition = condition
        self.action = action
        self.cost = cost

    def do(self, robot, location, state):
        if self.cost > robot.energy:
            return False
        if self.condition(robot, location, state):
            self.action(location, state)