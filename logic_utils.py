"""Pure game logic, independent of Streamlit."""


def get_range_for_difficulty(difficulty: str):
    """Return the starter's inclusive range; unknown names use Normal."""
    ranges = {"Easy": (1, 20), "Normal": (1, 100), "Hard": (1, 50)}
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """Return (ok, integer or None, error or None) without truncating decimals."""
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."
    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number."
    return True, value, None


def check_guess(guess: int, secret: int):
    """Compare two integers and return an outcome string, as starter tests expect."""
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Apply a win award or wrong-guess penalty; attempt numbers start at 1."""
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points
    if outcome in ("Too High", "Too Low"):
        return current_score - 5
    return current_score
