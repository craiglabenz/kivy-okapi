from __future__ import print_function, absolute_import, unicode_literals
import heapq

# Local
from .base import PureOkapiMixin


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class AStarPathingMixin(object):

    def get_best_move_toward(self, target_ground):
        """
        Generally, you will call this function to smartly path an actor.
        Returns an x,y tuple of the desired move.
        """
        options_by_parent, cost_to_reach = self.a_star_search(start=self.ground, goal=target_ground)
        ground = target_ground

        # Can't reach it?
        if ground not in options_by_parent:
            return None

        while options_by_parent[ground] is not self.ground:
            ground = options_by_parent[ground]

        return ground.x - self.ground.x, ground.y - self.ground.y

    def a_star_search(self, start, goal):

        def heuristic(a, b):
            x1 = a.x
            y1 = a.y
            x2 = b.x
            y2 = b.y
            return abs(x1 - x2) + abs(y1 - y2)

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {start: None}
        cost_to_reach = {start: 0}

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for neighbor in current.get_walkable_neighbors(actor=self):
                new_cost = cost_to_reach[current] + neighbor.get_cost_to_traverse(self)
                if neighbor not in cost_to_reach or new_cost < cost_to_reach[neighbor]:
                    cost_to_reach[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor)
                    frontier.put(neighbor, priority)
                    came_from[neighbor] = current

        return came_from, cost_to_reach


class BaseActor(AStarPathingMixin, PureOkapiMixin, object):
    """
    Class that knows about actor things, like how it moves, what actions
    it can take inside the game world, etc.
    Like all `engine` classes, it has no knowledge of Kivy.
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self._ground = None

    def __repr__(self):
        if self.ground:
            return '{} {}-{}'.format(type(self).__name__, self.ground.x, self.ground.y)
        else:
            return super(BaseActor, self).__repr__()

    @property
    def ground(self):
        return self._ground

    @ground.setter
    def ground(self, value):
        if self._ground == value:
            return

        # If the actor was somewhere else before, inform that
        # landlord we won't be renewing the lease
        if self._ground and getattr(self._ground, 'actor') == self:
            self._ground.actor = None

        if not self.id:
            self.id = "{}-{}".format(value.x, value.y)

        self._ground = value

        self.fire_event('moved')

    def move(self):
        pass
