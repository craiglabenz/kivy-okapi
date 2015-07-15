from __future__ import print_function, absolute_import
import os

# Engine
from okapi.app import Okapi as OkapiApp

# Local
from game import Game
from screen_manager import ScreenManager


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class RodentsRevengeApp(OkapiApp):

    SCREEN_MANAGER_CLS = ScreenManager
    GAME_CLASS = Game
    PROJECT_PATH = PROJECT_PATH

    def get_application_name(self):
        return "Rodent's Revenge"

    # def resize_window(self, window):
    #     window.size = (1200, 1320)

if __name__ == '__main__':
    RodentsRevengeApp().run()
