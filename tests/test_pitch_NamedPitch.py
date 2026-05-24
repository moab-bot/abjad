from fractions import Fraction

import pytest

import abjad

values: list[tuple] = []
values.extend((x / 2, x / 2) for x in range(-48, 49))
values.extend(
    [
        ("bf,", -14),
        ("c'", 0),
        ("cs'", 1),
        ("gff''", 17),
        ("", 0),
        ("dss,,", -32),
        ("fake", ValueError),
        (("bf", 2), -14),
        (("c", 4), 0),
        (("cs", 4), 1),
        (("dss", 1), -32),
        (("gff", 5), 17),
        (abjad.NamedPitch("bs'"), 12),
        (abjad.NamedPitch("c"), -12),
        (abjad.NamedPitch("cf,"), -25),
        (abjad.NamedPitch(), 0),
        (abjad.NamedPitchClass("cs'"), 1),
        (abjad.NamedPitchClass("c"), 0),
        (abjad.NamedPitchClass("cf,"), -1),
        (None, 0),
        (abjad.NumberedPitch("bs'"), 12),
        (abjad.NumberedPitch("c"), -12),
        (abjad.NumberedPitch("cf,"), -25),
        (abjad.NumberedPitch(), 0),
        (abjad.NumberedPitchClass("bs'"), 0),
        (abjad.NumberedPitchClass("c"), 0),
        (abjad.NumberedPitchClass("cf,"), 11),
    ]
)


@pytest.mark.parametrize("input_, expected_semitones", values)
def test_init(input_, expected_semitones):
    if isinstance(expected_semitones, type) and issubclass(
        expected_semitones, Exception
    ):
        with pytest.raises(expected_semitones):
            abjad.NamedPitch(input_)
        return
    instance = abjad.NamedPitch(input_)
    assert float(instance) == expected_semitones


def test_init_from_jitools_pitch():
    class DummyJitoolsPitch:
        def __init__(self, notation, letter_name, keynum):
            self.notation = notation
            self.letter_name = letter_name
            self.keynum = keynum

    jitools_pitch = DummyJitoolsPitch(("N", "A"), "A", 69.0)
    pitch = abjad.NamedPitch(jitools_pitch)
    assert isinstance(pitch, abjad.NamedPitch)
    assert pitch.name() == "a'"
    assert pitch.number() == 9.0
    assert pitch._heli_accidental_string == "N"
    assert pitch.simplify() is pitch
    note_head = abjad.NoteHead(pitch)
    expected = (
        "\\once \\override Accidental.stencil = #ly:text-interface::print\n"
        "\\once \\override Accidental.text = \\markup { \\override #'(font-name . \"HEJI2\") \\magnify #1.75 \"N\" }\n"
        "a'!"
    )
    assert note_head._get_lilypond_format() == expected


def test_init_from_jitools_pitch_with_custom_heji2_magnification():
    class DummyJitoolsPitch:
        def __init__(self, notation, letter_name, keynum):
            self.notation = notation
            self.letter_name = letter_name
            self.keynum = keynum

    jitools_pitch = DummyJitoolsPitch(("N", "A"), "A", 69.0)
    pitch = abjad.NamedPitch(jitools_pitch, heli_magnification=1.25)
    note_head = abjad.NoteHead(pitch)
    expected = (
        "\\once \\override Accidental.stencil = #ly:text-interface::print\n"
        "\\once \\override Accidental.text = \\markup { \\override #'(font-name . \"HEJI2\") \\magnify #1.25 \"N\" }\n"
        "a'!"
    )
    assert note_head._get_lilypond_format() == expected


def test_init_from_ratio():
    pytest.importorskip("jitools.pitch")
    pitch = abjad.NamedPitch.from_ratio(Fraction(5, 4), reference_pitch="C4")
    assert pitch._heli_accidental_string == "m"
    assert pitch.name() == "e'"
    assert pitch.cent_deviation_string() == "-13.68629"
    assert pitch.cent_deviation() == pytest.approx(-13.68629)
    note_head = abjad.NoteHead(pitch)
    expected = (
        "\\once \\override Accidental.stencil = #ly:text-interface::print\n"
        "\\once \\override Accidental.text = \\markup { \\override #'(font-name . \"HEJI2\") \\magnify #1.75 \"m\" }\n"
        "e'!"
    )
    assert note_head._get_lilypond_format() == expected
