import arcade
from constants import TYPES


def check_key_exists(key):
    if key not in TYPES.keys():
        raise KeyError('tile type given not listed', key)


class Tile(arcade.Sprite):
    """
    Tile class.
    """

    def __init__(self, tile_type=0):
        check_key_exists(tile_type)
        self._tile_type = tile_type
        self._coordinates = None
        self.filename = TYPES[self._tile_type]
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
        check_key_exists(value)
        self._tile_type = value
        # Since we updated what tile we are now using, we also must update the texture used
        self.set_tile_texture()

    def set_tile_texture(self):
        self.texture = arcade.load_texture(TYPES[self._tile_type])

    def __str__(self):
        return str(self.tile_type)







