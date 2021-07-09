import arcade
import random
import time
from tile import Tile, TileType
from board import Board
from dashboard import Dashboard
from constants import *
import logging

# Logger (for debugging)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Set random seed (for debugging)
random.seed(0)

# Set how many rows and columns we will have
ROW_COUNT = 4
COLUMN_COUNT = 4

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (TILE_SCALED_WIDTH + MARGIN) * COLUMN_COUNT + 2 * VERTICAL_BORDER_MARGIN
SCREEN_HEIGHT = (TILE_SCALED_HEIGHT + MARGIN) * ROW_COUNT + HORIZONTAL_BORDER_MARGIN


class TileMiner(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, screen_width, screen_height):
        """
        TileMiner construct.
        :param screen_width: screen width of window
        :param screen_height: screen height of window
        """

        super().__init__(screen_width, screen_height, "Tile miner")

        arcade.set_background_color(arcade.color.LIGHT_TAUPE)

        # Create (1D) list of all sprites
        self.grid_sprite_list = arcade.SpriteList()

        # 2D grid of sprites to that points to the same sprites that are
        # in grid_sprite_list. Improves runtime of the code.
        board_template = []

        # List of non-empty tile types
        nonempty_types = [i for i in TileType if i != TileType.EMPTY]

        # Set up the initial board of tiles randomly. Make sure we have legal moves
        # to begin with
        while True:
            for row in range(ROW_COUNT):
                board_template.append([])
                for column in range(COLUMN_COUNT):
                    x = column * (TILE_SCALED_WIDTH + MARGIN) + (
                                TILE_SCALED_WIDTH / 2 + MARGIN / 2) + VERTICAL_BORDER_MARGIN
                    y = row * (TILE_SCALED_HEIGHT + MARGIN) + (TILE_SCALED_HEIGHT / 2 + MARGIN / 2)
                    initial_tile_type = random.choice(nonempty_types)
                    sprite = Tile(initial_tile_type)
                    sprite.center_x = x
                    sprite.center_y = y
                    sprite.coordinates = (int(y // (TILE_SCALED_HEIGHT + MARGIN)),
                                          int((x - VERTICAL_BORDER_MARGIN) // (TILE_SCALED_WIDTH + MARGIN)))
                    sprite.scale = SCALE_FACTOR
                    self.grid_sprite_list.append(sprite)
                    board_template[row].append(sprite)
            self._board = Board(ROW_COUNT, COLUMN_COUNT, board_template)
            if self._board.any_legal_moves():
                logging.info("Board now set up")
                break

        # Information to draw the rectangle which we'll use as our dash board to display the time left, score and
        # game messages
        self.dashboard_data = {
            'center_x': SCREEN_WIDTH / 2,
            'center_y': (ROW_COUNT + 1) * (TILE_SCALED_HEIGHT + MARGIN) + 2 * MARGIN,
            'width': SCREEN_WIDTH - 2 * MARGIN,
            'height': HORIZONTAL_BORDER_MARGIN - 2 * MARGIN,
        }
        self.dashboard = Dashboard(self.dashboard_data)

        self.no_moves = False

        self._highlighted_group = []

        self._timer = 0
        self._highlight_target_changed = False

        logging.info("Initial board setup:\n" + str(self._board))

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()
        self.dashboard.setup_dashboard()
        self.grid_sprite_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called when the user moves the mouse.
        """

        # Change the x/y screen coordinates to grid coordinates
        column = int((x - VERTICAL_BORDER_MARGIN) // (TILE_SCALED_WIDTH + MARGIN))
        row = int(y // (TILE_SCALED_HEIGHT + MARGIN))

        # Highlight a group of tiles of the same type (single tiles will never be highlighted)
        if row < 0 or row >= ROW_COUNT or column < 0 or column >= COLUMN_COUNT \
                or self._board.get_tile_type(row, column) == TileType.EMPTY:
            return
        group, perimeter = self._board.find_group_and_perimeter(row, column)
        sorted_group = sorted(group)
        if self._highlighted_group != sorted_group:
            self._highlighted_group = sorted_group
            self._board.flush_board()
            self._timer = 0
            self._highlight_target_changed = True
        else:
            self._highlight_target_changed = False

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change the x/y screen coordinates to grid coordinates
        column = int((x - VERTICAL_BORDER_MARGIN) // (TILE_SCALED_WIDTH + MARGIN))
        row = int(y // (TILE_SCALED_HEIGHT + MARGIN))

        logging.info(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # If selected tile is part of a group of same-type tiles, remove and increment surrounding tiles by one (or
        # reset to one if tile has type four)
        if row < 0 or row >= ROW_COUNT or column < 0 or column >= COLUMN_COUNT \
                or self._board.get_tile_type(row, column) == TileType.EMPTY:
            return
        group, perimeter = self._board.find_group_and_perimeter(row, column)
        if len(group) > 1:
            self._board.remove_tiles(group)
            self._board.flush_tiles(group)
            self._board.increment_board_tiles(perimeter)
            self.dashboard.calculate_new_score(group)
        else:
            self.dashboard.message = "Only one tile!"
        check = self._board.any_legal_moves()
        if not check:
            self.dashboard.message = "NO MORE MOVES!"
            self.no_moves = True

    def on_update(self, new_time):
        """
        Called every frame
        :param new_time: delta time
        :return:
        """
        self.dashboard.timer -= new_time
        self._timer += new_time

        if self.dashboard.message != "" and self.dashboard.message != "NO MORE MOVES!":
            self.dashboard.msg_timer -= new_time
            if self.dashboard.msg_timer <= 0:
                self.dashboard.reset_message()
                self.dashboard.reset_msg_timer()

        if not self._highlight_target_changed:
            self._board.highlight_group(self._highlighted_group, self._timer)

        if self.dashboard.timer < 0 or self.no_moves:
            time.sleep(2)
            self.close()


def main():
    """
    Main method to run game from
    :return:
    """
    TileMiner(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
