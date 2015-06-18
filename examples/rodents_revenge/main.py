from __future__ import print_function, absolute_import


from kivy.factory import Factory
from kivy.graphics import Color
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
# from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
# from kivy.clock import Clock

# In practice, `Okapi` will be installed via pip. This mimicks that.
import os
import sys
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
ENGINE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(ENGINE_PATH)

# Engine
from okapi.app import Okapi as OkapiApp
from okapi.engine.game import Game as OkapiGame
from okapi.level import LevelScreen
from okapi.sprite import Sprite
from okapi.screen import Screen
from okapi.screen_manager import ScreenManager as OkapiScreenManager

# Local
import actors
import ground
from welcome_screen import WelcomeScreen

MAX_DISTANCE = sys.maxint


class Game(OkapiGame):

    BLANK_GROUND_CHARACTER = '.'
    EXTRA_GROUNDS = {
        "b": ground.BlockGround,
        "c": ground.CatGround,
        "h": ground.HellcatGround,
        "r": ground.RatGround,
        "#": ground.ImpassableGround,
        ' ': ground.NullGround
    }

    CLOCK_INTERVAL = 1.0

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        self.first_clock_cycle = True
        self.rat_can_move = True

        self.player_lives = int(self.configuration.get('meta', 'starting_lives'))
        self.player_score = 0

        self.initialize_level_specific_objects()

    def on_new_level(self):
        """Reset the level-specific objects
        """
        self.initialize_level_specific_objects()

    def initialize_level_specific_objects(self):
        self._player_actor = None
        self.cats = []

    @property
    def player_actor(self):
        return self._player_actor

    @player_actor.setter
    def player_actor(self, value):
        self._player_actor = value

    def get_base_ground_class(self):
        return ground.OpenGround

    def on_add_actor(self, actor, level):
        if isinstance(actor, actors.Rat):
            self.player_actor = actor

        if isinstance(actor, actors.Cat):
            self.cats.append(actor)

    def clock_update(self, dt):
        if self.first_clock_cycle:
            self.first_clock_cycle = False
            return

        if len(self.cats) == 0:
            if getattr(self, 'next_level_countdown', None) is None:
                self.next_level_countdown = 2

            if self.next_level_countdown > 0:
                self.next_level_countdown -= 1
                return

            self.adjust_player_score((self.current_level_index + 1) * 100)
            self.next_level()

        # Don't start moving the cats until the rat moves
        if not getattr(self.current_level, 'has_rat_moved', False):
            return

        for index, cat in enumerate(self.cats):
            if cat.detect_if_trapped():

                # A cat has to be trapped for 2 clock cycles
                if not getattr(cat, 'is_trapped', False):
                    cat.is_trapped = True
                    continue

                cat.ground.actor = actors.Cheese()
                del self.cats[index]
            else:
                cat.move(self)

    def on_press_down(self, actor=None):
        if not self.rat_can_move:
            return

        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self._move(actor, 0, 1)

    def on_press_up(self, actor=None):
        if not self.rat_can_move:
            return

        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self._move(actor, 0, -1)

    def on_press_left(self, actor=None):
        if not self.rat_can_move:
            return

        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self._move(actor, -1, 0)

    def on_press_right(self, actor=None):
        if not self.rat_can_move:
            return

        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self._move(actor, 1, 0)

    def _move(self, actor, delta_x=0, delta_y=0):
        current_ground = actor.ground
        new_ground = self.current_level.get_ground_by_coords(current_ground.x + delta_x, current_ground.y + delta_y)

        if new_ground and new_ground.can_accommodate(actor, delta_x, delta_y):
            new_ground.actor = actor
            return True
        else:
            return False

    def lose_life(self):
        self.should_run_update = False
        self.rat_can_move = False
        print("Caught by the cat!")

    def next_level(self):
        super(Game, self).next_level()
        self.should_run_update = True
        self.rat_can_move = True
        self.screen_manager.refresh_level()

    def eat_cheese(self, cheese):
        cheese.ground.actor = None
        self.adjust_player_score((self.current_level_index + 1) * 50)
        del cheese

    def adjust_player_score(self, delta, should_rerender=True):
        self.player_score += delta
        if should_rerender:
            self.screen_manager.rerender_menu()


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


class ScreenManager(OkapiScreenManager):

    def rerender_menu(self):
        self.menu.render()

    @property
    def menu(self):
        if not hasattr(self, '_menu'):
            self._menu = Menu(
                self.game,
            )
        return self._menu

    def refresh_level(self):
        self.rerender_menu()
        self.screen.remove_widget(self.level_screen)
        self.level_screen = self.get_current_level_screen()
        self.screen.add_widget(self.level_screen)

    def get_welcome_screen(self):
        return WelcomeScreen()

    def get_screen_from_game(self):
        # return self.menu.render()
        self.screen = Screen()
        self.screen.add_widget(self.menu.render())

        self.level_screen = self.get_current_level_screen()
        self.screen.add_widget(self.level_screen)
        return self.screen

    def get_current_level_screen(self):
        return LevelScreen(okapi_object=self.game.current_level,
            pos_hint={'x': 0, 'y': 0.1},
            size_hint=(1.0, 0.9)
        )


class RodentsRevengeApp(OkapiApp):

    WINDOW_MANAGER_CLS = ScreenManager
    INI_PATH = "{}/params.ini".format(PROJECT_PATH)

    GAME_CLASS = Game

    def get_application_name(self):
        return "Rodent's Revenge"

    # def resize_window(self, window):
    #     window.size = (1200, 1320)


if __name__ == '__main__':
    RodentsRevengeApp().run()
