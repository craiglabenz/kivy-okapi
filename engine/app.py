from __future__ import print_function, absolute_import, unicode_literals
from ConfigParser import SafeConfigParser
import codecs

# Kivy
from kivy.app import App
from kivy.core.window import Window


class Okapi(App):
    """Main game class
    """

    INI_PATH = None
    GAME_CLASS = None
    PROJECT_PATH = None
    WINDOW_MANAGER_CLS = None

    def get_ini_path(self):
        assert self.INI_PATH is not None, 'Failed to set an ``INI_PATH`` on {}'.format(type(self).__name__)
        return self.INI_PATH

    def load_configuration(self, path):
        config = SafeConfigParser()

        with codecs.open(path, 'r', encoding='utf-8') as f:
            config.readfp(f)

        return config

    def get_window_manager(self, *args, **kwargs):
        assert self.WINDOW_MANAGER_CLS is not None, 'Failed to set a ``WINDOW_MANAGER_CLS`` attr on your App'
        return self.WINDOW_MANAGER_CLS(*args, **kwargs)

    def resize_window(self, window):
        pass

    def build(self):
        self.configuration = self.load_configuration(self.get_ini_path())
        self.root = self.get_window_manager(
            configuration=self.configuration,
            project_path=self.PROJECT_PATH,
            game_class=self.GAME_CLASS
        )
        self.resize_window(Window)

        return self.root

