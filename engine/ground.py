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

    initial_actor = None

    def __init__(self, *args, **kwargs):

        # Must provide a valid source
        assert 'source' in kwargs or self.sprite_path, 'Failed to initialize {} with a `source`'.format(type(self).__name__)
        source = kwargs.pop('source', self.sprite_path)

        # Initialize the attr before calling `add_actor`
        self.actor = self.get_initial_actor()

        # Actors are, of course, optional
        self.add_actor(kwargs.get('actor', None))

        # The entire Ground class is really just a wrapper around
        # this container, which stores all required Sprite widgets
        self.container = self.get_container()
        self.ground_sprite = Sprite(source=source)

    def get_container(self):
        return RelativeLayout()

    def get_cost_to_traverse(self, actor=None):
        return self.cost_to_traverse

    def get_initial_actor(self):
        return self.initial_actor

    def add_actor(self, actor):
        if actor is None:
            return

        # Clear out a previous actor
        if self.actor:
            self.remove_widget(self.actor)

        # Save the new actor
        self.actor = actor

    def render(self):
        self.container.clear_widgets()

        self.container.add_widget(self.ground_sprite)
        if self.actor:
            self.container.add_widget(self.actor.render())

        return self.container
