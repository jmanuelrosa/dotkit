import io

from dotkit import colors


def test_colour_is_off_without_a_terminal():
    assert colors.paint("x", "green") == "x"


def test_force_color_paints_with_the_fish_reset(coloured):
    assert colors.paint("x", "green") == "\x1b[32mx\x1b[m"


def test_no_color_wins_over_force_color(coloured, monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    assert not colors.enabled()


def test_a_stream_without_isatty_is_plain():
    assert not colors.enabled(object())


def test_strip_removes_every_escape(coloured):
    assert colors.strip(colors.paint("x", "bold") + colors.cross()) == "x✗"


def test_for_stream_strips_what_a_pipe_refuses(coloured, monkeypatch):
    painted = colors.paint("x", "cyan")
    monkeypatch.delenv("FORCE_COLOR")
    assert colors.for_stream(painted, io.StringIO()) == "x"
