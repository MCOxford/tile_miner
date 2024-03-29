from random import choice
import numpy as np

from constants import *
from tile import Tile, TileType


class Board(object):
    """
    Board class.
    """

    def __init__(self, row, column, board_setup=None):
        """
        Board class construct.

        :param row: # of rows in the board
        :param column: # of columns in the board
        :param board_setup: initial board setup to use when initialising the state of the board. Default is None.
        """
        self.board: list = []
        self.board_row: int = row
        self.board_column: int = column
        self._initialise_board(board_setup)

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        if not isinstance(value, list):
            raise TypeError(f"Incorrect variable type assigned to board: {value}")
        self._board = value

    @property
    def board_row(self):
        return self._board_row

    @board_row.setter
    def board_row(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Incorrect variable type assigned to board_row: {value}")
        if value <= 3:
            raise ValueError(f"Row must be greater than 3: {value}")
        self._board_row = value

    @property
    def board_column(self):
        return self._board_column

    @board_column.setter
    def board_column(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Incorrect variable type assigned to board_row: {value}")
        if value <= 3:
            raise ValueError(f"Row must be greater than 3: {value}")
        self._board_column = value

    def _initialise_board(self, board_setup):
        """
        Initialise the board with non-empty Tile objects

        :param board_setup: 2D-array with prescribed non-empty Tile objects i.e. tile_type is at least one. If None,
        the board will instead be randomised with non-empty Tile objects.
        :return:
        """
        if board_setup is None:
            nonempty_types = [i for i in TileType if i != TileType.EMPTY]
            for i in range(self._board_row):
                self._board.append([])
                for j in range(self._board_column):
                    tile = Tile(choice(nonempty_types))
                    self._board[i].append(tile)
        else:
            if len(board_setup) != self._board_row:
                raise ValueError(f"INITIALISATION ERROR: row dimensions do not match")
            for i in range(self._board_row):
                if self._board_column != len(board_setup[i]):
                    raise ValueError(f"INITIALISATION ERROR: column size of row {i} does not match column size "
                                     f"parameter")
                for j in range(self._board_column):
                    if not isinstance(board_setup[i][j], Tile):
                        raise TypeError(f"INITIALISATION ERROR: board position ({i}, {j}) "
                                        f"is not an instance of class Tile.")
                    if board_setup[i][j].tile_type == TileType.EMPTY:
                        raise ValueError(f"INITIALISATION ERROR: tile_type of board position ({i}, {j}) is zero. "
                                         f"Must be at least one.")
            self._board = board_setup

    def _get_tile_sprite(self, row_pos, col_pos):
        return self._board[row_pos][col_pos]

    def get_tile_type(self, row_pos, col_pos):
        """
        Get the tile_type variable of a Tile class with board position (row_pos, col_pos)
        :param row_pos: Row index of tile (NB: First row has index 0!)
        :param col_pos: Column index of tile
        :return: tile_type from Tile class at (row_pos, col_pos)
        """
        return self._board[row_pos][col_pos].tile_type

    def set_tile_type(self, row_pos, col_pos, new_tile_type):
        """
        Set the tile_type variable of a Tile class with board position (row_pos, col_pos). Load the appropriate tile
        texture afterwards.
        :param row_pos: Row index of tile (NB: First row has index 0!)
        :param col_pos: Column index of tile
        :param new_tile_type: TileType enum
        :return:
        """
        self._board[row_pos][col_pos].tile_type = new_tile_type
        self._board[row_pos][col_pos].set_tile_texture()

    def remove_tiles(self, tile_coordinates):
        """
        Remove selected tiles so that their tile type is zero.
        :param tile_coordinates: list of tile co-ordinates, each of the form (row_pos, col_pos).
        :return:
        """
        for coord in tile_coordinates:
            self.set_tile_type(coord[0], coord[1], TileType.EMPTY)

    def increment_board_tiles(self, tile_coordinates):
        """
        Increment selected tiles provided that they are non-empty. If tile type is maximum (4), reset it to one.
        :param tile_coordinates: list of tile co-ordinates, each of the form (row_pos, col_pos).
        :return:
        """
        for coord in tile_coordinates:
            if self.get_tile_type(coord[0], coord[1]) == TileType.ONE_TILE:
                self.set_tile_type(coord[0], coord[1], TileType.TWO_TILE)
                continue
            if self.get_tile_type(coord[0], coord[1]) == TileType.TWO_TILE:
                self.set_tile_type(coord[0], coord[1], TileType.THREE_TILE)
                continue
            if self.get_tile_type(coord[0], coord[1]) == TileType.THREE_TILE:
                self.set_tile_type(coord[0], coord[1], TileType.FOUR_TILE)
                continue
            if self.get_tile_type(coord[0], coord[1]) == TileType.FOUR_TILE:
                self.set_tile_type(coord[0], coord[1], TileType.ONE_TILE)
                continue

    def find_group_and_perimeter(self, row_pos, col_pos):
        """
        Given a row and column position on the board, find the group of contiguous tiles of the same type and the set
        of tiles that surround them having a different tile type. Uses breadth-first search.
        :param row_pos: row position selected
        :param col_pos: column position selected
        :return: List, List
        """
        target_type = self.get_tile_type(row_pos, col_pos)
        group = [(row_pos, col_pos)]
        perimeter = []
        queue = [(row_pos, col_pos)]

        while queue:
            node = queue.pop(0)
            adjacent_tiles = []

            # Append the top tile
            if node[0] > 0:
                adjacent_tiles.append(self._board[node[0] - 1][node[1]])
            # Append the left tile
            if node[1] > 0:
                adjacent_tiles.append(self._board[node[0]][node[1] - 1])
            # Append the right tile
            if node[1] < self._board_column - 1:
                adjacent_tiles.append(self._board[node[0]][node[1] + 1])
            # Append the bottom tile
            if node[0] < self._board_row - 1:
                adjacent_tiles.append(self._board[node[0] + 1][node[1]])

            selected_tiles = [t.coordinates for t in adjacent_tiles if t.tile_type == target_type and
                              t.coordinates not in group]
            boundary_tiles = [t.coordinates for t in adjacent_tiles if t.tile_type != target_type and
                              t.coordinates not in perimeter]
            group.extend(selected_tiles)
            perimeter.extend(boundary_tiles)
            queue.extend(selected_tiles)

        return group, perimeter

    def highlight_group(self, group, counter):
        if len(group) == 1:
            return
        for coord in group:
            if self.get_tile_type(coord[0], coord[1]) == TileType.EMPTY:
                continue
            self._get_tile_sprite(coord[0], coord[1]).color = (255,
                                                               int(255 * 0.5 * (np.sin(HIGHLIGHT_SPEED * counter) + 1)),
                                                               int(255 * 0.5 * (np.sin(HIGHLIGHT_SPEED * counter) + 1)))

    def _flush_tile(self, row_pos, col_pos):
        self._get_tile_sprite(row_pos, col_pos).color = (255, 255, 255)

    def flush_tiles(self, group):
        for coord in group:
            self._flush_tile(coord[0], coord[1])

    def flush_board(self):
        for row in range(self._board_row):
            for column in range(self._board_column):
                self._flush_tile(row, column)

    def any_legal_moves(self):
        """
        Check if there any available moves in the board. A 'move' is present on the board if there are at least two
        non-empty contiguous tiles of the same type.
        :return: Boolean
        """
        for i in range(self._board_row):
            for j in range(self._board_column):
                tile = self._board[i][j]
                # Check that the tile in question is non-empty
                if tile.tile_type == TileType.EMPTY:
                    continue
                # Check the top row
                if i == 0:
                    if j == 0:
                        moves_exist = (tile.tile_type == self._board[0][1].tile_type) \
                                      or (tile.tile_type == self._board[1][0].tile_type)
                    elif j == self._board_column - 1:
                        moves_exist = (tile.tile_type == self._board[0][j - 1].tile_type) \
                                      or (tile.tile_type == self._board[1][j].tile_type)
                    else:
                        moves_exist = (tile.tile_type == self._board[0][j - 1].tile_type) \
                                      or (tile.tile_type == self._board[0][j + 1].tile_type) \
                                      or (tile.tile_type == self._board[1][j].tile_type)
                # Check the bottom row
                elif i == self._board_row - 1:
                    if j == 0:
                        moves_exist = (tile.tile_type == self._board[i][1].tile_type) \
                                      or (tile.tile_type == self._board[i - 1][0].tile_type)
                    elif j == self._board_column - 1:
                        moves_exist = (tile.tile_type == self._board[i][j - 1].tile_type) \
                                      or (tile.tile_type == self._board[i - 1][j].tile_type)
                    else:
                        moves_exist = (tile.tile_type == self._board[i][j - 1].tile_type) \
                                      or (tile.tile_type == self._board[i][j + 1].tile_type) \
                                      or (tile.tile_type == self._board[i - 1][j].tile_type)
                # Check the rest of the rows
                else:
                    if j == 0:
                        moves_exist = (tile.tile_type == self._board[i][j + 1].tile_type) \
                                      or (tile.tile_type == self._board[i + 1][j].tile_type) \
                                      or (tile.tile_type == self._board[i - 1][j].tile_type)
                    elif j == self._board_column - 1:
                        moves_exist = (tile.tile_type == self._board[i][j - 1].tile_type) \
                                      or (tile.tile_type == self._board[i + 1][j].tile_type) \
                                      or (tile.tile_type == self._board[i - 1][j].tile_type)
                    else:
                        moves_exist = (tile.tile_type == self._board[i][j - 1].tile_type) \
                                      or (tile.tile_type == self._board[i][j + 1].tile_type) \
                                      or (tile.tile_type == self._board[i - 1][j].tile_type) \
                                      or (tile.tile_type == self._board[i + 1][j].tile_type)
                if moves_exist:
                    return True
        return False

    def __str__(self):
        """
        Print out current state of the board. Note that we have to mirror the board when we print it out to match
        the grid displayed in the game window.
        :return: string
        """
        string = ""
        for i in range(self._board_row - 1, -1, -1):
            for j in range(self._board_column):
                string += str(self._board[i][j]) + " " + str(self._board[i][j].coordinates) + "\t"
            string += "\n"
        return string


if __name__ == "__main__":
    board = Board(5, 5)
    print(board)
    print(board.any_legal_moves())
