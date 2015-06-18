#!/usr/bin/env python
import copy
import unittest

from okapi.engine.actors import BaseActor
from okapi.engine.ground import BaseGround
from okapi.engine.level import BaseLevel


class WallGround(BaseGround):
    is_passable = False


class ActorGround(BaseGround):
    initial_actor_cls = BaseActor


class TestGroundFrontier(unittest.TestCase):

    MOCK_LEVEL_1 = [
        ['.', '.', '.'],
        ['.', '#', '.'],
        ['.', '#', '.'],
    ]

    MOCK_LEVEL_2 = [
        ['.', '.', '.'],
        ['.', '#', '.'],
        ['a', '#', '.'],
    ]

    MOCK_LEVEL_3 = [
        ['.', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '.'],
        ['.', '#', 'a', '.', '#', '.'],
        ['.', '#', '.', '.', '#', '.'],
        ['.', '.', '.', '.', '.', '.'],
    ]

    MOCK_LEVEL_4 = [
        ['.', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '.'],
        ['.', '#', '.', '.', '#', '.'],
        ['.', '#', 'a', '.', '#', '.'],
        ['.', '#', '#', '#', '#', '.'],
    ]

    GROUND_MAP = {
        '.': BaseGround,
        '#': WallGround,
        'a': ActorGround
    }

    def _on_add_actor(self, *args, **kwargs):
        pass

    def __getattr__(self, attr_name):
        if not attr_name.startswith('get_level_'):
            raise AttributeError(attr_name)

        level_id = int(attr_name[10:])
        return lambda: self.get_level(level_id)

    def get_level(self, level_id):
        raw_level = copy.copy(getattr(self, 'MOCK_LEVEL_{}'.format(level_id)))
        return BaseLevel(raw_level, self.GROUND_MAP.copy(), self._on_add_actor, 1, None)

    def _assert_coords(self, ground, x, y):
        self.assertEquals(ground.x, x)
        self.assertEquals(ground.y, y)

    def test_iter(self):
        """
        You owe me all the squares of ground. Nothing fancy.
        """
        level = self.get_level_1()
        ground = [g for g in level.ground_iter()]
        self.assertEquals(len(ground), 9)

        level = self.get_level_3()
        ground = [g for g in level.ground_iter()]
        self.assertEquals(len(ground), 30)

    def test_frontier(self):
        """
        Simply crawl out and cover all the territory.
        """
        level = self.get_level_1()
        ground = [g for g in level.get_frontier((0, 2))]
        self.assertEquals(len(ground), 9)

        self._assert_coords(ground[0], 0, 2)
        self._assert_coords(ground[1], 0, 1)
        self._assert_coords(ground[2], 1, 1)
        self._assert_coords(ground[3], 1, 2)
        self._assert_coords(ground[4], 0, 0)
        self._assert_coords(ground[5], 1, 0)
        self._assert_coords(ground[6], 2, 0)
        self._assert_coords(ground[7], 2, 1)
        self._assert_coords(ground[8], 2, 2)

    def test_frontier_with_actor(self):
        """
        The actor can't walk on walls, so those squards (1, 1,)
        and (1, 2,) are no longer part of the frontier.
        """
        level = self.get_level_2()
        ground = level.get_ground_by_coords(0, 2)

        ground = [g for g in level.get_frontier(ground, ground.actor)]
        self.assertEquals(len(ground), 7)

        self._assert_coords(ground[0], 0, 2)
        self._assert_coords(ground[1], 0, 1)
        self._assert_coords(ground[2], 0, 0)
        self._assert_coords(ground[3], 1, 0)
        self._assert_coords(ground[4], 2, 0)
        self._assert_coords(ground[5], 2, 1)
        self._assert_coords(ground[6], 2, 2)

    def test_pathing(self):
        # Should move down since that route is open
        level = self.get_level_3()
        start = level.get_ground_by_coords(2, 2)
        target = level.get_ground_by_coords(2, 0)
        delta_x, delta_y = start.actor.get_best_move_toward(target)
        self.assertEquals(delta_x, 0)
        self.assertEquals(delta_y, 1)

    # def test_pathing_fallback(self):
    #     # Should move up since ultimately trapped, and up is the direct route
    #     level = self.get_level_4()
    #     ground = level.get_ground_by_coords(2, 2)
    #     delta_x, delta_y = ground.actor.get_best_move_toward(2, 0)

    #     self.assertEquals(delta_x, 0)
    #     self.assertEquals(delta_y, -1)


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    unittest.main()
