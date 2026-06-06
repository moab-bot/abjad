# abjad (moab-bot fork)

This is a fork of [Abjad](https://github.com/Abjad/abjad) adding just intonation pitch support via the [jitools](https://github.com/sclark/jitools) library and HEJI2 microtonal accidental rendering in LilyPond output. The active branch is `abjad-ji`.

For installation, usage, and general documentation see the [upstream README](README.rst) and [abjad.github.io](https://abjad.github.io).

## Prerequisites

- **LilyPond** 2.25.26 or later — see upstream README for install instructions
- **HEJI2 font** — required for microtonal accidental rendering; install from [PLAINSOUND/HEJI2](https://github.com/PLAINSOUND/HEJI2)

## Installation

```
pip install abjad[ji]
```

## What this fork adds

`NamedPitch` can now be instantiated directly from a JI ratio or a jitools `Pitch` object. The resulting pitch carries its HEJI2 accidental glyph, cent deviation from the nearest 12-EDO pitch, and exact pitch number. When rendered to LilyPond, accidentals are emitted using the HEJI2 font via `\once \override` contributions rather than standard abjad accidental notation.

Specific additions to `NamedPitch`:
- Instantiation from an integer ratio tuple `(n, d)` or `fractions.Fraction` (requires jitools)
- `from_ratio(ratio, reference_pitch)` class method
- `cent_deviation()` and `cent_deviation_string()` methods
- `simplify()` — returns self for JI pitches (prevents abjad from enharmonically respelling them)
- Configurable HEJI2 magnification per pitch or globally via `HEJI2_MAGNIFICATION`
- `_suppress_heji2` slot — suppresses accidental rendering (used for tied-note repetitions)
- `_parenthesize_heji2` slot — wraps the rendered accidental in parentheses

## Changes from upstream

**`source/abjad/pitch.py`** — all of the above, plus a fix for a missing closing brace in the `\markup` block for the musicglyph parenthesize path

**`source/abjad/score.py`** — `NoteHead.set_written_pitch()` propagates all JI-specific slots when copying a `NamedPitch`

**`source/abjad/io.py`** — `LilyPondIO.__call__()` uses `tempfile.TemporaryDirectory()` instead of `mkdtemp()` so the render scratch directory is automatically cleaned up; removed dead `render_directory()` method

## License

GPL v3 — same as upstream. See [LICENSE](LICENSE).
