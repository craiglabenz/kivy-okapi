from __future__ import print_function, absolute_import

# Kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class WelcomeScreen(BoxLayout):

    def __init__(self, *args, **kwargs):
        self.start_game_handler = kwargs.pop('start_game_handler', None)
        super(WelcomeScreen, self).__init__(*args, **kwargs)

        self.starter = Button(
            text="Rodent's Revenge (click to start)",
            color=(0, 0.5, 1, 1),
            font_size="40dp"
        )
        self.add_widget(self.starter)

    def on_press_any(self, keycode, text):
        if self.start_game_handler:
            self.start_game_handler()
