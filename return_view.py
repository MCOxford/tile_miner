import arcade
from arcade.gui import UIManager
import menu_view
from data_handler import DataHandler
from constants import *

button_normal = arcade.load_texture('images/red_button_normal.png')
hovered_texture = arcade.load_texture('images/red_button_hover.png')
pressed_texture = arcade.load_texture('images/red_button_press.png')


class RestartButton(arcade.gui.UIImageButton):
    """
    When clicked, go back to the menu view.
    """

    restart = False

    def on_click(self):
        self.restart = True


class SubmitButton(arcade.gui.UIImageButton):
    """
    When clicked, submit player data to the leaderboard.
    """

    submit = False

    def on_click(self):
        self.submit = True


class ReturnView(arcade.View):
    """
    View after game session ends. If there is a new high score, player has the option to enter name and submit
    score. Otherwise, can either restart by going back to the menu or quitting.
    """

    def __init__(self, player_data: dict):
        """
        ReturnView construct
        :param player_data: dictionary containing data from the previous game session
        """

        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_TAUPE)
        self.ui_manager = UIManager()
        self.player_data = player_data

        # GUI elements
        self.ui_name_input_box = None
        self.submit_button = None
        self.submitted_text = ""
        self.restart_button = None
        self.quit_button = None

        self.txt_timer = 1.0
        self.submitted = False

    @property
    def new_high_score(self):
        return DataHandler.new_high_score(self._player_data['score'])

    @property
    def player_data(self):
        return self._player_data

    @player_data.setter
    def player_data(self, value):
        if not isinstance(value, dict):
            raise TypeError(f"Inappropriate data type for player_data: {value}")
        for key, entry in value.items():
            if not isinstance(entry, str):
                raise ValueError(f"Inappropriate pair found: ({key}: {entry})")
        self._player_data = value

    def on_draw(self):
        """ Draw this view """

        arcade.start_render()
        arcade.draw_text("GAME OVER", WIDTH / 2, HEIGHT * 3 / 4,
                         arcade.color.BLACK, font_size=75, anchor_x="center")
        if self.new_high_score or self.submitted:
            arcade.draw_text(f"NEW HIGH SCORE: {self.player_data['score']}", WIDTH / 2, HEIGHT * 3/4 - 50,
                             arcade.color.BLACK, font_size=30, anchor_x="center")
            arcade.draw_text("Enter name: ", WIDTH * 2.5 / 10, HEIGHT * 5 / 10,
                             arcade.color.BLACK, font_size=30, anchor_x="center", anchor_y="center")
            arcade.draw_text(self.submitted_text, WIDTH * 5 / 10, HEIGHT * 3 / 10,
                             arcade.color.BLACK, font_size=30, anchor_x="center", anchor_y="center")

    def setup(self):
        """
        Setup GUI elements.
        :return:
        """

        self.ui_manager.purge_ui_elements()

        if self.new_high_score or self.submitted:
            # name input box
            self.ui_name_input_box = arcade.gui.UIInputBox(center_x=WIDTH * 6.5 / 10, center_y=HEIGHT * 5 / 10,
                                                           width=400)
            self.ui_name_input_box.text = str('De Facto')
            self.ui_name_input_box.cursor_index = len(self.ui_name_input_box.text)
            self.ui_manager.add_ui_element(self.ui_name_input_box)

            # submit button
            self.submit_button = SubmitButton(center_x=WIDTH * 5 / 10, center_y=HEIGHT * 4 / 10,
                                              normal_texture=button_normal, hover_texture=hovered_texture,
                                              press_texture=pressed_texture, text='Submit')
            self.ui_manager.add_ui_element(self.submit_button)

        # play button - press to play the game (creates a new view)
        self.restart_button = RestartButton(center_x=WIDTH * 2 / 10, center_y=HEIGHT * 1 / 10,
                                            normal_texture=button_normal, hover_texture=hovered_texture,
                                            press_texture=pressed_texture, text='Restart')
        self.ui_manager.add_ui_element(self.restart_button)

        # quit button - close the game
        self.quit_button = menu_view.QuitButton(center_x=WIDTH * 8 / 10, center_y=HEIGHT * 1 / 10,
                                                normal_texture=button_normal, hover_texture=hovered_texture,
                                                press_texture=pressed_texture, text='Quit')
        self.ui_manager.add_ui_element(self.quit_button)

    def on_show_view(self):
        """
        What to do when showing this view.
        :return:
        """

        self.setup()

    def on_hide_view(self):
        """
        What to do when hiding this view
        :return:
        """

        self.ui_manager.unregister_handlers()

    def update(self, delta_time: float):
        """
        Update procedure per frame
        :param delta_time:
        :return:
        """

        if self.restart_button.restart:
            next_view = menu_view.MainMenu()
            self.window.show_view(next_view)
        if self.submit_button is not None and self.submit_button.submit and not self.submitted:
            self._player_data['name'] = self.ui_name_input_box.text
            DataHandler.add_new_player_data(**self._player_data)
            self.submitted_text = "Submitted!"
            self.submit_button.color = arcade.color.GRAY
            self.submit_button.hover_texture = self.submit_button.normal_texture
            self.submit_button.press_texture = self.submit_button.normal_texture
            self.submitted = True
        if self.submitted_text != "":
            self.txt_timer -= delta_time
            if self.txt_timer < 0:
                self.submitted_text = ""
                self.txt_timer = 1.0


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Tile Miner")
    return_view = ReturnView({'name': "",
                              'date_year': '2008', 'date_month': '05', 'date_day': '22',
                              'row': '4', 'column': '3',
                              'time_minutes': '4', 'time_seconds': '00',
                              'score': '29000'
                              })
    window.show_view(return_view)
    arcade.run()


if __name__ == "__main__":
    main()
