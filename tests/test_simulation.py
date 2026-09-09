
import pytest

# pyrefly: ignore [missing-import]
from src.simulation import simulate


class TestSimulate:
    def test_robots_are_processed_sequentially_on_shared_grid(self):
        robot_data = [
            (5, 3, "E", "F"),
            (5, 3, "E", "F"),
        ]

        # Robots are processed in input order and share the same grid,
        # allowing the second robot to benefit from the first robot's scent.
        robots = simulate(5, 3, robot_data)

        assert robots[0].lost
        assert not robots[1].lost

    def test_scent_persists_between_robots(self):
        robot_data = [
            (5, 3, "E", "F"),
            (5, 3, "E", "F"),
            (5, 3, "E", "F"),
        ]

        # Once a fatal edge has been scented, subsequent robots can
        # continue past that instruction without being lost.
        robots = simulate(5, 3, robot_data)

        assert robots[0].lost
        assert not robots[1].lost
        assert not robots[2].lost

    def test_commandless_robot_is_supported(self):
        robot_data = [
            (2, 2, "N", ""),
        ]

        # An empty command sequence is still a valid robot simulation.
        robots = simulate(5, 3, robot_data)

        assert len(robots) == 1
        assert robots[0].result() == "2 2 N"

    def test_no_robots_is_valid(self):
        # A valid grid may contain no robots.
        robots = simulate(5, 3, [])

        assert robots == []
