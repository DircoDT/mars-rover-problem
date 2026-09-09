import pytest

# pyrefly: ignore [missing-import]
from src.simulation import Grid, Robot


class TestRobot:
    @pytest.mark.parametrize(
        ("initial_direction", "command", "expected_direction"),
        [
            ("N", "L", "W"),
            ("W", "L", "S"),
            ("S", "L", "E"),
            ("E", "L", "N"),
            ("N", "R", "E"),
            ("E", "R", "S"),
            ("S", "R", "W"),
            ("W", "R", "N"),
        ],
    )
    def test_turning(
        self,
        initial_direction,
        command,
        expected_direction,
    ):
        grid = Grid(5, 3)
        robot = Robot(grid, 1, 1, initial_direction)

        # Turning changes only the robot's orientation, not its position.
        robot.execute(command)

        assert robot.direction == expected_direction
        assert robot.x == 1
        assert robot.y == 1
        assert not robot.lost

    @pytest.mark.parametrize(
        ("direction", "expected_position"),
        [
            ("N", (1, 2)),
            ("E", (2, 1)),
            ("S", (1, 0)),
            ("W", (0, 1)),
        ],
    )
    def test_move_forward(self, direction, expected_position):
        grid = Grid(5, 3)
        robot = Robot(grid, 1, 1, direction)

        # Forward movement advances exactly one grid point in the
        # direction the robot is facing.
        robot.execute("F")

        assert (robot.x, robot.y) == expected_position
        assert robot.direction == direction
        assert not robot.lost

    def test_multiple_commands_are_executed_in_order(self):
        grid = Grid(5, 3)
        robot = Robot(grid, 1, 1, "E")

        # Commands are executed sequentially, with each command operating
        # on the state produced by the preceding command.
        robot.execute("RFRF")  # moves one South and then one West

        assert (robot.x, robot.y) == (0, 0)
        assert robot.direction == "W"
        assert not robot.lost

    @pytest.mark.parametrize(
        ("position", "direction"),
        [
            ((0, 0), "S"),
            ((0, 0), "W"),
            ((5, 3), "N"),
            ((5, 3), "E"),
        ],
    )
    def test_moving_off_grid_loses_robot(self, position, direction):
        grid = Grid(5, 3)
        robot = Robot(grid, *position, direction)

        # Moving beyond a grid edge makes the robot lost. Its reported
        # position remains the last valid grid point.
        robot.execute("F")

        assert (robot.x, robot.y) == position
        assert robot.direction == direction
        assert robot.lost

    def test_lost_robot_leaves_scent(self):
        grid = Grid(5, 3)
        robot = Robot(grid, 5, 3, "E")

        # The attempted movement is recorded so that subsequent robots
        # can safely ignore the same fatal edge.
        robot.execute("F")

        assert grid.has_scent(5, 3, "E")

    def test_lost_robot_stops_executing_commands(self):
        grid = Grid(5, 3)
        robot = Robot(grid, 5, 3, "E")

        # Once a robot is lost, all remaining instructions are ignored.
        # In particular, the L after F must not change its direction.
        robot.execute("FL")

        assert robot.x == 5
        assert robot.y == 3
        assert robot.direction == "E"
        assert robot.lost

    def test_scent_prevents_robot_from_being_lost(self):
        grid = Grid(5, 3)

        first_robot = Robot(grid, 5, 3, "E")
        first_robot.execute("F")

        second_robot = Robot(grid, 5, 3, "E")
        second_robot.execute("F")

        # The second robot encounters the scent left by the first robot
        # and ignores the otherwise fatal movement.
        assert first_robot.lost
        assert not second_robot.lost
        assert (second_robot.x, second_robot.y) == (5, 3)

    def test_scent_does_not_prevent_movement_in_another_direction(self):
        grid = Grid(5, 3)

        first_robot = Robot(grid, 5, 3, "E")
        first_robot.execute("F")

        second_robot = Robot(grid, 5, 3, "S")
        second_robot.execute("F")

        # The scent only protects against the same edge being crossed.
        # A different direction from the same position remains valid.
        assert first_robot.lost
        assert not second_robot.lost
        assert (second_robot.x, second_robot.y) == (5, 2)

    def test_scent_does_not_prevent_movement_from_another_position(self):
        grid = Grid(5, 3)

        first_robot = Robot(grid, 5, 3, "E")
        first_robot.execute("F")

        second_robot = Robot(grid, 4, 3, "E")
        second_robot.execute("F")

        # The scent belongs to the edge at (5, 3), not to the direction
        # globally. The second robot can therefore move to (5, 3).
        assert first_robot.lost
        assert not second_robot.lost
        assert (second_robot.x, second_robot.y) == (5, 3)

    def test_commandless_robot_does_not_move(self):
        grid = Grid(5, 3)
        robot = Robot(grid, 2, 1, "N")

        # An empty instruction block represents a valid commandless robot.
        robot.execute("")

        assert robot.x == 2
        assert robot.y == 1
        assert robot.direction == "N"
        assert not robot.lost

    def test_result_for_robot_that_is_not_lost(self):
        grid = Grid(5, 3)
        robot = Robot(grid, 1, 1, "E")

        assert robot.result() == "1 1 E"

    def test_result_for_lost_robot(self):
        grid = Grid(5, 3)
        robot = Robot(grid, 5, 3, "E")

        robot.execute("F")

        # LOST is appended to the final valid position and orientation.
        assert robot.result() == "5 3 E LOST"

    def test_invalid_command_is_rejected(self):
        grid = Grid(5, 3)
        robot = Robot(grid, 1, 1, "N")

        # The parser normally guarantees valid commands, but Robot keeps
        # a defensive check at the simulation boundary.
        with pytest.raises(ValueError, match="Invalid command"):
            robot.execute("X")
