"""Exercise actual app callbacks and rendered output with Streamlit AppTest."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def new_app(secret=50):
    app = AppTest.from_file(APP).run()
    assert not app.exception
    app.session_state.secret = secret
    return app


def guess(app, text):
    app.text_input(key="guess_input").set_value(text)
    app.button(key="submit").click().run()
    assert not app.exception
    return app


def test_initial_attempts_and_range():
    app = new_app()
    assert app.session_state.attempts == 0
    assert "Attempts left: 8" in app.info[0].value
    assert "between 1 and 100" in app.info[0].value


def test_demo_walkthrough():
    app = new_app(50)
    guess(app, "40")
    assert "Go HIGHER" in app.warning[0].value
    assert app.session_state.score == -5
    assert "Attempts left: 7" in app.info[0].value
    guess(app, "70")
    assert "Go LOWER" in app.warning[0].value
    assert app.session_state.score == -10
    guess(app, "50")
    assert app.session_state.status == "won"
    assert app.session_state.score == 70
    assert app.session_state.history == [40, 70, 50]
    assert "Total score: 70" in app.success[0].value
    assert app.button(key="submit").disabled


def test_numeric_comparison_on_second_attempt():
    app = new_app(50)
    guess(app, "60")
    guess(app, "9")
    assert "Too Low" in app.warning[0].value


@pytest.mark.parametrize("raw", ["", "abc", "4.9", "-5", "0", "101", "9" * 100])
def test_invalid_or_out_of_range_does_not_use_attempt(raw):
    app = new_app()
    guess(app, raw)
    assert len(app.error) == 1
    assert app.session_state.attempts == 0
    assert app.session_state.score == 0
    assert app.session_state.history == []
    assert app.session_state.secret == 50


@pytest.mark.parametrize("difficulty,high,limit", [("Easy", 20, 6), ("Normal", 100, 8), ("Hard", 50, 5)])
def test_loss_at_exact_limit_and_restart(difficulty, high, limit):
    app = new_app()
    app.selectbox(key="difficulty").select(difficulty).run()
    app.session_state.secret = high
    for _ in range(limit - 1):
        guess(app, "1")
        assert app.session_state.status == "playing"
    guess(app, "1")
    assert app.session_state.status == "lost"
    assert "Attempts left: 0" in app.info[0].value
    assert app.session_state.score == -5 * limit
    app.button(key="new_game").click().run()
    assert not app.exception
    assert app.session_state.status == "playing"
    assert app.session_state.attempts == 0
    assert app.session_state.score == -5 * limit
    assert app.session_state.history == []
    assert 1 <= app.session_state.secret <= high
    assert app.text_input(key="guess_input").value == ""
    assert not app.button(key="submit").disabled


def test_restart_after_win():
    app = new_app(50)
    guess(app, "50")
    assert app.session_state.status == "won"
    app.button(key="new_game").click().run()
    assert not app.exception
    assert app.session_state.status == "playing"
    assert app.session_state.score == 100
    assert app.session_state.attempts == 0
    assert app.session_state.history == []
    assert not app.success


def test_difficulty_change_resets_round():
    app = new_app(99)
    guess(app, "40")
    app.selectbox(key="difficulty").select("Easy").run()
    assert not app.exception
    assert 1 <= app.session_state.secret <= 20
    assert app.session_state.attempts == 0
    assert app.session_state.score == -5
    assert app.session_state.history == []
    assert "between 1 and 20" in app.info[0].value
    assert "Attempts left: 6" in app.info[0].value


def test_secret_stays_fixed_and_hint_toggle_does_not_consume_attempt():
    app = new_app(50)
    guess(app, "40")
    app.checkbox(key="show_hint").uncheck().run()
    assert app.session_state.secret == 50
    assert app.session_state.attempts == 1
    assert not app.warning
    guess(app, "50")
    assert app.session_state.status == "won"
    assert app.success


def test_correct_guess_on_last_attempt_wins():
    app = new_app(50)
    for _ in range(7):
        guess(app, "1")
    guess(app, "50")
    assert app.session_state.status == "won"
    assert "Attempts left: 0" in app.info[0].value


def test_total_accumulates_across_two_games():
    app = new_app(50)
    guess(app, "50")
    assert app.session_state.score == 100
    app.button(key="new_game").click().run()
    app.session_state.secret = 20
    guess(app, "10")
    assert app.session_state.score == 95
    guess(app, "20")
    assert app.session_state.score == 185
    assert app.session_state.attempts == 2
    assert app.session_state.history == [10, 20]
    app.checkbox(key="show_hint").uncheck().run()
    assert app.session_state.score == 185


def test_restart_midgame_keeps_negative_score():
    app = new_app(50)
    guess(app, "40")
    assert app.session_state.score == -5
    app.button(key="new_game").click().run()
    assert not app.exception
    assert app.session_state.score == -5
    assert app.session_state.attempts == 0
    assert app.session_state.history == []
    assert app.session_state.status == "playing"
