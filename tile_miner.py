import arcade
import random
from tile import Tile
from board import Board
from constants import *

# Random seed (for debugging)
random.seed(0)

# Set how many rows and columns we will have
ROW_COUNT = 4
COLUMN_COUNT = 4

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (TILE_SCALED_WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (TILE_SCALED_HEIGHT + MARGIN) * ROW_COUNT + MARGIN


class TileMiner(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, "Tile miner")

        arcade.set_background_color(arcade.color.BLACK)

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list = arcade.SpriteList()

        # This will be a two-dimensional grid of sprites to mirror the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in grid_sprite_list, just in a 2d manner.
        board_template = []

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            board_template.append([])
            for column in range(COLUMN_COUNT):
                x = column * (TILE_SCALED_WIDTH + MARGIN) + (TILE_SCALED_WIDTH / 2 + MARGIN)
                y = row * (TILE_SCALED_HEIGHT + MARGIN) + (TILE_SCALED_HEIGHT / 2 + MARGIN)
                initial_tile_type = random.randint(1, 4)
                sprite = Tile(initial_tile_type)
                sprite.center_x = x
                sprite.center_y = y
                sprite.coordinates = (int(y // (TILE_SCALED_HEIGHT + MARGIN)), int(x // (TILE_SCALED_WIDTH + MARGIN)))
                print(sprite.coordinates)
                sprite.scale = SCALE_FACTOR
                self.grid_sprite_list.append(sprite)
                board_template[row].append(sprite)

        self.board = Board(ROW_COUNT, COLUMN_COUNT, board_template)
        print(self.board)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        self.grid_sprite_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (TILE_SCALED_WIDTH + MARGIN))
        row = int(y // (TILE_SCALED_HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        if row >= ROW_COUNT or column >= COLUMN_COUNT or self.board.get_board_tile(row, column) == 0:
            return
        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        group, perimeter = self.board.find_group_and_perimeter(row, column)
        print("group: ", group)
        print("perimeter: ", perimeter)
        if len(group) > 1:
            self.board.remove_tiles(group)
            self.board.increment_board_tiles(perimeter)
        else:
            print("only one tile!")
        check = self.board.any_legal_moves()
        if not check:
            print("NO MORE MOVES!")


def main():
    TileMiner(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
