
# Developer Notes

This file is for documenting architecture & design decisions during development. It starts with the initial considerations and high-level plan and is then appended to in later commits to add finer details or to provide reasoning behind deviations (e.g. if a previous assumption was inadequate.)

## High-level architecture

### Choice of language

A first reading of the problem statement shows that the focus of the task is on readability and clarity. It does not require a graphical UI, heavy processing, a database or system integrations.

Choice: Python 3 (current stable, not prerelease) with pytest for testing

- Easy to read (almost like pseudocode)
- Does not have a lot of distracting boilerplate
- Cross-platform; minimal infrastructure (just Python; IDE optional.)

### Output format

- No graphical UI required, so just use the CLI.
- The problem statement says to output the final coordinates for each robot.
- Displaying the current map state might be useful for debugging, but is not a required output.

### Input format

- The input string contains line breaks, so instead of stdin, we can rather read it from a text file.
- It is best to assume that the input might be flawed/corrupted in some way; at the very least, unexpected inputs should not break the program.
- Future versions may require more complex inputs, perhaps even binary format, but for now we stick to the text format as specified.

### Program structure

- There are identifiable objects, like planet/map and robot/vehicle, so we could use some basic OOP.
- Focus on readability, so don't go overboard, e.g. making small, abstract objects like "position" or "command" - those can just be arrays of strings/numbers (base types) for now.
- Start with a single .py file, but split it into parts as needed once the overall structure is clear.

### State variables

Here are the main things we want to keep track of:

- The world (planet/environment)
  - There is no map to store in the current problem definition. The grid is represented in the abstract only, by a 2D coordinate system with specified dimensions.
  - "LOST"/"scent" signals can be represented in memory with a set of coordinates (x,y,d) - initially empty - for other robots to look up.
- The robot position & orientation
  - Only its current state is relevant during execution, not its movement history.
  - Can print its movements to the console, if intermediate steps are needed for debugging.

_*Note:* There is a slight ambiguity in the way scents are described - whether they should block any subsequent movement off that position, or only if the attempt is also in the same direction. We interpret the latter: we do not want to trap future robots on that gridpoint, but only prevent them from going over the same edge. Therefore, we represent a scent using (x,y,d) rather than just (x,y)._

### Tests

- The problem has a small number of well-defined transitions, making it practical to specify expected behaviour early. But don't fetishise TDD.
- Unit tests should at least include
  - validating that the input file was read accurately
  - validating robot actions
- Integration/E2E test should check that we get the correct final output
  - for the known input samples provided
  - for any significant edge cases that are not covered by the given samples

### Future considerations

The problem states that near-future requirements may include new robot commands, among other features. While we should not try to predict too far ahead, it is prudent to anticipate at least the next logical step that a client may ask for next, to avoid painting ourselves into a corner with the current implementation and having to redo some of it. (It's like the inverse of technical debt.)

So, what are some things that may be added to the inputs, behavioural logic or outputs in the next phase, and what are their implications?

- Potential commands:
  - Backward
  - Jump
  - Shoot laser
  - Collect/Drop dirt
  - Forward x 5
  - Right 45 degrees

- Potential map:
  - Digital Elevation Map (height at each gridpoint)
  - Obstacles (is a gridpoint open or blocked)

- Potential logic:
  - Slighly more autonomous behaviour (internal if statements to react to the environment without an explicit command)
  - Sensors, collision handling, different movement rules, etc.

The initial architecture should avoid unnecessarily constraining these future directions. However, the design should not attempt to implement or fully abstract unknown requirements prematurely. New abstractions should be introduced when an actual requirement demonstrates that they are needed.


