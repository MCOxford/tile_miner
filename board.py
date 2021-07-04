from random import choice

import arcade.color

from constants import TYPES
from tile import Tile


class Board(object):
    """
    Board class.
    """

    def __init__(self, row, column, board_setup=None):
        """
        Board class construct.

        :param row: # of rows in the board
        :param column: # of columns in the board
        :param board_setup: # initial board setup to use when initialising the state of the board. Default is None.
        """
        self._board = []
        self._board_row = row
        self._board_column = column
        self.initialise_board(board_setup)

    @property
    def board(self):
        return self._board

    @property
    def board_row(self):
        return self._board_row

    @property
    def board_column(self):
        return self._board_column

    def initialise_board(self, board_setup):
        """
        Initialise the board with non-empty Tile objects

        :param board_setup: 2D-array with prescribed non-empty Tile objects i.e. tile_type is at least one. If None,
        the board will instead be randomised with non-empty Tile objects.
        :return:
        """
        if board_setup is None:
            nonempty_types = list(TYPES.keys())[1::]
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
                    if board_setup[i][j].tile_type == 0:
                        raise ValueError(f"INITIALISATION ERROR: tile_type of board position ({i}, {j}) is zero. "
                                         f"Must be at least one.")
            self._board = board_setup

    def get_board_tile(self, row_pos, col_pos):
        """
        Get the tile_type variable of a Tile class with board position (row_pos, col_pos)
        :param row_pos: Row index of tile (NB: First row has index 0!)
        :param col_pos: Column index of tile
        :return: tile_type from Tile class at (row_pos, col_pos)
        """
        return self._board[row_pos][col_pos].tile_type

    def set_board_tile(self, row_pos, col_pos, new_tile_type):
        """
        Set the tile_type variable of a Tile class with board position (row_pos, col_pos)
        :param row_pos: Row index of tile (NB: First row has index 0!)
        :param col_pos: Column index of tile
        :param new_tile_type: new value of tile_type variable. Exactly one from the list [0,1,2,3,4]
        :return:
        """
        self._board[row_pos][col_pos].tile_type = new_tile_type

    def remove_tiles(self, tile_coordinates):
        """
        Remove selected tiles so that their tile type is zero.
        :param tile_coordinates: list of tile co-ordinates, each of the form (row_pos, col_pos).
        :return:
        """
        for coord in tile_coordinates:
            self.set_board_tile(coord[0], coord[1], 0)

    def increment_board_tiles(self, tile_coordinates):
        """
        Increment selected tiles provided that they are non-empty. If tile type is maximum (4), reset it to one.
        :param tile_coordinates: list of tile co-ordinates, each of the form (row_pos, col_pos).
        :return:
        """
        for coord in tile_coordinates:
            if self.get_board_tile(coord[0], coord[1]) != 0:
                new_tile_type = self.get_board_tile(coord[0], coord[1]) + 1
                if new_tile_type > 4:
                    new_tile_type = 1
                self.set_board_tile(coord[0], coord[1], new_tile_type)

    def find_group_and_perimeter(self, row_pos, col_pos):
        """
        Given a row and column position on the board, find the group of contiguous tiles of the same type and the set
        of tiles that surround them having a different tile type. Uses breadth-first search.
        :param row_pos: row position selected
        :param col_pos: column position selected
        :return: tile_list, perimeter
        """
        target_type = self._board[row_pos][col_pos].tile_type
        tile_list = [(row_pos, col_pos)]
        perimeter = []
        queue = [(row_pos, col_pos)]

        while queue:
            node = queue.pop(0)
            adjacent_tiles = []

            # Append the top tile
            if node[0] > 0:
                adjacent_tiles.append(self._board[node[0]-1][node[1]])
            # Append the left tile
            if node[1] > 0:
                adjacent_tiles.append(self._board[node[0]][node[1]-1])
            # Append the right tile
            if node[1] < self._board_column - 1:
                adjacent_tiles.append(self._board[node[0]][node[1]+1])
            # Append the bottom tile
            if node[0] < self._board_row - 1:
                adjacent_tiles.append(self._board[node[0]+1][node[1]])

            selected_tiles = [t.coordinates for t in adjacent_tiles if t.tile_type == target_type and
                              t.coordinates not in tile_list]
            boundary_tiles = [t.coordinates for t in adjacent_tiles if t.tile_type != target_type and
                              t.coordinates not in perimeter]
            tile_list.extend(selected_tiles)
            perimeter.extend(boundary_tiles)
            queue.extend(selected_tiles)

        return tile_list, perimeter

    def any_legal_moves(self):
        """
        Check if there any available moves in the board. A 'move' is present on the board if there are at least two
        non-empty contiguous tiles of the same type.
        :return:
        """
        for i in range(self._board_row):
            for j in range(self._board_column):
                tile = self._board[i][j]
                # Check that the tile in question is non-empty
                if tile.tile_type == 0:
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
        :return:
        """
        string = ""
        for i in range(self._board_row-1, -1, -1):
            for j in range(self._board_column):
                string += str(self._board[i][j]) + "\t"
            string += "\n"
        return string


if __name__ == "__main__":
    board = Board(5, 5)
    print(board)
    print(board.any_legal_moves())

    board_template = [[Tile(1), Tile(2), Tile(3)],
                      [Tile(2), Tile(1), Tile(2)],
                      [Tile(1), Tile(2), Tile(1)]]
    board2 = Board(3, 3, board_template)
    print(board2)
    print(board2.any_legal_moves())
