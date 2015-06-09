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

    BLANK_GROUND_CHARACTER = '.'
    EXTRA_GROUNDS = {
        "b": ground.BlockGround,
        "c": ground.CatGround,
        "r": ground.RatGround,
        "#": ground.ImpassableGround,
        ' ': ground.NullGround
    }

    CLOCK_INTERVAL = 1.0

    def __init__(self, *args, **kwargs):
        self.first_clock_cycle = True
        super(Game, self).__init__(*args, **kwargs)

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
                self.next_level_countdown = 3

            if self.next_level_countdown > 0:
                self.next_level_countdown -= 1
                return

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
        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self._move(actor, 1, 0)

    def on_press_up(self, actor=None):
        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self._move(actor, -1, 0)

    def on_press_left(self, actor=None):
        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self._move(actor, 0, -1)

    def on_press_right(self, actor=None):
        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self._move(actor, 0, 1)

    def _move(self, actor, delta_x=0, delta_y=0):
        current_ground = actor.ground
        new_ground = self.current_level.get_ground_by_coords(current_ground.x + delta_x, current_ground.y + delta_y)

        if new_ground and new_ground.can_accommodate(actor, delta_x, delta_y):
            new_ground.actor = actor
            return True
        else:
            return False

    def lose_life(self):
        print("Caught by the cat!")

    def eat_cheese(self, cheese):
        cheese.ground.actor = None
        del cheese
        print("You got 50 points!")


class WindowManager(OkapiWindowManager):

    def get_welcome_screen(self):
        return Factory.WelcomeScreen()


class RodentsRevengeApp(Okapi):

    PROJECT_PATH = PROJECT_PATH
    WINDOW_MANAGER_CLS = WindowManager
    INI_PATH = "{}/params.ini".format(PROJECT_PATH)

    GAME_CLASS = Game

    def get_application_name(self):
        return "Rodent's Revenge"

    # def resize_window(self, window):
    #     window.size = (Game.ROWS * 50, Game.COLS * 50)


if __name__ == '__main__':
    RodentsRevengeApp().run()
