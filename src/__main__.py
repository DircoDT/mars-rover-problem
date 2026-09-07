import sys
from pathlib import Path

# pyrefly: ignore [missing-import]
from src.parser import parse_input


def main() -> int:
    """Parse the input file supplied on the command line."""
    if len(sys.argv) != 2:
        print(
            f"Usage: {Path(sys.argv[0]).name} <input-file>",
            file=sys.stderr,
        )
        return 1

    input_filename = sys.argv[1]

    try:
        input_text = Path(input_filename).read_text(encoding="utf-8")
        width, height, robots = parse_input(input_text)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    # TODO: Comment out temporary parser verification output.
    print(f"Grid: {width} {height}")
    for x, y, orientation, commands in robots:
        print(f"Robot: {x} {y} {orientation} {commands}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

