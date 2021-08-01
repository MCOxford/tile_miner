import arcade
import arcade.gui
from arcade.gui import UIManager
from constants import *

import os
dirname = os.path.dirname(__file__)
button_normal = arcade.load_texture(os.path.join(dirname, 'images/red_button_normal.png'))
hovered_texture = arcade.load_texture(os.path.join(dirname, 'images/red_button_hover.png'))
pressed_texture = arcade.load_texture(os.path.join(dirname, 'images/red_button_press.png'))


class BoundaryError(Exception):
    pass


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
    Quit button class - creates a button to close down game.
    """

    def on_click(self):
        arcade.close_window()


class LeaderboardButton(arcade.gui.UIImageButton):
    """
    Leaderboard button class - click the button to go to the leaderboard.
    """

    go_to_leaderboard = False

    def on_click(self):
        self.go_to_leaderboard = True


class MainMenu(arcade.View):
    """
    Class for main menu screen (the first view the player sees when booting up the game).
    """

    # minimum/maximum dimensions for tile board (width and height)
    MIN = 4
    MAX = 20

    def __init__(self, row_count=5, column_count=5, minutes=1, seconds=0):
        """
        MainMenu construct.
        """

        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_TAUPE)
        self.ui_manager = UIManager()
        self.row_count = row_count
        self.column_count = column_count
        self.minutes = minutes
        self.seconds = seconds

        # GUI elements which will get constructed in setup()
        self.ui_row_input_box = None
        self.ui_column_input_box = None
        self.ui_minute_input_box = None
        self.ui_second_input_box = None
        self.play_button = None
        self.leaderboard_button = None

    @property
    def timer(self):
        return 60 * self._minutes + self._seconds

    @property
    def row_count(self):
        return self._row_count

    @row_count.setter
    def row_count(self, value):
        if not isinstance(value, int):
            raise TypeError(f"row value not an integer: {value}")
        if value < self.MIN or value > self.MAX:
            raise BoundaryError
        self._row_count = value

    @property
    def column_count(self):
        return self._column_count

    @column_count.setter
    def column_count(self, value):
        if not isinstance(value, int):
            raise TypeError(f"column value not an integer: {value}")
        if value < self.MIN or value > self.MAX:
            raise BoundaryError
        self._column_count = value

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        if not isinstance(value, int):
            raise TypeError(f"value not an integer type: {value}")
        if value < 0 or value > 99:
            raise BoundaryError(f"value must be between 0 and 99: {value}")
        self._minutes = value

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value):
        if not isinstance(value, int):
            raise TypeError(f"value not an integer type: {value}")
        if value < 0 or value > 59:
            raise BoundaryError(f"value must be between 0 and 59: {value}")
        self._seconds = value

    def setup(self):
        """
        Sets up menu screen with GUI elements.
        :return:
        """

        self.ui_manager.purge_ui_elements()

        # board row size input box
        self.ui_row_input_box = arcade.gui.UIInputBox(center_x=WIDTH * 6.5 / 10, center_y=HEIGHT * 6 / 10,
                                                      width=350)
        self.ui_row_input_box.text = str(self._row_count)
        self.ui_row_input_box.cursor_index = len(self.ui_row_input_box.text)
        self.ui_manager.add_ui_element(self.ui_row_input_box)

        # board column size input box
        self.ui_column_input_box = arcade.gui.UIInputBox(center_x=WIDTH * 6.5 / 10, center_y=HEIGHT * 4.5 / 10,
                                                         width=350)
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
        self.play_button = PlayButton(center_x=WIDTH / 2, center_y=HEIGHT * 1.5 / 10, normal_texture=button_normal,
                                      hover_texture=hovered_texture, press_texture=pressed_texture, text='Play!')
        self.ui_manager.add_ui_element(self.play_button)

        # quit button - close the game
        quit_button = QuitButton(center_x=WIDTH * 8 / 10, center_y=HEIGHT * 1 / 10, normal_texture=button_normal,
                                 hover_texture=hovered_texture, press_texture=pressed_texture, text='Quit')
        self.ui_manager.add_ui_element(quit_button)

        # leaderboard button - press to go to the leaderboard view
        self.leaderboard_button = LeaderboardButton(center_x=WIDTH * 2 / 10, center_y=HEIGHT * 1 / 10,
                                                    normal_texture=button_normal, hover_texture=hovered_texture,
                                                    press_texture=pressed_texture, text='Leaderboard')
        self.ui_manager.add_ui_element(self.leaderboard_button)

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()
        arcade.draw_text("TILE MINER", WIDTH / 2, HEIGHT * 3/4,
                         arcade.color.BLACK, font_size=75, anchor_x="center")

        arcade.draw_text("Row size: ", WIDTH * 3 / 10, HEIGHT * 6 / 10,
                         arcade.color.BLACK, font_size=30, anchor_x="center", anchor_y="center")
        arcade.draw_text("(Whole number between 4 and 20)", WIDTH * 6.5 / 10, HEIGHT * 5.4 / 10,
                         arcade.color.BLACK, font_size=15, anchor_x="center", anchor_y="center")

        arcade.draw_text("Column size: ", WIDTH * 3 / 10 - 24, HEIGHT * 4.5 / 10,
                         arcade.color.BLACK, font_size=30, anchor_x="center", anchor_y="center")
        arcade.draw_text("(Whole number between 4 and 20)", WIDTH * 6.5 / 10, HEIGHT * 3.9 / 10,
                         arcade.color.BLACK, font_size=15, anchor_x="center", anchor_y="center")

        arcade.draw_text("Timer: ", WIDTH * 3.29 / 10, HEIGHT * 3 / 10,
                         arcade.color.BLACK, font_size=30, anchor_x="center", anchor_y="center")

        arcade.draw_text("min", WIDTH * 5.9 / 10, HEIGHT * 3 / 10,
                         arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
        arcade.draw_text("(0-99)", WIDTH * 4.93 / 10, HEIGHT * 2.4 / 10,
                         arcade.color.BLACK, font_size=15, anchor_x="center", anchor_y="center")

        arcade.draw_text("sec", WIDTH * 7.85 / 10, HEIGHT * 3 / 10,
                         arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
        arcade.draw_text("(0-59)", WIDTH * 6.9 / 10, HEIGHT * 2.4 / 10,
                         arcade.color.BLACK, font_size=15, anchor_x="center", anchor_y="center")

    def on_show_view(self):
        """
        Show this view.
        """

        self.setup()

    def on_hide_view(self):
        """
        What to do when hiding this view.
        :return:
        """

        self.ui_manager.unregister_handlers()

    def update(self, delta_time: float):
        """
        Called every frame.
        :param delta_time: delta time for each frame.
        :return:
        """

        if self.play_button.start_game:
            try:
                self.row_count = int(self.ui_row_input_box.text)
                self.column_count = int(self.ui_column_input_box.text)
                self.minutes = int(self.ui_minute_input_box.text)
                self.seconds = int(self.ui_second_input_box.text)
            except (ValueError, BoundaryError):
                self.ui_row_input_box.text = ""
                self.ui_column_input_box.text = ""
                self.ui_minute_input_box.text = ""
                self.ui_second_input_box.text = ""
                self.play_button.start_game = False
                return
            import tile_miner
            game_view = tile_miner.TileMiner(row_count=self._row_count, column_count=self._column_count,
                                             total_time=self.timer)
            self.window.width = game_view.screen_width
            self.window.height = game_view.screen_height
            self.window.show_view(game_view)

        if self.leaderboard_button.go_to_leaderboard:
            import leaderboard_view
            lb_view = leaderboard_view.LeaderboardView()
            self.window.show_view(lb_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Tile Miner")
    menu_view = MainMenu(6, 6, 3, 0)
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
