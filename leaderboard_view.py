import arcade
import arcade.gui
import menu_view
from data_handler import DataHandler
from arcade.gui import UIManager
from constants import *


class BackButton(arcade.gui.UIImageButton):
    """
    When clicked, go back to the menu view.
    """

    go_back = False

    def on_click(self):
        self.go_back = True


class LeaderboardView(arcade.View):

    def __init__(self):
        """
        LeaderboardView construct.
        """

        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_TAUPE)
        self.ui_manager = UIManager()

        # GUI elements which will get constructed in setup()
        self.back_button = None

    def setup(self):
        self.ui_manager.purge_ui_elements()

        # back button - press to play the game (creates a new view)
        button_normal = arcade.load_texture('images/red_button_normal.png')
        hovered_texture = arcade.load_texture('images/red_button_hover.png')
        pressed_texture = arcade.load_texture('images/red_button_press.png')
        self.back_button = BackButton(center_x=WIDTH / 2, center_y=HEIGHT * 1.5 / 10, normal_texture=button_normal,
                                      hover_texture=hovered_texture, press_texture=pressed_texture, text='Back')
        self.ui_manager.add_ui_element(self.back_button)

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()
        arcade.draw_text("LEADERBOARD", WIDTH / 2, HEIGHT * 3/4,
                         arcade.color.BLACK, font_size=75, anchor_x="center")

        arcade.draw_text("Name", WIDTH / 6, HEIGHT * 3 / 4 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Date", WIDTH * 2/6, HEIGHT * 3 / 4 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Dimensions", WIDTH * 3.1/6, HEIGHT * 3 / 4 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Time", WIDTH * 4.1/6, HEIGHT * 3 / 4 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Score", WIDTH * 5/6, HEIGHT * 3 / 4 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

        # Display player data
        leaderboard_data = DataHandler.get_leaderboard_data()
        for i in range(len(leaderboard_data)):
            rank = str(i+1)
            name = leaderboard_data[rank]['name']
            name = name[:6] + '...' if len(name) > 6 else name
            arcade.draw_text(name, WIDTH / 6, HEIGHT * 3 / 4 - 50*(i+2),
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text(leaderboard_data[rank]['date'], WIDTH * 2 / 6, HEIGHT * 3 / 4 - 50*(i+2),
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text(leaderboard_data[rank]['dimensions'], WIDTH * 3.1 / 6, HEIGHT * 3 / 4 - 50*(i+2),
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text(leaderboard_data[rank]['time'], WIDTH * 4.1 / 6, HEIGHT * 3 / 4 - 50*(i+2),
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text(leaderboard_data[rank]['score'], WIDTH * 5 / 6, HEIGHT * 3 / 4 - 50*(i+2),
                             arcade.color.BLACK, font_size=20, anchor_x="center")

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
        if self.back_button.go_back:
            next_view = menu_view.MainMenu()
            self.window.show_view(next_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Tile Miner")
    leaderboard_view = LeaderboardView()
    window.show_view(leaderboard_view)
    arcade.run()


if __name__ == "__main__":
    main()
