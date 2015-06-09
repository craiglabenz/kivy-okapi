# Kivy
from kivy.uix.boxlayout import BoxLayout


class WindowManager(BoxLayout):
    """
    Class that handles toggling between windows. So that's managing
    the loading screen, game screen, victory screen, high scores, etc.
    """

    GAME_CLASS = None

    def __init__(self, configuration, project_path, game_class=None):
        self._current_screen = None

        self.configuration = configuration
        self.project_path = project_path

        # Allow this to be passed in to prevent _forcing_ a developer
        # to define a child window manager *just* to specify this
        # reference
        if game_class is not None:
            self.GAME_CLASS = game_class

        super(WindowManager, self).__init__()

        # Load up and audit the ``welcome_screen``
        self.welcome_screen = self.get_welcome_screen()
        assert hasattr(self.welcome_screen, 'starter'), 'Must put a clickable attribute ``starter`` on welcome screen used to start the game.'

        self.welcome_screen.starter.bind(on_press=self.start_game)
        self.current_screen = self.welcome_screen

        # To more quickly get into the game during dev
        self.start_game(None)

    def get_welcome_screen(self, *args, **kwargs):
        """Should return some sort of ``Widget`` to use as your game's welcome screen.
        """
        raise NotImplementedError()

    def get_game_class(self):
        """Helper to get the actual Game Class
        """
        assert self.GAME_CLASS is not None, 'Failed to set a Game class on ``WindowManager``'
        return self.GAME_CLASS

    def get_game(self, **kwargs):
        """Should return the actual Game object.
        """
        return self.get_game_class()(**kwargs)

    def render(self):
        self.clear_widgets()
        self.add_widget(self.current_screen)

    @property
    def current_screen(self):
        """
        Property used to wrap whichever screen is current to facilitate
        the swapping of screens and also automatically directing all user
        input to the correct screen.
        """
        return self._current_screen

    @current_screen.setter
    def current_screen(self, value):
        """
        Setter for the @current_screen prop that also triggers a render.
        """
        self._current_screen = value
        self.render()

    def start_game(self, instance):
        """Handler for the ``click to continue`` click
        """
        self.game = self.get_game(
            configuration=self.configuration,
            project_path=self.project_path
        )
        self.current_screen = self.game
        self.game.start()

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not modifiers:
            command_name = 'on_press_{}'.format(keycode[1])
            command = getattr(self.current_screen, command_name, None)
            if command is not None:
                command()


