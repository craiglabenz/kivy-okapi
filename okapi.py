# from __future__ import print_statement

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
# from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
# from kivy.clock import Clock
# from kivy.uix.button import Button
from kivy.uix.image import Image
# from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


class Sprite(Image):

    def __init__(self, **kwargs):
        kwargs['allow_stretch'] = True
        kwargs['keep_ratio'] = False
        super(Sprite, self).__init__(**kwargs)


class BasicGround(BoxLayout):
    sprite_path = 'assets/images/ground-50.png'

    def __init__(self, *args, **kwargs):
        super(BasicGround, self).__init__(*args, **kwargs)
        self.ground_sprite = Sprite(source=self.sprite_path, size=("30dp", "30dp"))

    def render(self):
        self.add_widget(self.ground_sprite)
        return self


class Game(GridLayout):

    # in pixels
    SQUARE_SIZE = 50

    # in... numbers. heh
    ROWS = 10
    COLS = 10
    PADDING = 0
    SPACING = 0

    def __init__(self, **kwargs):
        kwargs.setdefault('cols', self.COLS)
        kwargs.setdefault('rows', self.ROWS)
        kwargs.setdefault('padding', self.PADDING)
        kwargs.setdefault('spacing', self.SPACING)
        super(Game, self).__init__(**kwargs)

        self.objectify()
        self.render()

    def objectify(self):
        """
        Dan's code will replace me.
        For now I'm responsible for a 10x10 grid.
        """
        self.ground = []

        for x in range(self.ROWS):
            self.ground.append([])

            for y in range(self.COLS):
                self.ground[x].append(BasicGround)

    def render(self):
        # self.clear_old_ground()
        for row_index, row in enumerate(self.ground):
            for column_index, ground_widget_cls in enumerate(row):

                ground_widget = ground_widget_cls()
                ground_widget.render()

                # Trow it on de barbey
                self.add_widget(ground_widget)

    def clear_old_ground(self):
        if self.ground:
            for row in self.ground:
                for column in row:
                    self.remove_widget(column)


class OkapiRoot(BoxLayout):

    def __init__(self):
        super(OkapiRoot, self).__init__()

        self.welcome_screen = Factory.WelcomeScreen()
        self.welcome_screen.btn.bind(on_press=self.start_game)
        self.add_widget(self.welcome_screen)

        # To more quickly get into the game during dev
        self.start_game(None)

    def start_game(self, instance):
        """Handler for the ``click to continue`` click
        """
        self.remove_widget(self.welcome_screen)
        self.game = Game()
        self.add_widget(self.game)


class OkapiApp(App):
    """Main game class
    """
    def build(self):
        self.root = OkapiRoot()
        Window.size = (Game.ROWS * 50, Game.COLS * 50)
        return self.root


if __name__ == '__main__':
    OkapiApp().run()
