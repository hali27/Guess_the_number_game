"""Streamlit interface for the repaired guessing game."""
import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

ATTEMPT_LIMITS = {"Easy": 6, "Normal": 8, "Hard": 5}
HINTS = {
    "Too High": "📉 Too High! Go LOWER!",
    "Too Low": "📈 Too Low! Go HIGHER!",
}


def start_new_game():
    """Start a fresh round while keeping the session total score."""
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_outcome = None
    st.session_state.error = None
    st.session_state.guess_input = ""


def submit_guess():
    """Validate first; only valid guesses can change round progress."""
    if st.session_state.status != "playing":
        return
    ok, guess, error = parse_guess(st.session_state.guess_input)
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    if not ok:
        st.session_state.error = error
        return
    if not low <= guess <= high:
        st.session_state.error = f"Enter a number between {low} and {high}."
        return

    st.session_state.error = None
    st.session_state.attempts += 1
    outcome = check_guess(guess, st.session_state.secret)
    st.session_state.last_outcome = outcome
    st.session_state.history.append(guess)
    st.session_state.score = update_score(
        st.session_state.score, outcome, st.session_state.attempts
    )
    if outcome == "Win":
        st.session_state.status = "won"
    elif st.session_state.attempts >= ATTEMPT_LIMITS[st.session_state.difficulty]:
        st.session_state.status = "lost"


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("Guess the secret number before your attempts run out.")
st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox(
    "Difficulty", ["Easy", "Normal", "Hard"], index=1,
    key="difficulty", on_change=start_new_game,
)
if "secret" not in st.session_state:
    start_new_game()

low, high = get_range_for_difficulty(difficulty)
attempt_limit = ATTEMPT_LIMITS[difficulty]
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
st.subheader("Make a guess")
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)
st.write(f"Total score: {st.session_state.score}")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

finished = st.session_state.status != "playing"
st.text_input("Enter your guess:", key="guess_input", disabled=finished)
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Submit Guess 🚀", key="submit", on_click=submit_guess,
              disabled=finished)
with col2:
    st.button("New Game 🔁", key="new_game", on_click=start_new_game)
with col3:
    show_hint = st.checkbox("Show hint", value=True, key="show_hint")

if st.session_state.error:
    st.error(st.session_state.error)
elif st.session_state.status == "won":
    st.success(
        f"🎉 You won! The secret was {st.session_state.secret}. "
        f"Total score: {st.session_state.score}. Start a new game to play again."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}. Start a new game to try again."
    )
elif show_hint and st.session_state.last_outcome:
    st.warning(HINTS[st.session_state.last_outcome])

st.divider()
st.caption("Built with AI assistance and checked with automated tests.")
