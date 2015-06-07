from __future__ import print_function, absolute_import, unicode_literals

from .sprite import Sprite


class BaseActor(object):

    SPRITE_SOURCE = None

    def __init__(self, *args, **kwargs):
        self._ground = None

    @property
    def ground(self):
        return self._ground

    @ground.setter
    def ground(self, value):

        # If the actor was somewhere else before, inform that
        # landlord we won't be renewing the lease
        if self._ground:
            self._ground.actor = None

        self._ground = value

    def render(self):
        return Sprite(source=self.get_sprite_source())

    def get_sprite_source(self):
        assert self.SPRITE_SOURCE is not None, 'Failed to set SPRITE_SOURCE on {}'.format(type(self).__name__)
        return self.SPRITE_SOURCE
