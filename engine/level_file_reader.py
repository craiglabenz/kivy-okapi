import os
import copy
import pprint
from kivy.uix.image import Image
from kivy.uix.widget import Widget

# TODO: Handle this creation somewhere in app init
IMAGES_DICTIONARY = {'okapi': '/Assets/Sprites/okapi.png',
                     'normal_ground': '/Assets/Sprites/normal_ground.png',
                     'wall': '/Assets/Sprites/wall.png'
                     }
ACTORS = {"x": 'block',
               "c": "",
               "d": "",
               "o": ""}
STATICS = {"#": "wall",
           " ": "normal_ground"
           }


class SpriteMap(object):
    def __init__(self):
        pass


class LevelFileReader(object):
    """Level loader, reads a level file, returns a level object
    """
    def __init__(self, path):
        # TODO: Get this from app init
        self.levels = self.parse_file(path)

    def parse_file(self, level_file):
        """Turns a levels file into a Levels object
        """
        # TODO: Add in the ability to have sensible whitespace
        levels = []
        current_level = []
        lines = self.open_and_read_file(level_file)

        for line in lines:

            # Ignore comment lines
            if self.is_comment(line):
                continue

            # Split up the string into a proper list
            line = [l for l in line]

            # If the line is real, we want it
            if line:
                current_level.append(line)

            # At blank line, finalize the current level and add
            # it to ``this.levels``
            else:
                if current_level:
                    self.add_to_levels(levels, current_level)
                    current_level = []

        # Don't forget trailing content if the file didn't end
        # with an empty newline
        if current_level:
            self.add_to_levels(levels, current_level)

        return levels

    def is_comment(self, line):
        """Helper function to check the line for commentage
        @param line: string returned from .readlines()
        @return: If the line is a comment
        (Any line that contains a ; is considered a comment)
        """
        if line.startswith(";"):
            return True

    def add_to_levels(self, levels, current_level):
        """Puts the current level content into the larger levels file
        """
        levels.append(copy.copy(current_level))

    def open_and_read_file(self, level_file):
        """I/O Handler for level files
        @param level_file: The target file to read
        @return lines: array of strings, representing level rows
        """
        lines = []
        try:
            with open(level_file, 'r') as my_file:
                for line in my_file.readlines():
                    lines.append(line.rstrip(os.linesep))
                return lines
        except IOError:
            raise IOError("Level File Not Found!")


# class Sprite(Image):
#     def __init__(self, **kwargs):
#         super(Sprite, self).__init__(**kwargs)
#         self.size = self.texture_size


# class Ground(Widget):
#     def __init__(self):
#         self.sprite_path = None
#         self.actor = None

#         def get_sprite_path(self):
#             if self.sprite_path:
#                 pass



#         def render(self):
#             self.add_widget(Sprite(source=self.get_sprite_path())
#             if self.actor:
#                 self.add_widget(Sprite(source=self.actor_path))


# class Actor(Ground):
#     def __init__(self):
#         super(Ground, self).__init__()
#         # self.actor = actor


# class Generic(object):
#     def __init__(self):
#         self.name = 'Generic'


# class Child(Generic):
#     def __init__(self):
#         super(Generic, self).__init__()
#         self.name = 'Child'


# class GameStateInitializer(object):
#     def __init__(self, level_number):
#         self.raw_levels = LevelFileReader().levels
#         self.level_number = level_number
#         self.spritemap = SpriteMap()

#     def create_objects(self):
#         game_objects = []
#         raw_level = copy.copy(self.raw_levels[self.level_number])
#         for row in raw_level:
#             game_objects.append([self.objectify(element) for element in row])
#         return game_objects

#     def objectify(self, raw_object):
#         """Objectify level raw text into objects
#         """
#         spritemap = SpriteMap()
#         if raw_object in spritemap.actors.keys():
#             return Actor(raw_object)
#         else:
#             return Ground(raw_object)


if __name__ == '__main__':
    gs = GameStateInitializer(1)
    gs.create_objects()
