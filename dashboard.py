import arcade
import time
from constants import *

# TODO: Finish Dashboard class


class Dashboard(object):

    def __init__(self, dashboard_data, timer=60, score=0, message=""):
        self._dashboard_data = dashboard_data
        self.timer = timer
        self.score = score
        self.message = message

    @property
    def dashboard_data(self):
        return self._dashboard_data

    @dashboard_data.setter
    def dashboard_data(self, value):
        if not isinstance(value, dict):
            raise TypeError(f"Incorrect variable type assigned to dashboard_data: {value}")
        self._dashboard_data = value

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise TypeError(f"Incorrect variable type assigned to timer: {value}")
        if value <= 0:
            raise ValueError(f"timer must be greater than zero: {value}")
        self._timer = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Incorrect variable type assigned to score: {value}")
        if value < 0:
            raise ValueError(f"score must be non-negative: {value}")
        self._score = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Incorrect variable type assigned to message: {value}")
        self._message = value

    def setup_dashboard(self):
        # Draw dashboard with border
        arcade.draw_rectangle_filled(**self._dashboard_data, color=arcade.color.BLUE)
        arcade.draw_rectangle_outline(**self._dashboard_data, color=arcade.color.BLACK, border_width=2*MARGIN)

        # Calculate timer (in MM:SS format) and display text
        calc_min = int(self._timer) // 60
        calc_sec = int(self._timer) % 60
        result_time = f"Time left: {calc_min}:{str(calc_sec).zfill(2)}"
        arcade.draw_text(result_time,
                         3 * MARGIN,
                         self._dashboard_data['center_y'] + self._dashboard_data['height'] // 4 - 2 * MARGIN,
                         arcade.color.RED,
                         20,
                         font_name='Verdana',
                         bold=True)

        # Display score
        score_text = f"Score: {self._score}"
        arcade.draw_text(score_text,
                         3 * MARGIN,
                         self._dashboard_data['center_y'] - 4 * MARGIN,
                         arcade.color.RED,
                         20,
                         font_name='Verdana',
                         bold=True)

        # Display message
        arcade.draw_text(self.message,
                         3 * MARGIN,
                         self._dashboard_data['center_y'] - 14 * MARGIN,
                         arcade.color.RED,
                         20,
                         font_name='Verdana',
                         bold=True)

    def display_message(self):
        end_time = time.time() + 2
        while time.time() < end_time:
            pass
        self.message = ""
