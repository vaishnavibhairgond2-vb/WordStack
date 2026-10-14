# WordStack

A Wordle-style terminal word game written in Python as a Data Structures & Algorithms mini project.

## How to play
```bash
python game.py
```
Guess the hidden 5-letter word in 6 tries. Green = right letter, right spot. Yellow = right letter, wrong spot. Gray = not in the word.

Commands: `undo` (-5 points), `hint` (-10 points), `quit`.

## Data structures used
| Structure | Where | Why |
|---|---|---|
| Hash set | `WORD_SET` | O(1) validation of guesses |
| Hash map | `Counter` in `score_guess`, keyboard status, revealed hints | Correct handling of repeated letters, O(1) lookups |
| Stack (linked list) | `GuessStack` | Guess history; `undo` pops the latest guess (LIFO) |

## Complexity
- `push`, `pop`, `peek`: O(1)
- `score_guess`: O(n) for word length n
- Word validation: O(1) average

## Requirements
Python 3.8+. No external libraries.
