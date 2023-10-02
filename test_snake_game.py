import snake_game
import pytest
import unittest
from parameterized import parameterized


class TestSnakeGame(unittest.TestCase):
    @parameterized.expand([
        (0, 0, "down", 650, 650, True, 50, 0, 50),
        (0, 0, "up", 650, 650, False, 50, 0, 600),
        (0, 0, "right", 650, 650, True, 50, 50, 0),
        (0, 0, "left", 650, 650, False, 50, 600, 0)
    ])
    def test_get_new_head_coordinates(self, x_head, y_head, direction, game_height, game_width,
                                      check_window_border, element_size, expected_x_head, expected_y_head):
        actual_x_head, actual_y_head = snake_game.get_new_head_coordinates(x_head, y_head, direction, game_height, game_width,
                                      check_window_border, element_size)
        assert expected_x_head == actual_x_head
        assert expected_y_head == actual_y_head


    @parameterized.expand([
        ("up", "down", False),
        ("down", "up", False),
        ("left", "right", False),
        ("right", "left", False),
        ("right", "up", True),
        ("right", "down", True),
        ("down", "left", True),
    ])
    def test_is_new_direction_allowed(self, old_direction, new_direction, is_allowed):
        assert is_allowed == snake_game.is_new_direction_allowed(old_direction, new_direction)


    @parameterized.expand([
        (1280, 650, 720, 650, "650x650+315+35"),
        (1280, 500, 720, 500, "500x500+390+110"),
        (1920, 650, 1080, 650, "650x650+635+215"),
        (1920, 500, 1080, 500, "500x500+710+290"),
        (2560, 650, 1440, 650, "650x650+955+395"),
        (2560, 500, 1440, 500, "500x500+1030+470")
    ])
    def test_format_window_geometry(self, screen_width, window_width, screen_height, window_height, expected_format):
        assert expected_format == snake_game.format_window_geometry(screen_width, window_width, screen_height, window_height)