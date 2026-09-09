
import pytest

# pyrefly: ignore [missing-import]
from src.simulation import Grid


class TestGrid:
    def test_position_within_bounds(self):
        grid = Grid(5, 3)

        # Grid boundaries are inclusive: (0, 0) and (width, height)
        # are both valid positions.
        assert grid.is_within_bounds(0, 0)
        assert grid.is_within_bounds(5, 3)
        assert grid.is_within_bounds(3, 2)

    def test_position_outside_bounds(self):
        grid = Grid(5, 3)

        # Positions beyond any of the four grid edges are invalid.
        assert not grid.is_within_bounds(-1, 0)
        assert not grid.is_within_bounds(0, -1)
        assert not grid.is_within_bounds(6, 3)
        assert not grid.is_within_bounds(5, 4)

    def test_scent_can_be_added_and_detected(self):
        grid = Grid(5, 3)

        assert not grid.has_scent(5, 3, "E")

        grid.add_scent(5, 3, "E")

        assert grid.has_scent(5, 3, "E")

    def test_scent_is_direction_specific(self):
        grid = Grid(5, 3)

        # A scent marks the specific edge from which a robot was lost.
        # The same position may therefore have different behaviour
        # depending on the direction of the attempted movement.
        grid.add_scent(5, 3, "E")

        assert grid.has_scent(5, 3, "E")
        assert not grid.has_scent(5, 3, "N")
        assert not grid.has_scent(5, 3, "S")
        assert not grid.has_scent(5, 3, "W")

    def test_scent_is_position_specific(self):
        grid = Grid(5, 3)

        # A scent only applies to the exact grid edge where the robot
        # was lost; it must not affect the same direction elsewhere.
        grid.add_scent(5, 3, "E")

        assert grid.has_scent(5, 3, "E")
        assert not grid.has_scent(4, 3, "E")
        assert not grid.has_scent(5, 2, "E")
