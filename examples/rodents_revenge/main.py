from __future__ import print_function, absolute_import
import os

# Engine
from okapi.app import Okapi as OkapiApp

# Local
from end_screens import LoseScreen, VictoryScreen
from game import Game
from menu import Menu
from screen_manager import ScreenManager
from welcome_screen import WelcomeScreen


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class RodentsRevengeApp(OkapiApp):

    # For asset loading:
    PROJECT_PATH = PROJECT_PATH

    # Screens and other classes
    GAME_CLASS = Game
    LOSE_SCREEN_CLASS = LoseScreen
    MENU_CLASS = Menu
    SCREEN_MANAGER_CLS = ScreenManager
    VICTORY_SCREEN_CLASS = VictoryScreen
    WELCOME_SCREEN_CLASS = WelcomeScreen

    def get_application_name(self):
        return "Rodent's Revenge"

    # def resize_window(self, window):
    #     window.size = (1200, 1320)

if __name__ == '__main__':
    RodentsRevengeApp().run()
