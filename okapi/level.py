from __future__ import print_function, absolute_import, unicode_literals

# Kivy
from kivy.uix.gridlayout import GridLayout

# Local
from .base import OkapiKivyMixin
from .ground import GroundWidget


class LevelScreen(OkapiKivyMixin, GridLayout):

    PADDING = 0
    SPACING = 0

    def __init__(self, okapi_object, *args, **kwargs):

        kwargs.setdefault('cols', okapi_object.cols)
        kwargs.setdefault('rows', okapi_object.rows)
        kwargs.setdefault('padding', self.PADDING)
        kwargs.setdefault('spacing', self.SPACING)

        super(LevelScreen, self).__init__(okapi_object, *args, **kwargs)

        self.render()

    def render(self):
        for ground in self.okapi_object.ground_iter():
            ground_widget = GroundWidget(okapi_object=ground)
            self.add_widget(ground_widget.render())

        return self

    def get_clock_tuple(self):
        return self.okapi_object.game.get_clock_tuple()
