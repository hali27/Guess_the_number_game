"""Preserve starter assertions and add regression/edge-case coverage."""
import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_winning_guess():
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    result = check_guess(40, 50)
    assert result == "Too Low"


@pytest.mark.parametrize("guess,secret,expected", [
    (9, 50, "Too Low"), (100, 50, "Too High"),
    (1, 1, "Win"), (100, 100, "Win"),
])
def test_numeric_comparison(guess, secret, expected):
    assert check_guess(guess, secret) == expected


@pytest.mark.parametrize("raw,expected", [("50", 50), (" 9 ", 9), ("-3", -3)])
def test_parse_integer(raw, expected):
    assert parse_guess(raw) == (True, expected, None)


@pytest.mark.parametrize("raw", [None, "", "   ", "abc", "4.9", "50.0", "nan", "inf"])
def test_invalid_input(raw):
    ok, value, error = parse_guess(raw)
    assert not ok
    assert value is None
    assert error


@pytest.mark.parametrize("difficulty,expected", [
    ("Easy", (1, 20)), ("Normal", (1, 100)),
    ("Hard", (1, 50)), ("Unknown", (1, 100)),
])
def test_ranges(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
def test_wrong_guesses_always_lose_five_points(outcome, attempt):
    assert update_score(20, outcome, attempt) == 15


@pytest.mark.parametrize("attempt,award", [(1, 100), (2, 90), (3, 80), (10, 10), (20, 10)])
def test_win_award(attempt, award):
    assert update_score(5, "Win", attempt) == 5 + award


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(25, "Unknown", 1) == 25
