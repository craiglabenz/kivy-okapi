from __future__ import print_function, absolute_import, unicode_literals

# Kivy
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

from .sprite import Sprite


class BaseActor(object):

    SPRITE_SOURCE = None

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

        # If the actor was somewhere else before, inform that
        # landlord we won't be renewing the lease
        if self._ground:
            self._ground.actor = None

        if not self.id:
            self.id = "{}-{}".format(value.x, value.y)

        self._ground = value

    def render(self):
        container = RelativeLayout()
        container.add_widget(Sprite(source=self.get_sprite_source()))
        container.add_widget(Label(text=str(self.id)))
        return container

    def get_sprite_source(self):
        assert self.SPRITE_SOURCE is not None, 'Failed to set SPRITE_SOURCE on {}'.format(type(self).__name__)
        return self.SPRITE_SOURCE
