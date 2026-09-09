import sys
from pathlib import Path

from .parser import parse_input
from .simulation import simulate


DEFAULT_INPUT_PATH = Path("inputs") / "sample.txt"


def resolve_input_path(arguments: list[str]) -> Path | None:
    """
    Resolve the input file from command-line arguments.

    With no argument, use the sample input file. With one argument,
    use that path. More than one argument is invalid.
    """
    if len(arguments) == 0:
        if DEFAULT_INPUT_PATH.exists():
            return DEFAULT_INPUT_PATH

        return (
            Path(__file__).resolve().parents[1]
            / DEFAULT_INPUT_PATH
        )

    if len(arguments) == 1:
        return Path(arguments[0])

    return None


def main() -> int:
    """Run the Mars robot simulation."""
    input_path = resolve_input_path(sys.argv[1:])

    if input_path is None:
        print(
            f"Usage: python -m src <input-file>",
            file=sys.stderr,
        )
        return 1

    try:
        input_text = input_path.read_text(
            encoding="utf-8-sig",
        )

        width, height, robot_data = parse_input(input_text)
        robots = simulate(width, height, robot_data)

    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    # For debugging
    #print(f"Grid: {width} {height}")

    # Print final robot states
    for robot in robots:
        print(robot.result())

    return 0


if __name__ == "__main__":
    sys.exit(main())

