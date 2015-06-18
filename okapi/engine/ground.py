from __future__ import print_function, absolute_import, unicode_literals
import copy

# Local
from .base import PureOkapiMixin


class BaseGround(PureOkapiMixin, object):
    """
    Class that knows about graph-like things. Like all `engine` classes,
    it has no knowledge of Kivy.
    """
    cost_to_traverse = 1
    is_passable = True

    initial_actor_cls = None

    def __init__(self, coords, level, *args, **kwargs):

        self.x = coords[0]
        self.y = coords[1]
        self.level = level
        self.on_add_actor = kwargs.get('on_add_actor', None)

        # Setup the initial the actor
        self._actor = None
        self.actor = kwargs.get('actor', self.get_initial_actor())

    def __repr__(self):
        return '{} at ({}, {})'.format(type(self).__name__, self.x, self.y)

    @property
    def str(self):
        """Convenience prop since __repr__ gets called constantly
        to represent ground objects as literals in dictionaries
        """
        return self.__repr__()

    def get_cost_to_traverse(self, actor=None):
        return self.cost_to_traverse

    def get_initial_actor(self):
        if self.initial_actor_cls:
            return self.initial_actor_cls()

    def get_walkable_neighbors(self, actor):
        for _ground, x, y in self.neighbors:
            if _ground:
                if actor and not _ground.can_accommodate(actor, x, y, is_pathfinding=True):
                    continue
                yield _ground

    def get_frontier(self):
        for ground in self.level.get_frontier(starting_ground=self, actor=self.actor):
            yield ground

    def can_accommodate(self, actor, delta_x, delta_y, is_pathfinding=False):
        # Can accommodate if currently empty
        return self.is_passable and self.is_empty

    @property
    def is_empty(self):
        return not bool(self.actor)

    @property
    def actor(self):
        return self._actor

    @actor.setter
    def actor(self, value):
        # Quick out if re-setting the standing value
        if value == self._actor:
            return

        self._actor = value
        if self._actor:
            if self._actor.ground is None:
                if self.on_add_actor:
                    self.on_add_actor(self._actor, self)
            self._actor.ground = self

        self.fire_event('updated_actor')

    def get_directions(self):
        return copy.copy([
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1),
        ])

    @property
    def neighbors(self):
        for neighbor, delta_x, delta_y in self.level.neighbors[str(self)]:
            yield neighbor, delta_x, delta_y
