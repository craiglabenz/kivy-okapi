from __future__ import print_function, absolute_import

from kivy.factory import Factory
# from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
# from kivy.clock import Clock

# In practice, `Okapi` will be installed via pip. This mimicks that.
import os
import sys
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
ENGINE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(ENGINE_PATH)

# Engine
from engine.app import Okapi
from engine.game import Game as OkapiGame
from engine.window_manager import WindowManager as OkapiWindowManager

# Local
import actors
import ground


class Game(OkapiGame):

    BLANK_GROUND_CHARACTER = 'o'
    EXTRA_GROUNDS = {
        "b": ground.BlockGround,
        "c": ground.CatGround,
        "r": ground.RatGround,
        "x": ground.ImpassableGround,
    }

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        self._player_actor = None

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

    def on_move_down(self):
        self._move(1, 0)

    def on_move_up(self):
        self._move(-1, 0)

    def on_move_left(self):
        self._move(0, -1)

    def on_move_right(self):
        self._move(0, 1)

    def _move(self, delta_x=0, delta_y=0):
        current_ground = self.player_actor.ground
        new_ground = self.current_level.get_ground_by_coords(current_ground.x + delta_x, current_ground.y + delta_y)

        if new_ground and new_ground.can_accommodate(self.player_actor):
            new_ground.actor = self.player_actor


class WindowManager(OkapiWindowManager):

    def get_welcome_screen(self):
        return Factory.WelcomeScreen()


class RodentsRevengeApp(Okapi):

    PROJECT_PATH = PROJECT_PATH
    WINDOW_MANAGER_CLS = WindowManager
    INI_PATH = "{}/params.ini".format(PROJECT_PATH)

    GAME_CLASS = Game

    # def resize_window(self, window):
    #     window.size = (Game.ROWS * 50, Game.COLS * 50)


if __name__ == '__main__':
    RodentsRevengeApp().run()
