from __future__ import print_function, absolute_import, unicode_literals
import collections
import random

# Local
from .base import PureOkapiMixin
from .ground import BaseGround


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


class BaseLevel(PureOkapiMixin, object):

    def __init__(self, raw_level, ground_map, on_add_actor, level_index, game, **kwargs):
        self.raw_level = raw_level
        self.ground_map = ground_map
        self.game = game
        self.level_index = level_index

        # Callback for when there's a new actor
        self.on_add_actor = on_add_actor

        # Find the longest line
        self.cols = self.get_longest_column(raw_level)
        self.rows = len(raw_level)

        self.ground = []
        self.neighbors = {}
        self.populate_map()

    def get_ground_by_coords(self, x, y):
        # No toruses!
        if x < 0 or y < 0:
            return None
        try:
            return self.ground[y][x]
        except IndexError:
            # If the player is at the edge of the map and tries to move
            # further, no worries, we just return None which indicates
            # that the desired ground doesn't exist.
            return None

    def ground_iter(self):
        """TODO: Use this everywhere.
        """
        for row_index, row in enumerate(self.ground):
            for column_index, ground_widget in enumerate(row):
                yield self.ground[row_index][column_index]

    def populate_map(self):
        """
        Works through ``self.raw_level``, which is a list of lists of chars,
        and puts that through ``self.ground_map`` to know which terrain is where.
        """
        for row_index, row in enumerate(self.raw_level):
            self.ground.append([])
            for column_index, column_character in enumerate(row):
                # Extract the ground type
                ground_type_cls = self.ground_map[column_character]

                # Put the piece of ground in its place, with the path prefix
                self.ground[row_index].append(ground_type_cls(
                    coords=((column_index), (row_index),),
                    level=self,
                    # path_prefix=self.project_path,
                    on_add_actor=self.on_add_actor
                ))
        self.cache_neighbors()

    def cache_neighbors(self):
        for ground in self.ground_iter():
            str_ground = str(ground)
            self.neighbors.setdefault(str_ground, [])
            for direction in ground.get_directions():
                _x = ground.x + direction[0]
                _y = ground.y + direction[1]
                neighbor = self.get_ground_by_coords(_x, _y)
                if neighbor:
                    self.neighbors[str_ground].append((neighbor, direction[0], direction[1],))

    def get_frontier(self, starting_ground, actor=None):
        """Iterator for a breadth-first search of territory
        """
        if isinstance(starting_ground, BaseGround):
            pass
        elif isinstance(starting_ground, tuple):
            x, y = starting_ground
            starting_ground = self.get_ground_by_coords(x, y)
        else:
            raise ValueError("frontier starting ground must either be a tile or coordinates")

        visited = [str(starting_ground)]
        frontier = Queue()
        frontier.put(starting_ground)

        while not frontier.empty():
            _ground = frontier.get()

            for neighbor in _ground.get_walkable_neighbors(actor):
                str_neighbor = str(neighbor)
                if str_neighbor not in visited:
                    frontier.put(neighbor)
                    visited.append(str_neighbor)

            yield _ground

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

    def get_random_square(self):
        try:
            random_x = random.randint(0, len(self.ground))
            random_y = random.randint(0, len(self.ground[random_x]))
            return self.ground[random_x][random_y]
        except IndexError:
            return self.get_random_square()
