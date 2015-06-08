# Kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

# Local
from .ground import BaseGround
from .level_file_reader import LevelFileReader


class Level(GridLayout):
    PADDING = 0
    SPACING = 0

    def __init__(self, raw_level, ground_map, project_path, on_add_actor, game, **kwargs):

        self.raw_level = raw_level
        self.project_path = project_path
        self.game = game

        # Callback for when there's a new actor
        self.on_add_actor = on_add_actor

        # Zip this lists of tuples into dicts
        # self.ground_map = {key: value for key, value in ground_map}
        self.ground_map = ground_map

        # Find the longest line
        self.cols = self.get_longest_column(raw_level)
        self.rows = len(raw_level)

        kwargs.setdefault('cols', self.cols)
        kwargs.setdefault('rows', self.rows)
        kwargs.setdefault('padding', self.PADDING)
        kwargs.setdefault('spacing', self.SPACING)

        super(Level, self).__init__(**kwargs)

        self.populate_map()

    def get_ground_by_coords(self, x, y):
        # No toruses!
        if x < 0 or y < 0:
            return None
        try:
            return self.ground[x][y]
        except IndexError:
            # If the player is at the edge of the map and tries to move
            # further, no worries, we just return None which indicates
            # that the desired ground doesn't exist.
            return None

    def get_longest_column(self, raw_level):
        """
        Loops over each row, returning an integer representing the length
        of the longest row
        """
        most_columns = 0
        for row in raw_level:
            if len(row) > most_columns:
                most_columns = len(row)
        return most_columns

    def populate_map(self):
        """
        Works through ``self.raw_level``, which is a list of lists of chars,
        and puts that through ``self.ground_map`` to know which terrain is where.
        """
        self.ground = []

        for row_index, row in enumerate(self.raw_level):
            self.ground.append([])

            for column_index, column_character in enumerate(row):
                # Extract the ground type
                ground_type_cls = self.ground_map[column_character]

                # Put the piece of ground in its place, with the path prefix
                self.ground[row_index].append(ground_type_cls(
                    coords=((row_index), (column_index),),
                    level=self,
                    # path_prefix=self.project_path,
                    on_add_actor=self.on_add_actor
                ))

    def render(self):
        # self.clear_old_ground()
        for row_index, row in enumerate(self.ground):
            for column_index, ground_widget in enumerate(row):

                # Trow it on de barbey
                self.add_widget(ground_widget.render())

        return self

    def clear_old_ground(self):
        if self.ground:
            for row in self.ground:
                for column in row:
                    self.remove_widget(column)


class Game(BoxLayout):

    LEVEL_CLASS = Level
    EXTRA_GROUNDS = {}
    BLANK_GROUND_CHARACTER = ' '
    CLOCK_INTERVAL = None

    def __init__(self, configuration, project_path, current_level_index=0, **kwargs):
        self.configuration = configuration
        self.project_path = project_path
        self.current_level_index = current_level_index
        self.raw_levels = LevelFileReader(self.configuration.get('meta', 'levels_file')).levels
        super(Game, self).__init__(**kwargs)

        self.should_run_update = True
        if self.CLOCK_INTERVAL:
            Clock.schedule_interval(self.clock_update_wrapper, float(self.CLOCK_INTERVAL))

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
            project_path=self.project_path,
            on_add_actor=self.on_add_actor,
            game=self,
            # Don't tell someone they're on the 0th level. That shit's crazy
            level_index=level_index + 1
        )

    @property
    def current_level(self):
        return self._current_level

    @current_level.setter
    def current_level(self, value):
        self.clear_widgets()
        self._current_level = value

        self.add_widget(self._current_level.render())

    def on_new_level(self, new_level):
        pass

    def start(self):
        self.current_level = self.get_level(self.current_level_index)
