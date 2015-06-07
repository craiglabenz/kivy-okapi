from __future__ import print_function, absolute_import, unicode_literals

# Kivy
# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

# Local
from .sprite import Sprite


class BaseGround(object):
    """
    Class that knows how to render a piece of ground and optionally
    an actor atop that ground.
    """

    sprite_path = None
    cost_to_traverse = 1
    is_passable = True

    initial_actor_cls = None

    def __init__(self, coords, level, *args, **kwargs):

        self.x = coords[0]
        self.y = coords[1]
        self.level = level
        self.on_add_actor = kwargs.get('on_add_actor', None)

        # Must provide a valid source
        assert 'source' in kwargs or self.sprite_path, 'Failed to initialize {} with a `source`'.format(type(self).__name__)
        source = kwargs.pop('source', self.sprite_path)

        # The entire Ground class is really just a wrapper around
        # this container, which stores all required Sprite widgets
        self.container = self.get_container()
        self.ground_sprite = Sprite(source=source)

        # Setup the initial the actor
        self._actor = None
        self.actor = kwargs.get('actor', self.get_initial_actor())

    def __repr__(self):
        return '{} at ({}, {})'.format(type(self).__name__, self.x, self.y)

    def get_container(self):
        return RelativeLayout()

    def get_cost_to_traverse(self, actor=None):
        return self.cost_to_traverse

    def get_initial_actor(self):
        if self.initial_actor_cls:
            return self.initial_actor_cls()

    def can_accommodate(self, actor, delta_x, delta_y):
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
        self._actor = value

        if self._actor:

            if self._actor.ground is None:
                if self.on_add_actor:
                    self.on_add_actor(self._actor, self)
            self._actor.ground = self

        self.render()

    def render(self):
        self.container.clear_widgets()

        self.container.add_widget(self.ground_sprite)
        if self.actor:
            self.container.add_widget(self.actor.render())

        return self.container
