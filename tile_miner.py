import arcade
import random
import time
from tile import Tile, TileType
from board import Board
from dashboard import Dashboard
from constants import *
# import logging
import return_view
import datetime

# Logger (for debugging)
# logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Set random seed (for debugging)
# random.seed(0)

# Set how many rows and columns we will have
ROW_COUNT = 4
COLUMN_COUNT = 4


class TileMiner(arcade.View):
    """
    Main application class.
    """

    def __init__(self, row_count=ROW_COUNT, column_count=COLUMN_COUNT, total_time=60):
        """
        TileMiner construct.
        """

        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_TAUPE)

        self.row_count = row_count
        self.column_count = column_count
        self._total_time = total_time

        # window dimensions
        self.screen_width = (TILE_SCALED_WIDTH + MARGIN) * self.column_count + 2 * VERTICAL_BORDER_MARGIN
        self.screen_height = (TILE_SCALED_HEIGHT + MARGIN) * self.row_count + HORIZONTAL_BORDER_MARGIN

        # Create (1D) list of all sprites
        self.grid_sprite_list = arcade.SpriteList()

        # 2D grid of sprites to that points to the same sprites that are in grid_sprite_list. Improves runtime of the
        # code.
        board_template = []

        # List of non-empty tile types
        nonempty_types = [i for i in TileType if i != TileType.EMPTY]

        # Set up the initial board of tiles randomly. Make sure we have legal moves to begin with.
        while True:
            for row in range(self.row_count):
                board_template.append([])
                for column in range(self.column_count):
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
            self._board = Board(self.row_count, self.column_count, board_template)
            if self._board.any_legal_moves():
                # logging.info("Board now set up")
                break

        # Information to draw the rectangle which we'll use as our dashboard to display the time left, score and
        # game messages
        self.dashboard_data = {
            'center_x': self.screen_width / 2,
            'center_y': (self.row_count + 1) * (TILE_SCALED_HEIGHT + MARGIN) + 2 * MARGIN,
            'width': self.screen_width - 2 * MARGIN,
            'height': HORIZONTAL_BORDER_MARGIN - 2 * MARGIN,
        }
        self.dashboard = Dashboard(self.dashboard_data, timer=total_time)

        # Evaluates to True if no available moves can be found (i.e. the game ends)
        self.no_moves = False

        # Group of same-type tiles to be highlighted when the cursor hovers over them
        self._highlighted_group = []

        # Has _highlighted_group changed?
        self._highlight_target_changed = False

        # dashboard message timer. Message pops up for a given amount of time for certain events.
        self._timer = 0

        # Has the game already started?
        self.game_started = True

        # logging.info("Initial board setup:\n" + str(self._board))

    @property
    def player_data(self):
        """
        Encapsulate player data for this game session.
        :return:
        """
        current_date = datetime.datetime.today()
        return {'name': "",
                'date_year': str(current_date.year),
                'date_month':  str(current_date.month),
                'date_day':  str(current_date.day),
                'row': str(self.row_count), 'column': str(self.column_count),
                'time_minutes': str(int(self._total_time / 60)),
                'time_seconds': str(int(self._total_time % 60)).zfill(2),
                'score': str(self.dashboard.score)
                }

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
        if row < 0 or row >= self.row_count or column < 0 or column >= self.column_count \
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

        # logging.info(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # If selected tile is part of a group of same-type tiles, remove and increment surrounding tiles by one (or
        # reset to one if tile has type four)
        if row < 0 or row >= self.row_count or column < 0 or column >= self.column_count \
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
        any_more_moves = self._board.any_legal_moves()
        if not any_more_moves:
            self.dashboard.message = "NO MORE MOVES!"
            self.no_moves = True

    def on_update(self, new_time):
        """
        Called every frame.
        :param new_time: delta time for each frame.
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
            time.sleep(1.5)
            next_view = return_view.ReturnView(self.player_data)
            self.window.width = WIDTH
            self.window.height = HEIGHT
            self.window.show_view(next_view)


def main():
    """
    Main method to run game from.
    :return:
    """
    screen_width = (TILE_SCALED_WIDTH + MARGIN) * COLUMN_COUNT + 2 * VERTICAL_BORDER_MARGIN
    screen_height = (TILE_SCALED_HEIGHT + MARGIN) * ROW_COUNT + HORIZONTAL_BORDER_MARGIN

    window = arcade.Window(screen_width, screen_height, "Tile Miner")
    tile_miner = TileMiner()
    window.show_view(tile_miner)
    arcade.run()


if __name__ == "__main__":
    main()
