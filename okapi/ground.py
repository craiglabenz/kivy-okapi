from __future__ import print_function, absolute_import, unicode_literals

# Local
from .actors import ActorWidget
from .base import OkapiKivyMixin, SpriteRenderMixin


class GroundWidget(SpriteRenderMixin, OkapiKivyMixin, object):
    """
    Class that knows how to render a piece of ground.
    """
    events = {
        'updated_actor': 'render'
    }

    def render(self):
        """
        Like a normal ``SpriteRenderMixin`` render, except
        also adds ``self.actor`` if the attr is set.
        """
        container = super(GroundWidget, self).render()

        if self.okapi_object and self.okapi_object.actor:
            actor_widget = ActorWidget(okapi_object=self.okapi_object.actor)
            container.add_widget(actor_widget.render())

        return container
