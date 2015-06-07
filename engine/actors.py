from __future__ import print_function, absolute_import

from .sprite import Sprite


class BaseActor(object):

    SPRITE_SOURCE = None

    def render(self):
        return Sprite(source=self.get_sprite_source())

    def get_sprite_source(self):
        assert self.SPRITE_SOURCE is not None, 'Failed to set SPRITE_SOURCE on {}'.format(type(self).__name__)
        return self.SPRITE_SOURCE
