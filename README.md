
# Martian Robots

A Python solution to the Martian Robots challenge.

The program simulates robots moving on a bounded rectangular grid according to a sequence of provided instructions, including the handling of robots that are lost and the warning ("scent") they leave behind for other robots.

See [NOTES.md](NOTES.md) to follow the architectural and design decisions made.

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

(From inside the `mars-rover-problem` folder.)

Activate environment, if not already active:
```
.venv\Scripts\activate
```

Then run the simulation with the specified input file:
```
python -m src inputs\sample.txt
```

## Test

(From inside the `mars-rover-problem` folder.)

Activate environment, if not already active:
```
.venv\Scripts\activate
```

Then run all the tests:
```
pytest
```
