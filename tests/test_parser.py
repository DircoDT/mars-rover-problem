import pytest

# pyrefly: ignore [missing-import]
from src.parser import (
    MAX_COORDINATE,
    parse_commands,
    parse_dimensions,
    parse_input,
    parse_robot_position,
)


# ---------------------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------------------

def test_parse_dimensions():
    assert parse_dimensions("5 3") == (5, 3)


def test_dimensions_allow_leading_and_trailing_whitespace():
    assert parse_dimensions("  5 3  ") == (5, 3)
    assert parse_dimensions("\t5 3\t") == (5, 3)


def test_dimensions_allow_multiple_spaces():
    assert parse_dimensions("5     3") == (5, 3)


def test_dimensions_allow_tabs_between_values():
    assert parse_dimensions("5\t3") == (5, 3)


def test_dimensions_allow_zero_padded_values():
    assert parse_dimensions("05 03") == (5, 3)


@pytest.mark.parametrize(
    "line",
    [
        "",
        "5",
        "5 3 2",
        "5x3",
        "5,3",
        "5-3",
        "5.3",
        "five 3",
        "5 three",
        "5 3 N",
        "N 5 3",
    ],
)
def test_invalid_dimensions_are_rejected(line):
    with pytest.raises(ValueError):
        parse_dimensions(line)


def test_maximum_grid_dimensions_are_allowed():
    assert parse_dimensions(
        f"{MAX_COORDINATE} {MAX_COORDINATE}"
    ) == (MAX_COORDINATE, MAX_COORDINATE)


@pytest.mark.parametrize(
    "line",
    [
        "51 3",
        "3 51",
        "51 51",
    ],
)
def test_grid_dimensions_above_maximum_are_rejected(line):
    with pytest.raises(ValueError):
        parse_dimensions(line)


# ---------------------------------------------------------------------------
# Robot positions
# ---------------------------------------------------------------------------

def test_parse_robot_position():
    assert parse_robot_position("1 2 N") == (1, 2, "N")


def test_robot_position_allows_whitespace():
    assert parse_robot_position("  1   2   N  ") == (1, 2, "N")
    assert parse_robot_position("\t1\t2\tN\t") == (1, 2, "N")


def test_robot_orientation_is_case_insensitive():
    assert parse_robot_position("1 2 n") == (1, 2, "N")
    assert parse_robot_position("1 2 e") == (1, 2, "E")
    assert parse_robot_position("1 2 s") == (1, 2, "S")
    assert parse_robot_position("1 2 w") == (1, 2, "W")


def test_robot_position_allows_multiple_spaces():
    assert parse_robot_position("1     2     E") == (1, 2, "E")


def test_robot_position_allows_tabs():
    assert parse_robot_position("1\t2\tE") == (1, 2, "E")


def test_robot_coordinates_allow_zero_padded_values():
    assert parse_robot_position("01 002 E") == (1, 2, "E")


@pytest.mark.parametrize(
    "line",
    [
        "",
        "1",
        "1 2",
        "1 2 N extra",
        "extra 1 2 N",
        "1,2,N",
        "1-2-N",
        "1.2.N",
        "1 2 X",
        "1 2 North",
        "one 2 N",
        "1 two N",
    ],
)
def test_invalid_robot_positions_are_rejected(line):
    with pytest.raises(ValueError):
        parse_robot_position(line)


@pytest.mark.parametrize(
    "line",
    [
        "51 0 N",
        "0 51 N",
        "51 51 N",
    ],
)
def test_robot_coordinates_above_maximum_are_rejected(line):
    with pytest.raises(ValueError):
        parse_robot_position(line)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def test_parse_commands():
    assert parse_commands("LFR") == "LFR"


def test_commands_allow_whitespace():
    assert parse_commands(" L F R ") == "LFR"
    assert parse_commands("\tL\tF\tR\t") == "LFR"


def test_commands_can_span_multiple_lines():
    assert parse_commands(
        """
        L
        F
        R
        """
    ) == "LFR"


def test_commands_are_case_insensitive():
    assert parse_commands("lFr") == "LFR"


def test_empty_commands_are_valid():
    assert parse_commands("") == ""
    assert parse_commands("   ") == ""
    assert parse_commands("\t\t") == ""


@pytest.mark.parametrize(
    "line",
    [
        "X",
        "LFX",
        "L-R",
        "L,F",
        "123",
        "forward",
        "LFR!",
    ],
)
def test_invalid_commands_are_rejected(line):
    with pytest.raises(ValueError):
        parse_commands(line)


# ---------------------------------------------------------------------------
# Complete input
# ---------------------------------------------------------------------------

def test_parse_sample_input():
    input_text = """
    5 3

    1 1 E
    RFRFRFRF

    3 2 N
    FRRFLLFFRRFLL

    0 3 W
    LLFFFLFLFL
    """

    assert parse_input(input_text) == (
        5,
        3,
        [
            (1, 1, "E", "RFRFRFRF"),
            (3, 2, "N", "FRRFLLFFRRFLL"),
            (0, 3, "W", "LLFFFLFLFL"),
        ],
    )


def test_blank_lines_can_appear_between_records():
    input_text = """

    5     3

    1   1   E
    R F R F


    3  2 N

    F R R F L L F F R R F L L


    0 3 W

    L L F F F L F L F L

    """

    assert parse_input(input_text) == (
        5,
        3,
        [
            (1, 1, "E", "RFRF"),
            (3, 2, "N", "FRRFLLFFRRFLL"),
            (0, 3, "W", "LLFFFLFLFL"),
        ],
    )


def test_commandless_robot_is_valid():
    input_text = """
    5 3

    1 1 E

    3 2 N
    FRRF

    0 3 W
    """

    assert parse_input(input_text) == (
        5,
        3,
        [
            (1, 1, "E", ""),
            (3, 2, "N", "FRRF"),
            (0, 3, "W", ""),
        ],
    )


def test_commands_can_span_multiple_lines():
    input_text = """
    5 3

    1 1 E
    L
    F
    R

    3 2 N
    F R
    R F L
    """

    assert parse_input(input_text) == (
        5,
        3,
        [
            (1, 1, "E", "LFR"),
            (3, 2, "N", "FRRFL"),
        ],
    )


def test_commandless_robot_can_be_between_other_robots():
    input_text = """
    5 3

    1 1 E
    LFR

    3 2 N


    0 3 W
    R
    """

    assert parse_input(input_text) == (
        5,
        3,
        [
            (1, 1, "E", "LFR"),
            (3, 2, "N", ""),
            (0, 3, "W", "R"),
        ],
    )


def test_no_robots_is_valid():
    assert parse_input("5 3") == (5, 3, [])


def test_no_robots_with_blank_lines_is_valid():
    assert parse_input(
        """
        5 3



        """
    ) == (5, 3, [])


def test_empty_input_is_rejected():
    with pytest.raises(ValueError):
        parse_input("")


def test_whitespace_only_input_is_rejected():
    with pytest.raises(ValueError):
        parse_input("   \n\t\n  ")


def test_missing_dimensions_is_rejected():
    with pytest.raises(ValueError):
        parse_input(
            """
            1 1 N
            RFRF
            """
        )


def test_unexpected_data_before_first_robot_is_rejected():
    with pytest.raises(ValueError):
        parse_input(
            """
            5 3
            unexpected
            1 1 E
            RFRF
            """
        )


def test_invalid_robot_position_is_rejected():
    with pytest.raises(ValueError):
        parse_input(
            """
            5 3
            1 1 X
            RFRF
            """
        )


def test_invalid_instruction_is_rejected():
    with pytest.raises(ValueError):
        parse_input(
            """
            5 3
            1 1 E
            RFRX
            """
        )


def test_extra_fields_are_rejected():
    with pytest.raises(ValueError):
        parse_input(
            """
            5 3
            1 1 E extra
            RFRF
            """
        )


def test_punctuation_is_not_treated_as_whitespace():
    with pytest.raises(ValueError):
        parse_input(
            """
            5-3
            1,1,E
            RFRF
            """
        )


def test_missing_robot_coordinate_is_rejected():
    with pytest.raises(ValueError):
        parse_input(
            """
            5 3
            1 N
            RFRF
            """
        )


def test_missing_robot_orientation_is_rejected():
    with pytest.raises(ValueError):
        parse_input(
            """
            5 3
            1 1
            RFRF
            """
        )


def test_invalid_text_between_robots_is_rejected():
    with pytest.raises(ValueError):
        parse_input(
            """
            5 3
            1 1 E
            RFRF
            invalid!
            3 2 N
            F
            """
        )


def test_robot_coordinates_are_not_required_to_match_grid_bounds():
    # Parsing validates the challenge's maximum coordinate constraint,
    # but whether a robot starts inside a particular world is a domain
    # concern rather than a parser concern.
    assert parse_input(
        """
        5 3
        5 3 N
        F
        """
    ) == (
        5,
        3,
        [
            (5, 3, "N", "F"),
        ],
    )

