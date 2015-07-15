## Okapi

#### What it is
A library to build grid-based games using Kivy 1.9


#### Installation

Installing packages with Kivy is a joy because you cannot use virtual environments (assuming you use the Kivy package installer). Kivy creates its own unique snowflake environment, then provides a `kivy` command-line utility that heavily modifies your `PYTHONPATH` before ultimately launching the python interpreter. Thus, virtual environments are off the table, as none of their packages can be imported after using `kivy`.

1. [Download the Kivy installer](http://kivy.org/docs/installation/installation.html) and use it to install Kivy.
2. Next, install `okapi` from PyPI using Kivy's `pip`: `$ kivy -m pip install kivy-okapi`

#### Launching an `Okapi` App

Once `Okapi` is installed where Kivy is willing to look, you can simply navigate into any game folder and run `kivy main.py` like normal, and all Okapi libraries will be available.


## Building a Game with `Okapi`

For reference, a complete example is provided in the `/examples/rodents_revenge` directory

#### Create an `OkapiApp` class

In your `main.py` file, provide this bare minimum skeleton:

```py
# Okapi
from okapi.app import Okapi as OkapiApp

# Local
from game import Game
from screen_manager import ScreenManager


class MyGameApp(OkapiApp):

    GAME_CLASS = Game
    SCREEN_MANAGER_CLS = ScreenManager
    PROJECT_PATH = PROJECT_PATH

    def get_application_name(self):
        return "My Game"

if __name__ == '__main__':
    MyGameApp().run()

```

#### Kivy's `build()` method

Those familiar with Kivy know that the your project's main `App` class is required to define a `build()` function that returns the root widget. For `Okapi`, that root widget is of the `ScreenManager` class. It is this widget's job to swap in and out loading screens, the game screen, menu screens, high score screens, etc.

An example of overriding the `ScreenManager` class is provided in the Rodent's Revenge game, but here is a bare minimum example:

```py
# Okapi
from okapi.screen_manager import ScreenManager as OkapiScreenManager

# Local
from welcome_screen import WelcomeScreen

class ScreenManager(OkapiScreenManager):

    def get_welcome_screen(self):
        """
        Optional.

        If implemented, should return a `Screen` widget that says something
        like "Hello, welcome to my game!" and has a click listener. The
        `OkapiScreenManager` will listen for that click and start the game.
        """
        return WelcomeScreen()

    def get_screen_from_game(self):
        """
        Required.

        Should do something with `self.game` to get a Screen widget used to start
        and render the game.
        """
        return self.game.get_screen()

```


#### Listening to Kivy's clock

The `ScreenManager` is also a clean interface to Kivy's clock module. Your `ScreenManager` keeps track of a `current_screen` attribute,
and whenever this changes it unregisters any clock listeners from the previous screen and registers the new screen's clock listeners.

To register clock handlers, define them like so:

```py
# Okapi
from okapi.screen import Screen


class SomeScreen(Screen):

    def every_second(self):
        # Do stuff

    def every_other_second(self):
        # Do more stuff

    def get_clock_tuple(self):
        # Option 1
        return (self.every_second, 1.0,)

        # or Option 2
        return (
            (self.every_second, 1.0,),
            (self.every_other_second, 2.0,),
        )
```

The `ScreenManager` class will also drill down and check all top-level children of a screen to see if any have clock listeners.


#### Listening to keyboard input

The `ScreenManager` also listens to all keyboard input and passes it to both `self.game` and whatever is its `current_screen`. To listen for clicks to the "down arrow":

```py
# Okapi
from okapi.screen import Screen


class SomeScreen(Screen):

    def on_press_down(self):
        # Do stuff

    def on_press_y(self):
        # Do stuff

    def on_press_cmd_w(self):
        # Do stuff

    def on_press_alt_shift_s(self):
        # Do stuff

```

The above definitions also apply to your `Game` class.

If there are > 1 modifier keys pressed (`shift`, `command`, `alt`, etc) they will be alphabetized for consistency.

#### The `Game` class

The `Game` class is where you put your fun game logic! Define one like so:


```py
# Engine
from okapi.engine.game import Game as OkapiGame


class Game(OkapiGame):

    # Used by `OkapiGame` to provide default functionality for
    # `self.get_clock_tuple()`
    # Rodent's Revenge only has to update once per second
    CLOCK_INTERVAL = 1.0

    # Default blank ground -- empty walkable space
    BLANK_GROUND_CHARACTER = '.'

    # Other special types of ground. Maybe impassable, or maybe
    # containing various actors
    EXTRA_GROUNDS = {
        "b": ground.BlockGround,
        "#": ground.ImpassableGround,
    }

    def clock_update(self, dt):
        # Make the game happen!

    def on_press_down(self):
        # Move something down!

```


#### Moving actors

The `OkapiGame` class provides a function called `move_actor`. Let's say you are building a chess app. To move a knight, you would make a call like this:

```py
self.game.move_actor(self.white_knight_1, 1, 2)
```

This will immediately cause a reanimation, showing the white knight having just moved.


#### Moving Rules

Moving legality is determined by the target ground's `can_accommodate()` method. By default, this rejects movements into occupied territory. Of course, that rule makes little sense for chess, so for that example you'd want to override that function to accept new pieces at any time, and to remove from the game any piece currently found in that spot.


## Rodent's Revenge

One of my favorite games as a kid was [Rodent's Revenge](https://en.wikipedia.org/wiki/Rodent%27s_Revenge). It's a simple game of block pushing and cat trapping, but the gameplay is simple and quick enough that the game is very addicting.

So much did I like this game, in fact, that I cloned it as a working example of `Okapi`.

![Rodent's Revenge](https://raw.githubusercontent.com/craiglabenz/kivy-okapi/master/media/okapi-rodents-revenge.png)


