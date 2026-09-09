import pytest
from pathlib import Path

# pyrefly: ignore [missing-import]
from src.__main__ import main


SAMPLE_INPUT = """\
5 3
1 1 E
RFRFRFRF
3 2 N
FRRFLLFFRRFLL
0 3 W
LLFFFLFLFL
"""


def test_sample_input_produces_expected_output(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "sample.txt"
    input_file.write_text(SAMPLE_INPUT, encoding="utf-8")

    # Invoke the application through its command-line entry point,
    # supplying a real input file rather than calling parser/simulation
    # functions directly.
    monkeypatch.setattr(
        "sys.argv",
        ["python", str(input_file)],
    )

    exit_code = main()

    captured = capsys.readouterr()

    # This exercises the complete path:
    # input file -> parser -> simulation -> formatted stdout.
    assert exit_code == 0
    assert captured.out == (
        "1 1 E\n"
        "3 3 N LOST\n"
        "2 3 S\n"
    )
    assert captured.err == ""


def test_commandless_robot_works_end_to_end(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "commandless.txt"
    input_file.write_text(
        """\
5 3
1 1 E

3 2 N
FRF
""",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["python", str(input_file)],
    )

    exit_code = main()

    captured = capsys.readouterr()

    # The blank instruction block is interpreted as a commandless robot,
    # while the following robot is still parsed and simulated normally.
    assert exit_code == 0
    assert captured.out == (
        "1 1 E\n"
        "4 3 E\n"
    )
    assert captured.err == ""


def test_invalid_input_returns_error(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "invalid.txt"
    input_file.write_text(
        """\
5 3
1 1 E
RFQ
""",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["python", str(input_file)],
    )

    exit_code = main()

    captured = capsys.readouterr()

    # Invalid input should produce a non-zero exit status and an error
    # on stderr, without writing anything to the required output stream.
    assert exit_code == 1
    assert captured.out == ""
    assert "Error:" in captured.err


def test_missing_input_file_returns_error(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    input_file = tmp_path / "does-not-exist.txt"

    monkeypatch.setattr(
        "sys.argv",
        ["python", str(input_file)],
    )

    exit_code = main()

    captured = capsys.readouterr()

    # File errors are handled by the application rather than escaping
    # as an unhandled exception.
    assert exit_code == 1
    assert captured.out == ""
    assert "Error:" in captured.err


def test_default_sample_input_is_used_when_no_argument_is_given(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    inputs_directory = tmp_path / "inputs"
    inputs_directory.mkdir()

    input_file = inputs_directory / "sample.txt"
    input_file.write_text(SAMPLE_INPUT, encoding="utf-8")

    # Run from a temporary project-like directory so that the default
    # relative input path can be tested without touching the real sample.
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "sys.argv",
        ["python"],
    )

    exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == (
        "1 1 E\n"
        "3 3 N LOST\n"
        "2 3 S\n"
    )
