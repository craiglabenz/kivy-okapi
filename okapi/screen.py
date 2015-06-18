from __future__ import print_function, absolute_import

# Kivy
from kivy.uix.boxlayout import BoxLayout


class Screen(object):

    def __init__(self, layout_cls=None, **kwargs):
        self.layout_cls = layout_cls or BoxLayout
        self.layout_kwargs = kwargs.get('layout_kwargs', {
            'orientation': 'vertical'
        })

    @property
    def container(self):
        if not hasattr(self, '_container'):
            self._container = self.get_container()
        return self._container

    def get_container(self):
        return self.layout_cls(**self.layout_kwargs)

    def add_widget(self, widget):
        self.container.add_widget(widget)

    def remove_widget(self, widget):
        self.container.remove_widget(widget)

    def render(self, widgets=None):
        self.container.clear_widgets()

        for widget in widgets or []:
            self.add_widget(widget)

        return self.container

    def get_clock_tuple(self):
        total_clock_tuple = ()
        for child in self.container.children or []:
            if hasattr(child, 'get_clock_tuple'):
                clock_tuple = child.get_clock_tuple()
                if not clock_tuple:
                    continue

                total_clock_tuple += clock_tuple

        return total_clock_tuple
