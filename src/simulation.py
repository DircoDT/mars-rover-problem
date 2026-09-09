
DIRECTIONS = "NESW"

MOVEMENTS = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


class Grid:
    """The rectangular Mars grid and its lost-robot scents."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        # A scent identifies a specific edge of a grid point.
        # For example, (5, 3, "E") means a robot attempting to move
        # east from (5, 3) would fall from the grid.
        self._scents: set[tuple[int, int, str]] = set()

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Return whether a position lies within the grid."""
        return (
            0 <= x <= self.width
            and 0 <= y <= self.height
        )

    def has_scent(self, x: int, y: int, direction: str) -> bool:
        """Return whether a scent exists for this exact edge."""
        return (x, y, direction) in self._scents

    def add_scent(self, x: int, y: int, direction: str) -> None:
        """Record a lost robot's attempted movement."""
        self._scents.add((x, y, direction))


class Robot:
    """A robot moving around a Mars grid."""

    def __init__(
        self,
        grid: Grid,
        x: int,
        y: int,
        direction: str,
    ) -> None:
        self.grid = grid
        self.x = x
        self.y = y
        self.direction = direction
        self.lost = False

    def execute(self, commands: str) -> None:
        """Execute the robot's instruction sequence."""
        for command in commands:
            if command == "L":
                self._turn_left()
            elif command == "R":
                self._turn_right()
            elif command == "F":
                self._move_forward()
            else:
                # The parser already guarantees valid commands.
                # Keep this as a defensive check at the simulation boundary.
                raise ValueError(f"Invalid command: {command!r}")

            if self.lost:
                break

    def _turn_left(self) -> None:
        """Turn 90 degrees to the left."""
        index = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(index - 1) % len(DIRECTIONS)]

    def _turn_right(self) -> None:
        """Turn 90 degrees to the right."""
        index = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(index + 1) % len(DIRECTIONS)]

    def _move_forward(self) -> None:
        """Move forward or become lost at the edge of the grid."""
        dx, dy = MOVEMENTS[self.direction]

        new_x = self.x + dx
        new_y = self.y + dy

        if self.grid.is_within_bounds(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return

        # A previous robot may already have fallen from this exact edge.
        # In that case this robot ignores the movement instruction.
        if self.grid.has_scent(self.x, self.y, self.direction):
            return

        # Otherwise the robot is lost and leaves a scent for future robots.
        self.grid.add_scent(self.x, self.y, self.direction)
        self.lost = True

    def result(self) -> str:
        """Return the robot's final state in challenge output format."""
        result = f"{self.x} {self.y} {self.direction}"

        if self.lost:
            result += " LOST"

        return result


def simulate(
    width: int,
    height: int,
    robot_data: list[tuple[int, int, str, str]],
) -> list[Robot]:
    """Create and execute all robots sequentially on one shared grid."""
    grid = Grid(width, height)
    robots: list[Robot] = []

    for x, y, direction, commands in robot_data:
        robot = Robot(
            grid=grid,
            x=x,
            y=y,
            direction=direction,
        )

        robot.execute(commands)
        robots.append(robot)

    return robots

