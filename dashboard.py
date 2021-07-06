import arcade
from constants import *

# TODO: Finish Dashboard class


class Dashboard(object):

    def __init__(self, dashboard_data, timer=60, score=0):
        self._dashboard_data = dashboard_data
        self._timer = timer
        self._score = score

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value):
        self._timer = value

    def setup_dashboard(self):
        arcade.draw_rectangle_filled(**self._dashboard_data, color=arcade.color.BLUE)
        arcade.draw_rectangle_outline(**self._dashboard_data, color=arcade.color.BLACK, border_width=2*MARGIN)
        calc_min = int(self._timer) // 60
        calc_sec = int(self._timer) % 60
        result_time = f"Time left: {calc_min}:{str(calc_sec).zfill(2)}"
        arcade.draw_text(result_time,
                         3*MARGIN,
                         self._dashboard_data['center_y'] + self._dashboard_data['height'] // 4 - 2*MARGIN,
                         arcade.color.RED,
                         20,
                         font_name=('Verdana'),
                         bold=True)
        score_text = f"Score: {self._score}"
        arcade.draw_text(score_text,
                         3 * MARGIN,
                         self._dashboard_data['center_y'] - 4 * MARGIN,
                         arcade.color.RED,
                         20,
                         font_name=('Verdana'),
                         bold=True)