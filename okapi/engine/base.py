from __future__ import print_function, absolute_import, unicode_literals


class PureOkapiMixin(object):
    """
    Mixin that allows the Kivy layer to listen to the pure Okapi layer
    without the pure Okapi layer being any the wiser.
    """
    def fire_event(self, event_name, *args, **kwargs):
        if hasattr(self, 'event_handler'):
            self.event_handler(event_name, *args, **kwargs)
