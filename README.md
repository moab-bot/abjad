# abjad (moab-bot fork)

This is a fork of [Abjad](https://github.com/Abjad/abjad) extending `NamedPitch` with HEJI2 microtonal accidental rendering for just intonation scores. The active branch is `abjad-ji`.

For installation, usage, and general documentation see the [upstream README](README.rst) and [abjad.github.io](https://abjad.github.io).

## Changes from upstream

**`source/abjad/pitch.py`**
- `_suppress_heji2` slot on `NamedPitch` — when set, suppresses HEJI2 accidental rendering (used for tied-note repetitions)
- `_parenthesize_heji2` slot on `NamedPitch` — when set, wraps the rendered HEJI2 accidental in parentheses
- Fix: missing closing brace in the `\markup` block for the musicglyph parenthesize path

**`source/abjad/score.py`**
- `NoteHead.set_written_pitch()` now propagates `_suppress_heji2` and `_parenthesize_heji2` when copying a `NamedPitch`

**`source/abjad/io.py`**
- `LilyPondIO.__call__()` uses `tempfile.TemporaryDirectory()` context manager instead of `mkdtemp()` so the render scratch directory is automatically cleaned up
- Removed dead `render_directory()` method

## License

GPL v3 — same as upstream. See [LICENSE](LICENSE).
