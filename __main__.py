import arcade
import menu_view
from constants import WIDTH, HEIGHT


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Tile Miner")
    main_view = menu_view.MainMenu(6, 6, 3, 0)
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()
