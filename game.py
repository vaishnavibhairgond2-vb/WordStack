"""
WordStack - a Wordle-style terminal word game built for a DSA mini project.

Data structures used
--------------------
1. Hash Set  : WORD_SET        -> O(1) check that a guess is a valid word
2. Hash Map  : Counter / dict  -> letter frequency for correct green/yellow
                                  feedback, keyboard status, revealed hints
3. Stack     : GuessStack      -> guess history; `undo` pops the last guess
                                  (implemented from scratch with linked nodes)
"""

import random
from collections import Counter

WORDS = [
    "array", "graph", "queue", "stack", "logic", "merge", "class", "token",
    "index", "float", "while", "break", "yield", "scope", "parse", "query",
    "cache", "apple", "brain", "chair", "dance", "eagle", "flame", "grape",
    "house", "knife", "lemon", "mango", "night", "ocean", "pilot", "queen",
    "river", "table", "voice", "water", "youth", "zebra", "light", "music",
    "plant", "smile", "tiger", "bread", "cloud", "dream", "earth", "heart",
]

WORD_SET = set(WORDS)          # hash set -> O(1) membership test
WORD_LENGTH = 5
MAX_ATTEMPTS = 6

GREEN, YELLOW, GRAY, RESET = "\033[42;30m", "\033[43;30m", "\033[100;97m", "\033[0m"
COLORS = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}
RANK = {"gray": 0, "yellow": 1, "green": 2}


# ---------------------------------------------------------------- Stack (DSA)
class _Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class GuessStack:
    """LIFO stack implemented with a singly linked list."""

    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, value):          # O(1)
        self._top = _Node(value, self._top)
        self._size += 1

    def pop(self):                  # O(1)
        if self.is_empty():
            raise IndexError("pop from empty stack")
        value = self._top.value
        self._top = self._top.next
        self._size -= 1
        return value

    def peek(self):                 # O(1)
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._top.value

    def is_empty(self):
        return self._top is None

    def __len__(self):
        return self._size

    def __iter__(self):             # top -> bottom
        node = self._top
        while node:
            yield node.value
            node = node.next


# ------------------------------------------------------------------ Game logic
def score_guess(secret, guess):
    """Return a list of 'green' / 'yellow' / 'gray' for each letter.

    Uses a hash map (Counter) of the secret's unmatched letters so that
    repeated letters are handled correctly.
    """
    result = ["gray"] * WORD_LENGTH
    remaining = Counter()
    for i, (s, g) in enumerate(zip(secret, guess)):
        if s == g:
            result[i] = "green"
        else:
            remaining[s] += 1
    for i, g in enumerate(guess):
        if result[i] != "green" and remaining[g] > 0:
            result[i] = "yellow"
            remaining[g] -= 1
    return result


def render(word, result):
    return "".join(f"{COLORS[c]} {ch.upper()} {RESET}" for ch, c in zip(word, result))


def keyboard_status(history):
    """Hash map letter -> best status seen so far, rebuilt from the stack."""
    status = {}
    for word, result in history:
        for ch, c in zip(word, result):
            if ch not in status or RANK[c] > RANK[status[ch]]:
                status[ch] = c
    return status


def print_board(history):
    print()
    for word, result in reversed(list(history)):   # oldest guess first
        print("   " + render(word, result))
    for _ in range(MAX_ATTEMPTS - len(history)):
        print("   " + "".join(f"{GRAY} _ {RESET}" for _ in range(WORD_LENGTH)))
    status = keyboard_status(history)
    if status:
        line = " ".join(f"{COLORS[status[c]]}{c.upper()}{RESET}" if c in status
                        else c.upper() for c in "abcdefghijklmnopqrstuvwxyz")
        print("\n   " + line)
    print()


def show_hints(revealed):
    pattern = " ".join(revealed.get(i, "_").upper() for i in range(WORD_LENGTH))
    print(f"   Hints: {pattern}")


def play():
    secret = random.choice(WORDS)
    history = GuessStack()
    revealed = {}                 # hash map: position -> letter
    undos = hints = 0

    print("\n=== WORDSTACK ===")
    print(f"Guess the {WORD_LENGTH}-letter word in {MAX_ATTEMPTS} tries.")
    print("Commands: 'undo' (-5 pts), 'hint' (-10 pts), 'quit'\n")
    print_board(history)

    while len(history) < MAX_ATTEMPTS:
        cmd = input(f"Guess {len(history) + 1}/{MAX_ATTEMPTS} > ").strip().lower()

        if cmd == "quit":
            print(f"The word was: {secret.upper()}")
            return
        if cmd == "undo":
            if history.is_empty():
                print("Nothing to undo.")
                continue
            word, _ = history.pop()
            undos += 1
            print(f"Removed '{word.upper()}'.")
            print_board(history)
            continue
        if cmd == "hint":
            hidden = [i for i in range(WORD_LENGTH) if i not in revealed]
            if not hidden:
                print("All letters already revealed.")
                continue
            pos = random.choice(hidden)
            revealed[pos] = secret[pos]
            hints += 1
            show_hints(revealed)
            continue
        if len(cmd) != WORD_LENGTH or not cmd.isalpha():
            print(f"Enter a {WORD_LENGTH}-letter word.")
            continue
        if cmd not in WORD_SET:
            print("Not in the word list.")
            continue

        result = score_guess(secret, cmd)
        history.push((cmd, result))
        print_board(history)

        if cmd == secret:
            points = max(0, 100 - 10 * (len(history) - 1) - 5 * undos - 10 * hints)
            print(f"You won in {len(history)} guess(es)! Score: {points}")
            return

    print(f"Out of tries! The word was: {secret.upper()}")


if __name__ == "__main__":
    while True:
        play()
        if input("\nPlay again? (y/n) > ").strip().lower() != "y":
            print("Thanks for playing!")
            break
