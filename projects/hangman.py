"""Hangman: the word-guessing game, plus a computer player.

You build the game in layers that stay separate: a class that knows the rules
and the state of one game (and never prints), a function that draws the
gallows, a loop that feeds guesses into the game, and finally two sources of
guesses: a computer player that reasons about the word list, and you at the
keyboard.

Keeping the rules apart from input and output is what makes this testable:
the same `play()` loop runs a scripted game in the demo and a real one when
you type.

    python projects/hangman.py          scripted games only
    python projects/hangman.py --play   the same, then a game for you

Uses:
    04_strings             str.format with named fields, join, isalpha
    05_control_flow        while and for loops, match on an enum
    06_functions           keyword-only options, functions as values
    07_collections         sets of guessed letters, list filtering
    08_iterators           generators that produce guesses one at a time
    09_classes             a class with properties, an Enum for outcomes
    11_errors              ValueError for bad input, EOFError from input()
    13_standard_library    random, collections.Counter
"""

import random
import sys
from collections import Counter
from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from enum import Enum


class Outcome(Enum):
    HIT = "hit"
    MISS = "miss"
    REPEAT = "already guessed"


class Hangman:
    """The rules and state of one game. It never prints or reads input."""

    def __init__(self, word: str, max_misses: int = 6) -> None:
        if not (word.isascii() and word.isalpha()):
            raise ValueError(f"the word must be letters a-z, got {word!r}")
        self.word = word.lower()
        self.max_misses = max_misses
        self.guessed: set[str] = set()
        self.misses: list[str] = []  # a list keeps the order they were made

    @property
    def masked(self) -> str:
        return " ".join(c if c in self.guessed else "_" for c in self.word)

    @property
    def won(self) -> bool:
        # Every letter of the word is in the guessed set: a subset test.
        return set(self.word) <= self.guessed

    @property
    def lost(self) -> bool:
        return len(self.misses) >= self.max_misses

    @property
    def over(self) -> bool:
        return self.won or self.lost

    def guess(self, text: str) -> Outcome:
        if self.over:
            raise RuntimeError("the game is already over")
        letter = text.strip().lower()
        if len(letter) != 1 or not (letter.isascii() and letter.isalpha()):
            raise ValueError("guess a single letter a-z")
        if letter in self.guessed:
            return Outcome.REPEAT  # not a mistake: no miss is counted
        self.guessed.add(letter)
        if letter in self.word:
            return Outcome.HIT
        self.misses.append(letter)
        return Outcome.MISS


def game_state_demo() -> None:
    print("== stage 1: the game state ==")
    game = Hangman("python")
    print(f"start:      {game.masked}")
    for text in ["p", "z", "Y", "p"]:
        outcome = game.guess(text)
        shown = f"guess {text!r}:"
        print(f"{shown:<12}{outcome.value:<16} {game.masked}  misses {game.misses}")
    try:
        game.guess("7")
    except ValueError as exc:
        print(f"{"guess '7':":<12}ValueError: {exc}")
    print(f"won {game.won}, lost {game.lost}, over {game.over}")


# One template, with a named field for every body part. Missing parts are
# filled with spaces so the picture keeps its shape.
GALLOWS = r"""
  +---+
  |   |
  {head}   |
 {left_arm}{body}{right_arm}  |
 {left_leg} {right_leg}  |
      |
=========""".strip("\n")

# The order body parts appear in, one per miss, and how each is drawn.
BODY = {
    "head": "O",
    "body": "|",
    "left_arm": "/",
    "right_arm": "\\",
    "left_leg": "/",
    "right_leg": "\\",
}


def draw(misses: int) -> str:
    parts = {
        name: char if i < misses else " "
        for i, (name, char) in enumerate(BODY.items())
    }
    return GALLOWS.format(**parts)


def render(game: Hangman) -> str:
    left = game.max_misses - len(game.misses)
    return (
        f"{draw(len(game.misses))}\n"
        f"word:   {game.masked}\n"
        f"misses: {' '.join(game.misses) or '-'}  ({left} left)"
    )


def art_demo() -> None:
    print("== stage 2: drawing the gallows ==")
    frames = [draw(n).splitlines() for n in (0, 2, 4, 6)]
    # Print four frames side by side: zip takes one row from each frame.
    print("    ".join(f"{n} misses " for n in (0, 2, 4, 6)).rstrip())
    for rows in zip(*frames):
        print("    ".join(f"{row:<9}" for row in rows).rstrip())


def play(
    game: Hangman,
    guesses: Iterable[str],
    *,
    verbose: bool = False,
    say: Callable[[str], None] = print,
) -> bool:
    """Feed guesses into the game until it ends. Returns True for a win.

    `guesses` can be any iterable: a list for a scripted game, or a
    generator that asks a person or a computer for each next letter.
    """
    if verbose:
        say(render(game))
    for text in guesses:
        try:
            outcome = game.guess(text)
        except ValueError as exc:
            say(f"{text!r}: {exc}")
            continue
        match outcome:
            case Outcome.HIT:
                note = f"yes, {game.word.count(text.strip().lower())} found"
            case Outcome.MISS:
                note = "no"
            case Outcome.REPEAT:
                note = "already tried"
        say(f"{text!r}: {note:<14} {game.masked}")
        if verbose and outcome is Outcome.MISS:
            say(draw(len(game.misses)))
        if game.over:
            break
    say(render(game))
    if game.won:
        say(f"You won with {len(game.misses)} misses.")
    elif game.lost:
        say(f"Hanged. The word was {game.word!r}.")
    else:
        say("Stopped before the game ended.")
    return game.won


def scripted_game_demo() -> None:
    print("== stage 3: a scripted game ==")
    # Guessing vowels first is a poor plan against a word with no vowels.
    guesses = ["a", "e", "7", "i", "o", "u", "E", "y", "s"]
    won = play(Hangman("rhythm"), guesses)
    print(f"play() returned {won}")


WORDS = [
    "python", "string", "module", "lambda", "syntax", "method", "object",
    "return", "import", "assert", "global", "format", "socket", "thread",
    "binary", "cursor", "parser", "vector", "buffer", "branch", "commit",
    "keyword", "boolean", "integer", "package", "closure", "default",
    "variable", "function", "iterator", "generator", "decorator", "exception",
]


def could_be(word: str, game: Hangman) -> bool:
    """Is `word` still possible, given what the game has shown so far?"""
    # Only use what a player can see: the masked word and the guesses.
    pattern = game.masked.split(" ")
    if len(word) != len(pattern):
        return False
    for shown, letter in zip(pattern, word):
        if shown != "_" and shown != letter:
            return False  # a revealed letter does not match
        if shown == "_" and letter in game.guessed:
            return False  # a guessed letter would have been revealed here
    return True


def computer_guesses(game: Hangman, words: list[str]) -> Iterator[str]:
    """Yield the best next letter, looking at the game afresh each time.

    A generator pauses at each yield. play() makes its guess with that
    letter, and only then asks for the next one, so every guess here sees
    the result of the previous one.
    """
    while not game.over:
        candidates = [w for w in words if could_be(w, game)]
        # Count each letter once per candidate word it appears in.
        votes = Counter(c for w in candidates for c in set(w) - game.guessed)
        if not votes:
            return
        letter, count = votes.most_common(1)[0]
        if len(candidates) == 1:
            print(f"  (only {candidates[0]!r} fits)")
        else:
            print(f"  ({len(candidates)} words fit; {letter!r} is in {count} of them)")
        yield letter


def computer_player_demo() -> None:
    print("== stage 4: a computer player ==")
    rng = random.Random(3)  # seeded, so the demo picks the same word each run
    word = rng.choice(WORDS)
    game = Hangman(word)
    # The generator gets the same game object that play() updates.
    play(game, computer_guesses(game, WORDS))


def typed_guesses() -> Iterator[str]:
    """Ask the person at the keyboard, one guess per loop of play()."""
    while True:
        try:
            yield input("your guess: ")
        except EOFError:  # Ctrl-D (or Ctrl-Z on Windows) ends the game
            print()
            return


def play_yourself_demo() -> None:
    print("== stage 5: your turn ==")
    if "--play" not in sys.argv:
        # Never wait for input unless asked: scripts and CI have no keyboard.
        print("run with --play to play a game yourself")
        return
    word = random.choice(WORDS)  # unseeded: a different word each time
    play(Hangman(word), typed_guesses(), verbose=True)


def main() -> None:
    game_state_demo()
    print()
    art_demo()
    print()
    scripted_game_demo()
    print()
    computer_player_demo()
    print()
    play_yourself_demo()


if __name__ == "__main__":
    main()
