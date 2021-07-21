import arcade
import main_menu
from constants import *


class ReturnView(arcade.View):
    """ View to show instructions """

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.LIGHT_TAUPE)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("GAME OVER", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to return to the menu", WIDTH / 2, HEIGHT / 2-75,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        next_view = main_menu.MainMenu()
        self.window.width = WIDTH
        self.window.height = HEIGHT
        self.window.show_view(next_view)
