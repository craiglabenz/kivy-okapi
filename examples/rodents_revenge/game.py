# Engine
from okapi.engine.game import Game as OkapiGame

# Local
import actors
import ground


class Game(OkapiGame):

    BLANK_GROUND_CHARACTER = '.'
    EXTRA_GROUNDS = {
        "b": ground.BlockGround,
        "c": ground.CatGround,
        "h": ground.HellcatGround,
        "r": ground.RatGround,
        "#": ground.ImpassableGround,
        ' ': ground.NullGround
    }

    CLOCK_INTERVAL = 1.0

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        self.first_clock_cycle = True
        self.rat_can_move = True

        self.player_lives = int(self.configuration.get('meta', 'starting_lives'))
        self.player_score = 0

        self.pause_for = 0

        self.initialize_level_specific_objects()

    def on_new_level(self):
        """Reset the level-specific objects
        """
        self.initialize_level_specific_objects()

    def initialize_level_specific_objects(self):
        self._player_actor = None
        self.cats = []

    @property
    def player_actor(self):
        return self._player_actor

    @player_actor.setter
    def player_actor(self, value):
        self._player_actor = value

    def get_base_ground_class(self):
        return ground.OpenGround

    def on_add_actor(self, actor, level):
        if isinstance(actor, actors.Rat):
            self.player_actor = actor

        if isinstance(actor, actors.Cat):
            self.cats.append(actor)

    def clock_update(self, dt):
        if self.first_clock_cycle:
            self.first_clock_cycle = False
            return

        if self.pause_for > 0:
            self.pause_for -= 1
            return

        if len(self.cats) == 0:
            if getattr(self, 'next_level_countdown', None) is None:
                self.next_level_countdown = 2

            # Allow a few seconds for the player to eat the cheese
            # the last cat turned into
            if self.next_level_countdown > 0:
                self.next_level_countdown -= 1
                return

            self.adjust_player_score((self.current_level_index + 1) * 100)
            self.next_level()

        # Don't start moving the cats until the rat moves
        if not getattr(self.current_level, 'has_rat_moved', False):
            return

        for index, cat in enumerate(self.cats):
            if cat.detect_if_trapped():

                # A cat has to be trapped for 2 clock cycles
                if not getattr(cat, 'is_trapped', False):
                    cat.is_trapped = True
                    continue

                cat.ground.actor = actors.Cheese()
                del self.cats[index]
            else:
                cat.move(self)

    def get_score(self):
        return self.player_score

    def on_press_down(self, actor=None):
        if not self.rat_can_move:
            return
        self.pause_for = 0
        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self.move_actor(actor, 0, 1)

    def on_press_up(self, actor=None):
        if not self.rat_can_move:
            return
        self.pause_for = 0
        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self.move_actor(actor, 0, -1)

    def on_press_left(self, actor=None):
        if not self.rat_can_move:
            return
        self.pause_for = 0
        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self.move_actor(actor, -1, 0)

    def on_press_right(self, actor=None):
        if not self.rat_can_move:
            return
        self.pause_for = 0
        self.current_level.has_rat_moved = True
        actor = actor or self.player_actor
        self.move_actor(actor, 1, 0)

    def move_actor(self, actor, delta_x=0, delta_y=0):
        current_ground = actor.ground
        new_ground = self.current_level.get_ground_by_coords(current_ground.x + delta_x, current_ground.y + delta_y)

        if new_ground and new_ground.can_accommodate(actor, delta_x, delta_y):
            new_ground.actor = actor
            return True
        else:
            return False

    def lose_life(self):
        self.should_run_update = False
        self.player_lives -= 1

        if self.player_lives == 0:
            self.render_lose_screen()
            return

        self.screen_manager.rerender_menu()
        self.pause_for = 2

        while True:
            ground = self.current_level.get_random_square()
            if ground.is_passable and not ground.actor:
                ground.actor = self.player_actor
                self.should_run_update = True
                return

    def render_lose_screen(self):
        self.screen_manager.render_lose_screen()

    def next_level(self):
        super(Game, self).next_level()
        self.should_run_update = True
        self.rat_can_move = True
        self.screen_manager.refresh_level()

    def eat_cheese(self, cheese):
        cheese.ground.actor = None
        self.adjust_player_score((self.current_level_index + 1) * 50)
        del cheese

    def adjust_player_score(self, delta, should_rerender=True):
        self.player_score += delta
        if should_rerender:
            self.screen_manager.rerender_menu()
