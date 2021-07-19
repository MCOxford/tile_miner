import arcade
import arcade.gui
from arcade.gui import UIManager
from constants import *
from tile_miner import TileMiner

# TODO: Button for ranking table?
# TODO: Display messages when input is invalid instead of raising exceptions
# TODO: animated background? (idea: falling tiles at different speeds/rotations
# TODO: Take input from minute/second input GUIs when starting the game


class PlayButton(arcade.gui.UIImageButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    start_game = False

    def on_click(self):
        """ Called when user lets off button """
        self.start_game = True


class QuitButton(arcade.gui.UIImageButton):
    """
    Quit button class - creates a button to close down game
    """

    def on_click(self):
        arcade.close_window()


class MainMenu(arcade.View):
    """
    Class for main menu screen (the first view the player sees when booting up the game).
    """

    # minimum/maximum dimensions for tile board (width and height)
    MIN = 4
    MAX = 15

    def __init__(self, row_count=5, column_count=5):
        """
        MainMenu construct.
        """

        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_TAUPE)
        self.ui_manager = UIManager()
        self.row_count = row_count
        self.column_count = column_count
        self.minutes = 1
        self.seconds = 0
        self._timer = 60 * self.minutes + self.seconds

        # GUI elements which will get constructed in setup()
        self.ui_row_input_box = None
        self.ui_column_input_box = None
        self.ui_minute_input_box = None
        self.ui_second_input_box = None
        self.play_button = None

    @property
    def row_count(self):
        return self._row_count

    @row_count.setter
    def row_count(self, value):
        if not isinstance(value, int):
            raise TypeError(f"row value not an integer: {value}")
        if value < self.MIN or value > self.MAX:
            raise ValueError(f"row value not within bounds: {value}")
        self._row_count = value

    @property
    def column_count(self):
        return self._column_count

    @column_count.setter
    def column_count(self, value):
        if not isinstance(value, int):
            raise TypeError(f"column value not an integer: {value}")
        if value < self.MIN or value > self.MAX:
            raise ValueError(f"column value not within bounds: {value}")
        self._column_count = value

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        if not isinstance(value, int):
            raise TypeError(f"value not an integer type: {value}")
        if value < 0:
            raise ValueError(f"value must be greater than -1: {value}")
        self._minutes = value

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value):
        if not isinstance(value, int):
            raise TypeError(f"value not an integer type: {value}")
        if value < 0 or value > 59:
            raise ValueError(f"value must be between 0 and 59: {value}")
        self._seconds = value

    def setup(self):
        """
        Sets up menu screen with GUI elements
        :return:
        """

        self.ui_manager.purge_ui_elements()

        # board row size input box
        self.ui_row_input_box = arcade.gui.UIInputBox(center_x=WIDTH * 4 / 10 + 175, center_y=HEIGHT * 6 / 10,
                                                      width=300)
        self.ui_row_input_box.text = str(self._row_count)
        self.ui_row_input_box.cursor_index = len(self.ui_row_input_box.text)
        self.ui_manager.add_ui_element(self.ui_row_input_box)

        # board column size input box
        self.ui_column_input_box = arcade.gui.UIInputBox(center_x=WIDTH * 3 / 10 + 255, center_y=HEIGHT * 4.5 / 10,
                                                         width=300)
        self.ui_column_input_box.text = str(self._column_count)
        self.ui_column_input_box.cursor_index = len(self.ui_column_input_box.text)
        self.ui_manager.add_ui_element(self.ui_column_input_box)

        # minute input box
        self.ui_minute_input_box = arcade.gui.UIInputBox(center_x=WIDTH * 4.94 / 10, center_y=HEIGHT * 3 / 10,
                                                         width=100)
        self.ui_minute_input_box.text = str(self._minutes)
        self.ui_minute_input_box.cursor_index = len(self.ui_minute_input_box.text)
        self.ui_manager.add_ui_element(self.ui_minute_input_box)

        # second input box
        self.ui_second_input_box = arcade.gui.UIInputBox(center_x=WIDTH * 6.9 / 10, center_y=HEIGHT * 3 / 10,
                                                         width=100)
        self.ui_second_input_box.text = str(self._seconds)
        self.ui_second_input_box.cursor_index = len(self.ui_second_input_box.text)
        self.ui_manager.add_ui_element(self.ui_second_input_box)

        # play button - press to play the game (creates a new view)
        button_normal = arcade.load_texture('images/red_button_normal.png')
        hovered_texture = arcade.load_texture('images/red_button_hover.png')
        pressed_texture = arcade.load_texture('images/red_button_press.png')
        self.play_button = PlayButton(center_x=WIDTH / 2, center_y=HEIGHT * 1.5 / 10, normal_texture=button_normal,
                                      hover_texture=hovered_texture, press_texture=pressed_texture, text='Play!')
        self.ui_manager.add_ui_element(self.play_button)

        # quit button - close the game
        quit_button = QuitButton(center_x=WIDTH * 8 / 10, center_y=HEIGHT * 1 / 10, normal_texture=button_normal,
                                 hover_texture=hovered_texture, press_texture=pressed_texture, text='Quit')
        self.ui_manager.add_ui_element(quit_button)

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()
        arcade.draw_text("TILE MINER", WIDTH / 2, HEIGHT * 3/4,
                         arcade.color.BLACK, font_size=75, anchor_x="center")
        arcade.draw_text("Row size: ", WIDTH * 3 / 10, HEIGHT * 6 / 10,
                         arcade.color.BLACK, font_size=30, anchor_x="center", anchor_y="center")
        arcade.draw_text("Column size: ", WIDTH * 3 / 10 - 24, HEIGHT * 4.5 / 10,
                         arcade.color.BLACK, font_size=30, anchor_x="center", anchor_y="center")
        arcade.draw_text("Timer: ", WIDTH * 3.29 / 10, HEIGHT * 3 / 10,
                         arcade.color.BLACK, font_size=30, anchor_x="center", anchor_y="center")
        arcade.draw_text("min", WIDTH * 5.9 / 10, HEIGHT * 3 / 10,
                         arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
        arcade.draw_text("sec", WIDTH * 7.85 / 10, HEIGHT * 3 / 10,
                         arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

    def on_show_view(self):
        """
        Show this view
        """

        self.setup()

    def on_hide_view(self):
        """
        What to do when hiding this view
        :return:
        """
        self.ui_manager.unregister_handlers()

    def update(self, delta_time: float):
        if self.play_button.start_game:
            self.row_count = int(self.ui_row_input_box.text)
            self.column_count = int(self.ui_column_input_box.text)
            game_view = TileMiner(row_count=self._row_count, column_count=self._column_count)
            self.window.width = game_view.screen_width
            self.window.height = game_view.screen_height
            self.window.show_view(game_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Tile Miner")
    menu_view = MainMenu(4, 4)
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
