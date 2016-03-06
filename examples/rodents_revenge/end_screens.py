# Kivy
from kivy.uix.button import Button
from kivy.uix.label import Label

# Okapi
from okapi.screen import Screen


class LoseScreen(Screen):

    def __init__(self, layout_class=None, **kwargs):
        self.game = kwargs.pop('game')
        self.restart_handler = kwargs.pop('restart_handler')
        super(LoseScreen, self).__init__(layout_class, **kwargs)

    def render(self):
        self.add_widget(Label(text="Game Over!", font_size="40dp"))
        self.add_widget(Label(text="Final Score: {}".format(self.game.get_score()), font_size="40dp"))
        self.restarter = Button(
            text="Restart",
            color=(0.3, 0.5, 1, 1),
            font_size="40dp"
        )
        self.restarter.bind(on_press=self.restart_handler)
        self.add_widget(self.restarter)
        return self


class VictoryScreen(Screen):

    def __init__(self, layout_class=None, **kwargs):
        self.game = kwargs.pop('game')
        self.restart_handler = kwargs.pop('restart_handler')
        super(VictoryScreen, self).__init__(layout_class, **kwargs)

    def render(self):
        self.add_widget(Label(text="You Win!", font_size="40dp"))
        self.add_widget(Label(text="Final Score: {}".format(self.game.get_score()), font_size="40dp"))
        self.add_widget(Label(text="asdf", font_size="40dp", color=(1, 0, 0, 1),))
        return self
