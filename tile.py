import arcade
from enum import Enum
import os

# Tile image file paths
dirname = os.path.dirname(__file__)
EMPTY_TILE_SPRITE_PATH = os.path.join(dirname, "images/empty_alt.png")
ONE_TILE_SPRITE_PATH = os.path.join(dirname, "images/one_alt.png")
TWO_TILE_SPRITE_PATH = os.path.join(dirname, "images/two_alt.png")
THREE_TILE_SPRITE_PATH = os.path.join(dirname, "images/three_alt.png")
FOUR_TILE_SPRITE_PATH = os.path.join(dirname, "images/four_alt.png")


class TileTypeError(Exception):

    def __init__(self, msg, args):
        super().__init__(msg, args)


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
        # Tile type used. This represents the 'block' currently being used.
        self.tile_type: TileType = tile_type
        # Grid coordinates for the tile
        self.coordinates: tuple = (0, 0)
        try:
            self.filename: str = TileType.get_file_name(self._tile_type)
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

    @classmethod
    def _check_tile_type_exists(cls, tile_type):
        """
        Check tile_type is indeed a TileType member.
        :param tile_type: parameter to check
        :return:
        """
        if not isinstance(tile_type, TileType):
            raise TileTypeError("Invalid tile type used", tile_type)

    def set_tile_texture(self):
        """
        Load texture for Tile object using the specified file path. Should use when tile_type field is set to a
        different value.
        :return:
        """
        try:
            img = TileType.get_file_name(self._tile_type)
            self.texture = arcade.load_texture(img)
        except FileNotFoundError as e:
            print(f"SPRITE IMAGE CANNOT BE FOUND: {e}")

    def __str__(self):
        return str(self.tile_type.value)


if __name__ == "__main__":
    tile = Tile(TileType.ONE_TILE)
