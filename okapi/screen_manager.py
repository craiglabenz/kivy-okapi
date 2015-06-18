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

    def __init__(self, configuration, game_class=None):
        self._current_screen = None

        self.configuration = configuration

        # Allow this to be passed in to prevent _forcing_ a developer
        # to define a child window manager *just* to specify this
        # reference
        self.game_class = game_class or self.GAME_CLASS

        super(ScreenManager, self).__init__()

        # Load up and audit the ``welcome_screen``
        self.welcome_screen = self.get_welcome_screen()
        if self.welcome_screen:
            assert hasattr(self.welcome_screen, 'starter'), 'Must put a clickable attribute ``starter`` on welcome screen used to start the game.'

            self.welcome_screen.starter.bind(on_press=self.start_game)
            self.current_screen = self.welcome_screen
        else:
            self.start_game(None)

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

    def render(self):
        self.clear_widgets()

        widget = self.current_screen
        if hasattr(self.current_screen, 'container'):
            widget = self.current_screen.container

        self.add_widget(widget)

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

    def start_game(self, instance):
        """Handler for the ``click to continue`` click
        """
        self.game = self.get_game(
            configuration=self.configuration
        )
        self.game.start()
        self.update_screen_from_game()

    def update_screen_from_game(self):
        self.current_screen = self.get_screen_from_game()

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print(keycode, text, modifiers)
        if not modifiers:
            command_name = 'on_press_{}'.format(keycode[1])
            command = getattr(self.current_screen, command_name, None)
            if command is not None:
                command()

        if getattr(self, 'game', None):
            command = getattr(self.game, 'on_press_{}'.format(keycode[1]), None)
            if command:
                command()
