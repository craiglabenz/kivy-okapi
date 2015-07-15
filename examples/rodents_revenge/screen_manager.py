# Okapi
from okapi.level import LevelScreen
from okapi.screen import Screen
from okapi.screen_manager import ScreenManager as OkapiScreenManager

# Local
from menu import Menu
from welcome_screen import WelcomeScreen


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
