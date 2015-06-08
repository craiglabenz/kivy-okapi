from __future__ import print_function, absolute_import

# Engine
from engine.actors import BaseActor


class Cat(BaseActor):
    SPRITE_SOURCE = 'assets/images/cat-50.png'
    IS_MOVABLE = True

    MOVES = {
        "1": (-1, -1),
        "2": (0, -1),
        "3": (1, -1),
        "4": (-1, 0),
        "6": (1, 0),
        "7": (-1, 1),
        "8": (0, 1),
        "9": (1, 1),
    }

    def move(self, game):
        """
        If the cat is the "c" below, and the rat is "r",
        the cat will debate between moving to spots 2, 3, and 6.

           123..r.
           4c6....
           789....
        """
        considered_moves = []

        my_x = self.ground.x
        my_y = self.ground.y

        mouse_x = game.player_actor.ground.x
        mouse_y = game.player_actor.ground.y

        differential_x = my_x - mouse_x
        differential_y = my_y - mouse_y

        # Humanize the situation to make the next code block
        # more manageable. Note that these words are the direction
        # the cat needs to travel to get to the rat
        humanized_x = 'horizontally_flat'
        if differential_x > 0:
            humanized_x = 'left'
        elif differential_x < 0:
            humanized_x = 'right'

        humanized_y = 'vertically_flat'
        if differential_y > 0:
            humanized_y = 'up'
        elif differential_y < 0:
            humanized_y = 'down'

        abs_x = abs(differential_x)
        abs_y = abs(differential_y)

        # This block always honors Y over X. If it turns out that
        # abs_x > abs_y, we can swap indices 1 and 2 in this list
        if humanized_x == 'right':
            if humanized_y == 'up':
                considered_moves += ["3", "2", "6"]
            elif humanized_y == 'down':
                considered_moves += ["9", "8", "6"]
            elif humanized_y == "vertically_flat":
                considered_moves += ["6", "3", "9"]
        elif humanized_x == 'left':
            if humanized_y == 'up':
                considered_moves += ["1", "2", "4"]
            elif humanized_y == 'down':
                considered_moves += ["7", "8", "4"]
            elif humanized_y == "vertically_flat":
                considered_moves += ["4", "1", "7"]
        elif humanized_x == "horizontally_flat":
            if humanized_y == 'up':
                considered_moves += ["2", "1", "3"]
            elif humanized_y == 'down':
                considered_moves += ["8", "7", "9"]
            elif humanized_y == "vertically_flat":
                print("Sounds like the cats won.")

        if abs_x > abs_y:
            considered_moves = [considered_moves[0], considered_moves[2], considered_moves[1]]

        for considered_move in considered_moves:
            x, y = self.MOVES[considered_move]
            has_moved = game._move(self, x, y)

            if has_moved:
                break

    def detect_if_trapped(self):
        for key, value in self.MOVES.items():
            x, y = value
            new_ground = self.ground.level.get_ground_by_coords(self.ground.x + x, self.ground.y + y)

            if new_ground and new_ground.can_accommodate(self, x, y):
                return False

        return True


class Rat(BaseActor):
    SPRITE_SOURCE = 'assets/images/rat-50.png'
    IS_MOVABLE = True


class Block(BaseActor):
    SPRITE_SOURCE = 'assets/images/fancy-block-50.png'
    IS_MOVABLE = True


class Cheese(BaseActor):
    SPRITE_SOURCE = 'assets/images/fancy-cheese-50.png'
    IS_MOVABLE = False
