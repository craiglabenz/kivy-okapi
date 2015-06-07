from __future__ import print_function, absolute_import

# Engine
from engine.actors import BaseActor


class Cat(BaseActor):
    SPRITE_SOURCE = 'assets/images/cat-50.png'


class Rat(BaseActor):
    SPRITE_SOURCE = 'assets/images/rat-50.png'


class Block(BaseActor):
    SPRITE_SOURCE = 'assets/images/block-50.png'


class Cheese(BaseActor):
    SPRITE_SOURCE = 'assets/images/cheese-50.png'
