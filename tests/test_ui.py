"""The python vocabulary on its own. The fish differential test lives in dotfiles, beside _ui.fish."""

import os
import unicodedata

import pytest

from dotkit import ui

RESET = "\x1b[m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"
DIM = "\x1b[90m"
BOLD = "\x1b[1m"


# --- the glyphs -------------------------------------------------------------


@pytest.mark.parametrize(
    "kind,expected",
    [
        ("ok", f"{GREEN}✓{RESET} it worked"),
        ("warn", f"{YELLOW}⚠{RESET} it might not have"),
        ("err", f"{MAGENTA}✗{RESET} it did not"),
        ("step", f"{CYAN}→{RESET} doing it"),
    ],
)
def test_a_status_glyph_is_coloured_and_the_message_is_not(coloured, kind, expected):
    """The glyph carries the colour. A fully painted sentence competes with it and
    reads badly on half the terminal themes in use."""
    assert ui.render(kind, expected.split(" ", 1)[1]) == expected


def test_a_title_paints_its_whole_text(coloured):
    assert ui.render("title", "🧩 Available skills:") == f"{BOLD}🧩 Available skills:{RESET}"


def test_a_note_is_dim_and_indented_under_the_line_it_qualifies(coloured):
    assert ui.render("note", "an aside") == f"  {DIM}an aside{RESET}"


def test_the_summary_emoji_is_supplied_by_the_vocabulary(coloured):
    """✨ is the one emoji this module adds itself: every script closes the same way."""
    assert ui.render("done", "all done") == "✨ all done"


def test_colour_is_off_when_not_a_terminal():
    assert ui.render("ok", "plain") == "✓ plain"


# --- layout -----------------------------------------------------------------


@pytest.mark.parametrize("kind,expected", [("item", 2), ("note", 2), ("ok", 0), ("title", 0)])
def test_default_indents(kind, expected):
    """Only the two kinds that sit *under* something are indented by default."""
    line = ui.render(kind, "x")
    assert len(line) - len(line.lstrip()) == expected


def test_indent_is_overridable():
    assert ui.render("ok", "x", indent=4) == "    ✓ x"


def test_only_a_column_zero_kind_carries_a_wide_marker():
    """A wide marker knocks every following column out of line, which is what makes an
    emoji unusable as a row glyph and ✓ ⚠ ✗ · → usable. ✨ is wide, and is allowed
    because `done` starts at column zero and nothing is aligned beneath it."""
    for kind, (glyph, _, _, indent) in ui.KINDS.items():
        if glyph is None:
            continue
        wide = unicodedata.east_asian_width(glyph) == "W"
        assert len(glyph) == 1
        assert not wide or (kind == "done" and indent == 0), f"{kind} uses a wide marker"
    assert unicodedata.east_asian_width(ui.KINDS["done"][0]) == "W"


# --- streams ----------------------------------------------------------------


def test_a_refusal_goes_to_stderr(capsys):
    ui.err("no")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == "✗ no"


def test_everything_else_goes_to_stdout(capsys):
    ui.ok("yes")
    assert capsys.readouterr().out.strip() == "✓ yes"


# --- paths ------------------------------------------------------------------


def test_home_collapses_to_a_tilde(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    assert ui.path(tmp_path / "dev" / "api") == os.path.join("~", "dev", "api")
    assert ui.path(tmp_path) == "~"


def test_a_path_outside_home_is_left_alone(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    assert ui.path("/opt/homebrew/bin") == "/opt/homebrew/bin"


# --- capped name lists ------------------------------------------------------


def test_a_short_list_is_named():
    assert ui.names_or_count(["a", "b"], "skill") == "a, b"


def test_a_long_list_becomes_a_count():
    names = [str(n) for n in range(ui.NAME_LIMIT + 1)]
    assert ui.names_or_count(names, "skill") == f"{len(names)} skills"


def test_the_limit_itself_is_still_named():
    names = [str(n) for n in range(ui.NAME_LIMIT)]
    assert ui.names_or_count(names, "skill") == ", ".join(names)
