
# Martian Robots

A Python solution to the Martian Robots challenge.

The program simulates robots moving on a bounded rectangular grid according to a sequence of provided instructions, including the handling of robots that are lost and the warning ("scent") they leave behind for other robots.

## Requirements

**Python 3.10+** (Python 3.14 recommended as latest stable release - see https://python.org)

## Setup

Clone the repository:

```
git clone https://github.com/DircoDT/mars-rover-problem.git
cd mars-rover-problem
```

Create a virtual environment and install the dependencies (`pytest`, specified in `pyproject.toml`):

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Run

From the `mars-rover-problem` folder:

```
python -m src inputs\sample.txt
```

## Test

```
pytest
```

See [NOTES.md](NOTES.md) to follow the architectural and design decisions made.
