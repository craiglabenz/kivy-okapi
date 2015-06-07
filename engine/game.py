import os

# Kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

# Local
from .ground import BaseGround
from .level_file_reader import LevelFileReader


class Level(GridLayout):
    PADDING = 0
    SPACING = 0

    def __init__(self, raw_level, ground_map, project_path, **kwargs):

        self.raw_level = raw_level
        self.project_path = project_path

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

        self.objectify()

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

    def objectify(self):
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
                self.ground[row_index].append(ground_type_cls(path_prefix=self.project_path))

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

    def __init__(self, configuration, project_path, **kwargs):
        self.configuration = configuration
        self.project_path = project_path
        self.raw_levels = LevelFileReader(self.configuration.get('meta', 'levels_file')).levels
        super(Game, self).__init__(**kwargs)

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

    def get_levels(self):
        for index, raw_level in enumerate(self.raw_levels):
            yield self.get_level_class(index)(
                raw_level=raw_level,
                # ground_map=self.configuration.items('levelmap'),
                ground_map=self.get_ground_map(),
                project_path=self.project_path
            )

    def start(self):
        # Totally wrong, but not sure yet how to do this
        levels = [level for level in self.get_levels()]

        first_level = levels[0]
        self.add_widget(first_level.render())

