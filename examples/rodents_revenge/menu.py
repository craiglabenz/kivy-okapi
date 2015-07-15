import os

# Kivy
from kivy.graphics import Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# Engine
from okapi.sprite import Sprite


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class Menu(object):

    def __init__(self, game):
        self.game = game

    @property
    def container(self):
        if not hasattr(self, '_container'):
            self._container = self.get_container()
        return self._container

    def get_container(self):
        layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1.0, 0.1,)
        )
        layout.canvas.add(Color(0, 0, 0))
        return layout

    def render(self):
        self.container.clear_widgets()
        self.draw_lives()
        self.draw_level_marker()
        self.draw_score()
        return self.container

    def draw_level_marker(self):
        self.container.add_widget(Label(text="Level {}".format(self.game.current_level_index + 1)))

    def draw_score(self):
        self.score_label = Label(text=str(self.game.player_score), size_hint=(0.4, 1.0))
        self.container.add_widget(self.score_label)

    def draw_lives(self):
        lives_container = BoxLayout(size_hint=(0.4, 1.0))
        source = os.path.abspath(os.path.join(PROJECT_PATH, 'assets/images/rat-50.png'))
        for _ in range(self.game.player_lives):
            lives_container.add_widget(Sprite(source=source))

        self.container.add_widget(lives_container)
