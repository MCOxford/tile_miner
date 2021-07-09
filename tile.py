import arcade
from enum import Enum
from constants import *


class TileTypeError(Exception):
    pass


class TileType(Enum):
    EMPTY = 0
    ONE_TILE = 1
    TWO_TILE = 2
    THREE_TILE = 3
    FOUR_TILE = 4

    @classmethod
    def get_file_name(cls, tile_type):
        if tile_type == cls.EMPTY:
            return EMPTY_TILE_SPRITE_PATH
        if tile_type == cls.ONE_TILE:
            return ONE_TILE_SPRITE_PATH
        if tile_type == cls.TWO_TILE:
            return TWO_TILE_SPRITE_PATH
        if tile_type == cls.THREE_TILE:
            return THREE_TILE_SPRITE_PATH
        if tile_type == cls.FOUR_TILE:
            return FOUR_TILE_SPRITE_PATH


class Tile(arcade.Sprite):
    """
    Tile class.
    """

    def __init__(self, tile_type=TileType.EMPTY):
        self._check_tile_type_exists(tile_type)
        self._tile_type = tile_type
        self._coordinates = None
        try:
            self.filename = TileType.get_file_name(self._tile_type)
        except FileNotFoundError as e:
            print(f"SPRITE IMAGE CANNOT BE FOUND: {e}")
        super().__init__(self.filename)

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value):
        if not isinstance(value, tuple):
            raise TypeError('position of tile must be given as a tuple', value)
        if len(value) != 2:
            raise ValueError('Co-ordinate not of correct length', len(value))
        if not (isinstance(value[0], int) and isinstance(value[0], int)):
            raise ValueError('Co-ordinates not given as an integer pair', value)
        self._coordinates = value

    @property
    def tile_type(self):
        return self._tile_type

    @tile_type.setter
    def tile_type(self, value):
        self._check_tile_type_exists(value)
        self._tile_type = value
        # Since we updated what tile we are now using, we also must update the texture used
        self._set_tile_texture()

    @classmethod
    def _check_tile_type_exists(cls, tile_type):
        if not isinstance(tile_type, TileType):
            raise TileTypeError

    def _set_tile_texture(self):
        try:
            img = TileType.get_file_name(self._tile_type)
            self.texture = arcade.load_texture(img)
        except FileNotFoundError as e:
            print(f"SPRITE IMAGE CANNOT BE FOUND: {e}")

    def __str__(self):
        return str(self.tile_type.value)
