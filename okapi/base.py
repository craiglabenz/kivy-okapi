from __future__ import print_function, absolute_import, unicode_literals
import os

# Kivy
from kivy.uix.relativelayout import RelativeLayout

# Local
from .sprite import Sprite


class SpriteRenderMixin(object):
    sprite_path = None

    @property
    def sprite(self):
        if not hasattr(self, '_sprite'):
            self._sprite = Sprite(source=self.get_sprite_source())
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        self._sprite = value

    def get_sprite_source(self):
        return os.path.abspath(os.path.join(self.okapi_object.project_root, self.okapi_object.sprite_path))

    def render(self):
        self.container.clear_widgets()
        self.container.add_widget(self.sprite)
        return self.container

    @property
    def container(self):
        if not hasattr(self, '_container'):
            self._container = self.get_container()
        return self._container

    def get_container(self):
        return RelativeLayout()


class OkapiKivyMixin(object):
    """
    A class sits between Kivy and Okapi concepts.
    This mixin is the core of that conceptual class.
    """

    # Should have keys of event names and values of strings
    # matching the names of functions on ``self``.
    #   e.g.
    #       events: {
    #           'changed_thing': 'render'
    #       }
    events = {}

    def __init__(self, okapi_object, *args, **kwargs):
        self.okapi_object = okapi_object
        if self.okapi_object:
            self.initialize_okapi_object()
        super(OkapiKivyMixin, self).__init__(*args, **kwargs)

    def initialize_okapi_object(self):
        self.okapi_object.event_handler = self.event_handler
        self.callbacks_map = {}
        self.setup_listeners()

    def setup_listeners(self):
        for key, value in self.events.items():
            self.listen_to(key, getattr(self, value))

    def listen_to(self, event_name, cb):
        """
        Allow OkapiKivy components to listen to their raw
        Okapi objects without the objects knowing what's up.
        """
        self.callbacks_map.setdefault(event_name, [])
        self.callbacks_map[event_name].append(cb)

    def event_handler(self, event_name):
        for cb in self.callbacks_map.get(event_name, []):
            cb()
