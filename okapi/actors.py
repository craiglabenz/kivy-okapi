from __future__ import print_function, absolute_import, unicode_literals

# Local
from .base import OkapiKivyMixin, SpriteRenderMixin


class ActorWidget(SpriteRenderMixin, OkapiKivyMixin, object):
    """
    Class that knows how to render an actor.
    """
    sprite_source = None
