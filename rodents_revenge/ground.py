# mimicks pip install of engine
import os
import sys
ENGINE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(ENGINE_PATH)

# Engine
from engine import ground as okapi_ground

# Local
import actors


class OpenGround(okapi_ground.BaseGround):
    sprite_path = 'assets/images/ground-50.png'


class CatGround(OpenGround):
    initial_actor_cls = actors.Cat


class RatGround(OpenGround):
    initial_actor_cls = actors.Rat


class BlockGround(OpenGround):
    initial_actor_cls = actors.Block


class ImpassableGround(okapi_ground.BaseGround):
    is_passable = False
    sprite_path = 'assets/images/impassable-ground-50.png'
