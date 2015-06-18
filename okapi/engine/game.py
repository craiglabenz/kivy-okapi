from __future__ import print_function, absolute_import

# Local
from .ground import BaseGround
from .level import BaseLevel
from .level_file_reader import LevelFileReader


class Game(object):

    LEVEL_CLASS = BaseLevel
    EXTRA_GROUNDS = {}
    BLANK_GROUND_CHARACTER = '.'
    CLOCK_INTERVAL = None

    def __init__(self, configuration, screen_manager, current_level_index=0, **kwargs):
        self.configuration = configuration
        self.current_level_index = current_level_index
        self.raw_levels = LevelFileReader(self.configuration.get('meta', 'levels_file')).levels
        self.should_run_update = kwargs.get('should_run_update', True)
        self.screen_manager = screen_manager

    def get_clock_interval(self):
        return self.CLOCK_INTERVAL

    def get_clock_tuple(self):
        clock_interval = self.get_clock_interval()
        if clock_interval:
            return self.clock_update_wrapper, clock_interval
        else:
            return None, None

    def clock_update_wrapper(self, dt):
        if self.should_run_update:
            self.clock_update(dt)

    def clock_update(self, dt):
        pass

    def get_ground_map(self):
        """
        Merges the base ground dictionary with the "extra_grounds",
        which may or may not exist in any given game. You could imagine
        a game like Chess would not require any.
        """
        # Build the base ground dictionary
        ground_map = {
            self.get_base_ground_character(): self.get_base_ground_class()
        }

        # Merge in extra grounds if they are specified
        extra_grounds = self.get_extra_grounds()
        if extra_grounds:
            ground_map.update(extra_grounds)

        return ground_map

    def get_base_ground_character(self):
        return self.BLANK_GROUND_CHARACTER

    def get_extra_grounds(self):
        return self.EXTRA_GROUNDS

    def get_base_ground_class(self):
        return BaseGround

    def get_level_class(self, level_number):
        return self.LEVEL_CLASS

    def on_add_actor(self, actor, level):
        pass

    def get_level(self, level_index):
        self.on_new_level()
        return self.get_level_class(level_index)(
            raw_level=self.raw_levels[level_index],
            ground_map=self.get_ground_map(),
            on_add_actor=self.on_add_actor,
            index=level_index,
            game=self,
            # Don't tell someone they're on the 0th level. That shit's crazy
            level_index=level_index + 1
        )

    @property
    def current_level(self):
        return self._current_level

    @current_level.setter
    def current_level(self, value):
        self._current_level = value

    def on_new_level(self):
        pass

    def next_level(self):
        self.current_level_index += 1
        self.load_level()

    def load_level(self):
        next_level = self.get_level(self.current_level_index)
        if next_level:
            self.current_level = next_level
        else:
            print ("Win screen!")

    def start(self):
        self.load_level()
