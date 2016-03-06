from __future__ import print_function, absolute_import, unicode_literals

# Kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout


class ScreenManager(BoxLayout):
    """
    Class that handles toggling between windows. So that's managing
    the loading screen, game screen, victory screen, high scores, etc.
    """

    GAME_CLASS = None
    LOSE_SCREEN_CLASS = None
    MENU_CLASS = None
    VICTORY_SCREEN_CLASS = None
    WELCOME_SCREEN_CLASS = None

    def __init__(self, configuration, game_class=None, menu_class=None, welcome_screen_class=None,
                 lose_screen_class=None, victory_screen_class=None):
        self._current_screen = None

        self.configuration = configuration

        # Allow this to be passed in to prevent _forcing_ a developer
        # to define a child window manager *just* to specify this reference
        self.lose_screen_class = lose_screen_class or self.LOSE_SCREEN_CLASS
        self.game_class = game_class or self.GAME_CLASS
        self.menu_class = menu_class or self.MENU_CLASS
        self.victory_screen_class = victory_screen_class or self.VICTORY_SCREEN_CLASS
        self.welcome_screen_class = welcome_screen_class or self.WELCOME_SCREEN_CLASS

        super(ScreenManager, self).__init__()

        # Load up and audit the ``welcome_screen``
        self.welcome_screen = self.get_welcome_screen(start_game_handler=self.start_game)
        if self.welcome_screen:

            if hasattr(self.welcome_screen, 'starter'):
                self.welcome_screen.starter.bind(on_press=self.start_game)

            self.current_screen = self.welcome_screen
        else:
            self.start_game()

    def get_welcome_screen(self, *args, **kwargs):
        """Should return some sort of ``Widget`` to use as your game's welcome screen.
        """
        return None

    def get_game_class(self):
        """Helper to get the actual Game Class
        """
        assert self.game_class is not None, 'Failed to set a Game class on ``ScreenManager``'
        return self.game_class

    def get_game(self, **kwargs):
        """Should return the actual Game object.
        """
        kwargs.setdefault('screen_manager', self)
        return self.get_game_class()(**kwargs)

    def get_welcome_screen(self, **kwargs):
        return self.get_welcome_screen_class()(**kwargs)

    def get_welcome_screen_class(self):
        return self.welcome_screen_class

    def get_victory_screen(self, **kwargs):
        return self.get_victory_screen_class()(**kwargs)

    def get_victory_screen_class(self):
        return self.victory_screen_class

    def render_victory_screen(self):
        self.current_screen = self.get_victory_screen(
            game=self.game,
            restart_handler=self.start_game
        ).render()

    def get_lose_screen(self, **kwargs):
        return self.get_lose_screen_class()(**kwargs)

    def get_lose_screen_class(self):
        return self.lose_screen_class

    def render_lose_screen(self):
        self.current_screen = self.get_lose_screen(
            game=self.game,
            restart_handler=self.start_game
        ).render()

    def render(self):
        self.clear_widgets()

        widget = self.current_screen
        if hasattr(self.current_screen, 'container'):
            widget = self.current_screen.container

        self.add_widget(widget)

    def rerender_menu(self):
        self.menu.render()

    @property
    def current_screen(self):
        """
        Property used to wrap whichever screen is current to facilitate
        the swapping of screens and also automatically directing all user
        input to the correct screen.
        """
        return self._current_screen

    def unregister_with_clock(self):
        """
        Unregisters either:
            (cb, freq,)
        or
            (
                (cb, freq,),
                (cb, freq,),
                ...
            )
        """
        if getattr(self, '_current_screen', None) and getattr(self._current_screen, 'get_clock_tuple', None):
            clock_tuple = self._current_screen.get_clock_tuple()
            if clock_tuple:
                if isinstance(clock_tuple[0], tuple):
                    for _ in clock_tuple:
                        Clock.unschedule(_[0])
                else:
                    Clock.unschedule(clock_tuple[0])

    def register_with_clock(self):
        """
        Registers either:
            (cb, freq,)
        or
            (
                (cb, freq,),
                (cb, freq,),
                ...
            )
        """
        if getattr(self._current_screen, 'get_clock_tuple', None):
            clock_tuple = self._current_screen.get_clock_tuple()
            if clock_tuple:
                if isinstance(clock_tuple[0], tuple):
                    for _ in clock_tuple:
                        Clock.schedule_interval(*_)
                else:
                    Clock.schedule_interval(*clock_tuple)

    @current_screen.setter
    def current_screen(self, value):
        """
        Setter for the @current_screen prop that also triggers a render.
        """
        self.unregister_with_clock()
        self._current_screen = value
        self.register_with_clock()
        self.render()

    @property
    def menu(self):
        if not hasattr(self, '_menu'):
            self._menu = self.get_menu(self.game)
        return self._menu

    @menu.setter
    def menu(self, val):
        self._menu = val

    def get_menu(self, game):
        return self.menu_class(self.game)

    def start_game(self, instance=None):
        """Handler for the ``click to start`` click

        Arguments:
        @instance       The click event. May or may not be present, so likely ignore.
        """
        self.game = self.get_game(
            configuration=self.configuration
        )
        self.game.start()
        self.menu = self.get_menu(self.game)
        self.update_screen_from_game()

    def update_screen_from_game(self):
        self.current_screen = self.get_screen_from_game()

    def get_screen_from_game(self):
        raise NotImplementedError("Your `ScreenManager` class must implement this function.")

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        if not modifiers:
            command_name = 'on_press_{}'.format(keycode[1])
            command = getattr(self.current_screen, command_name, None)
            if command is not None:
                command()

            wildcard_handler = getattr(self.current_screen, 'on_press_any', None)
            if wildcard_handler is not None:
                wildcard_handler(keycode, text)

        if modifiers:
            modifiers.sort()
            modifiers_string = "_".join(modifiers)
            command_name = 'on_press_{}_{}'.format(modifiers_string, keycode[1])
            command = getattr(self.current_screen, command_name, None)
            if command is not None:
                command

        if getattr(self, 'game', None):
            command = getattr(self.game, 'on_press_{}'.format(keycode[1]), None)
            if command:
                command()
