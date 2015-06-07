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
import ground


class Game(OkapiGame):

    BLANK_GROUND_CHARACTER = 'o'
    EXTRA_GROUNDS = {
        "b": ground.BlockGround,
        "c": ground.CatGround,
        "r": ground.RatGround,
        "x": ground.ImpassableGround,
    }

    def get_base_ground_class(self):
        return ground.OpenGround


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
