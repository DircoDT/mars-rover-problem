import re


MAX_COORDINATE = 50

DIMENSIONS_PATTERN = re.compile(
    r"^[^0-9a-z]*(\d+)[^0-9a-z]+(\d+)[^0-9a-z]*$",
    re.IGNORECASE,
)

ROBOT_PATTERN = re.compile(
    r"^[^0-9a-z]*(\d+)[^0-9a-z]+(\d+)[^0-9a-z]+([NSEW])[^0-9a-z]*$",
    re.IGNORECASE,
)

COMMANDS_PATTERN = re.compile(
    r"^([^0-9a-z]|[LRF])*$",
    re.IGNORECASE,
)


def parse_dimensions(line: str) -> tuple[int, int]:
    """Parse and validate grid dimensions."""
    match = DIMENSIONS_PATTERN.fullmatch(line)

    if match is None:
        raise ValueError(f"Invalid grid dimensions: {line!r}")

    width, height = (int(value) for value in match.groups())

    if width > MAX_COORDINATE or height > MAX_COORDINATE:
        raise ValueError(
            f"Grid dimensions must not exceed {MAX_COORDINATE}: "
            f"{width} {height}"
        )

    return width, height


def parse_robot_position(
    line: str,
) -> tuple[int, int, str]:
    """Parse and validate a robot position."""
    match = ROBOT_PATTERN.fullmatch(line)

    if match is None:
        raise ValueError(f"Invalid robot position: {line!r}")

    x, y, orientation = match.groups()
    x = int(x)
    y = int(y)

    if x > MAX_COORDINATE or y > MAX_COORDINATE:
        raise ValueError(
            f"Robot coordinates must not exceed {MAX_COORDINATE}: "
            f"{x} {y}"
        )

    return x, y, orientation.upper()


def parse_commands(text: str) -> str:
    """
    Parse and validate a robot instruction block.

    Whitespace and non-alphanumeric characters are ignored, so commands may
    be on one or multiple lines, comma-separated, etc. An empty block represents
    a commandless robot.
    """
    if COMMANDS_PATTERN.fullmatch(text) is None:
        raise ValueError(f"Invalid robot instructions: {text!r}")

    return "".join(
        character
        for character in text.upper()
        if character in "LRF"
    )


def parse_input(
    input_text: str,
) -> tuple[int, int, list[tuple[int, int, str, str]]]:
    """
    Parse the complete challenge input.

    The first non-blank line contains the grid dimensions.

    Each subsequent robot is identified by a robot-position line.
    Everything between that position line and the next robot-position
    line is treated as that robot's instruction block.

    Instruction blocks may contain zero or more lines and may contain
    arbitrary whitespace or non-alphanumeric characters. An empty instruction
    block represents a commandless robot.

    Apart from whitespace and non-alphanumeric delimiters, the input must
    follow the expected format exactly.
    """

    # OS-agnostic splitting (LF/CRLF/CR)
    lines = input_text.splitlines()

    # Find the first non-blank line. It must contain the dimensions.
    first_nonblank = next(
        (index for index, line in enumerate(lines) if line.strip()),
        None,
    )

    if first_nonblank is None:
        raise ValueError("Input is empty")

    width, height = parse_dimensions(lines[first_nonblank])

    # Everything after the dimensions belongs to the robot section.
    robot_text = "\n".join(lines[first_nonblank + 1:])

    # Robot positions are structural delimiters between instruction
    # blocks. They must occur on their own lines.
    robot_position_pattern = re.compile(
        r"(?im)^[^0-9a-z\r\n]*(\d+)[^0-9a-z\r\n]+(\d+)[^0-9a-z\r\n]+([NSEW])[^0-9a-z\r\n]*$"
    )

    matches = list(robot_position_pattern.finditer(robot_text))

    if not matches:
        # No robots is valid, provided the remainder contains only
        # whitespace.
        if robot_text.strip():
            raise ValueError(
                "Input contains data that is not a robot position"
            )

        return width, height, []

    # Anything before the first robot position must be whitespace.
    if robot_text[:matches[0].start()].strip():
        raise ValueError(
            "Unexpected data before first robot position"
        )

    robots = []

    for index, match in enumerate(matches):
        x = int(match.group(1))
        y = int(match.group(2))
        orientation = match.group(3).upper()

        if x > MAX_COORDINATE or y > MAX_COORDINATE:
            raise ValueError(
                f"Robot coordinates must not exceed {MAX_COORDINATE}: "
                f"{x} {y}"
            )

        # Everything between this robot's position and the next
        # robot position belongs to this robot's instruction block.
        block_start = match.end()

        if index + 1 < len(matches):
            block_end = matches[index + 1].start()
        else:
            block_end = len(robot_text)

        command_block = robot_text[block_start:block_end]
        commands = parse_commands(command_block)

        robots.append((x, y, orientation, commands))

    return width, height, robots
