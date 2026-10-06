
## 1. What was broken when you started?

The code had backwards hints, inconsistent scoring, and a New Game button that did not
fully reset the round.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|---|---|---|---|
| `check_guess(60, 50)` | Too High, go lower | Tells player to go higher | `('Too High', '📈 Go HIGHER!')` |
| `check_guess(9, "50")` | Too Low numerically | Compares strings and says Too High | `('Too High', '📈 Go HIGHER!')` |
| `parse_guess("4.9")` | Reject decimals | Accepts integer 4 | `(True, 4, None)` |
| `update_score(0, "Too High", 2)` | Wrong guesses lose 5 points | Adds 5 points | `5` |
| New Game after winning | Status becomes playing | Source leaves status won | Source inspection; no console error claimed |

## 2. How did you use AI as a teammate?

I used ChatGPT to help repair it. One correct suggestion was to return an outcome string from `check_guess`, because that
matches the three starter tests; I verified those assertions by running the
full test suite on my Mac. I did not accept the suggestion to reset the score
to zero with every new game, because I wanted to keep the total across games.


## 3. Debugging and testing your fixes

I  checked that entering a float showed an error without using an attempt, entering the secret number won the game, and New
Game started another playable round. 
ChatGPT helped generate the test set 

## 4. What did you learn about Streamlit and state?

Streamlit reruns the script when someone interacts with a widget. Session
state keeps values such as the secret and attempt count between those reruns
within the same session. 

## 5. Looking ahead: your developer habits

A habit I want to use again is reproducing a bug with a specific input before
changing the code. 