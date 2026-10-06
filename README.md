# Number Guessing Game

A Streamlit number-guessing game. You enter whole numbers, follow the higher/lower hints, and try to win before you run out of attempts.

## Setup

You need Python 3.10 or newer. The files need to be named exactly `logic_utils.py`, `requirements.txt`, and `.gitignore` (with the dot).

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell, activate with `.\.venv\Scripts\Activate.ps1` instead.

## Rules

| Difficulty | Range (inclusive) | Attempts |
|------------|-------------------|----------|
| Easy       | 1–20              | 6        |
| Normal     | 1–100             | 8        |
| Hard       | 1–50              | 5        |

I kept the difficulty ranges that came with the project.

- Invalid inputs and out-of-range numbers don't use up an attempt.
- Each wrong (valid) guess costs 5 points.
- A win gives you `max(10, 100 - 10 * (attempt_number - 1))` points on top of your current score, so winning on the first try is worth 100.
- Scores can go negative.
- The instructions didn't give a scoring formula, so I chose these numbers myself.
- New Game keeps your total score but resets everything else for the round. Changing difficulty also keeps the total.
- The total lives in session state, so it isn't saved to disk and disappears when the session ends.
- The new secret number can be the same as the last one by chance. It stays fixed for the whole round.

## Document Your Experience

### Bugs I found

- The hints pointed the wrong way (it told you to go lower when you needed to go higher, and the reverse).
- On even attempts the secret turned into a string, so comparisons were alphabetical instead of numeric (for example, "9" > "50").
- A decimal like 4.9 was quietly turned into 4.
- Attempts started at 1, and invalid guesses still used up attempts.
- Some wrong guesses that were too high added points instead of taking them away.
- New Game didn't reset the status or history, and it ignored the difficulty. My first fix also reset the score, but I later decided I wanted a running total instead.
- Changing difficulty kept leftover state from the previous round.
- The displayed range was always 1–100.
- The helper function returned a tuple, but the tests I was given expected a string.

### What I changed

- I moved the pure logic into `logic_utils.py`.
- `check_guess` now returns the string the original tests expect, and `app.py` turns that into the right hint.
- Input is checked before attempts are counted.
- Callbacks update state before Streamlit draws the counters, and reset sets up all the round fields the same way every time.
- Submit is disabled once the round is over.
- The UI shows the real range for the chosen difficulty and the current score.

## Demo Walkthrough

This example is also covered by `test_demo_walkthrough`. In normal play the secret is random, but the test sets it to 50.

1. Start on Normal with secret 50, 8 attempts, and a score of 0.
2. Enter 40. The game says "Too Low! Go HIGHER!". 7 attempts left, score is -5.
3. Enter 70. The game says "Too High! Go LOWER!". 6 attempts left, score is -10.
4. Enter 50. You win on the third valid attempt. The award is 80 points, so the final score is 70.
5. Submit is now disabled. Clicking New Game keeps the total at 70, resets attempts, history, and status, clears the input, and picks a new secret in the current range. Future wins and penalties change that same total.

## Test Results

Run `python -m pytest -q` or `pytest`.

On the current version (55 tests), the output was:

```
.......................................................                  [100%]
55 passed in 3.94s
```

I didn't change the three outcome assertions that came with the project. I added tests for numeric comparisons, input parsing, difficulty ranges, and scoring. I also used Streamlit's AppTest to cover callbacks, both hint directions, the sample game, the exact attempt limits, winning on the last attempt, restarting after a win or loss, and changing difficulty. The score tests check that positive and negative totals carry over, and that awards add up correctly across two games without being counted twice on reruns.

Environment for that run: Python 3.12, Streamlit 1.60.0, pytest 9.1.1, Altair 4.2.2. The Streamlit server also started and its health endpoint returned HTTP 200.

On my own computer, I ran the previous version's 53 tests (they passed in 3.25 seconds) and checked three things by hand: decimals get rejected, a winning guess works, and restart works.

**Still to do:** run the 55 tests locally and check by hand that the score carries over between games.

## Stretch Features

Challenge 1: I added automated edge-case tests for negative numbers, decimals, and very large integers. The app rejects all three without changing the score, attempts, history, or secret. I'm not claiming any of the other optional challenges.

## How I Used AI

I used an AI assistant to help debug the game, write the tests, and draft some documentation.

## Sources

- Streamlit Session State: explains how state persists across reruns and the order callbacks run in.
- Streamlit AppTest: the app-testing API I used.
- pytest parametrization: how to run one test over many inputs.


