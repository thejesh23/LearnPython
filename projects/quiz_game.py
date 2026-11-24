"""Project: a multiple-choice quiz game.

You build it in four steps:

    1. questions as data   a plain list of dicts turned into Question objects,
                           so adding a question never means touching code
    2. scoring             ask each question through a function you pass in,
                           with a bonus for a streak of right answers
    3. shuffling           mix up question and choice order with a seeded
                           random.Random, so a given seed always gives the
                           same game (handy for tests and for this demo)
    4. playing             a scripted run by default; `python quiz_game.py
                           --play` asks you for real

Passing the "ask" function in (instead of calling input() inside the game) is
what makes the game testable: tests and the demo hand it canned answers.

Uses:
    05_control_flow        loops, conditionals
    06_functions           functions as arguments
    07_collections         lists, dicts, zip
    09_classes             dataclasses
    13_standard_library    random with a seed
"""

from dataclasses import dataclass


QUESTIONS = [
    {"prompt": "Which keyword defines a function?",
     "choices": ["func", "def", "lambda", "fn"], "answer": "def"},
    {"prompt": "What does len('hello') return?",
     "choices": ["4", "5", "6", "an error"], "answer": "5"},
    {"prompt": "Which type is immutable?",
     "choices": ["list", "dict", "set", "tuple"], "answer": "tuple"},
    {"prompt": "What is 7 // 2?",
     "choices": ["3", "3.5", "4", "1"], "answer": "3"},
    {"prompt": "Which module reads JSON?",
     "choices": ["csv", "pickle", "json", "toml"], "answer": "json"},
]

LETTERS = "abcd"


@dataclass
class Question:
    prompt: str
    choices: list[str]
    answer: str

    def is_correct(self, reply: str) -> bool:
        # Accept either the letter ("b") or the text ("def"), any case.
        reply = reply.strip().lower()
        if len(reply) == 1 and reply in LETTERS[: len(self.choices)]:
            reply = self.choices[LETTERS.index(reply)].lower()
        return reply == self.answer.lower()

    def render(self) -> str:
        lines = [self.prompt]
        for letter, choice in zip(LETTERS, self.choices):
            lines.append(f"   {letter}) {choice}")
        return "\n".join(lines)


def load_questions(data: list[dict]) -> list[Question]:
    questions = [Question(**item) for item in data]
    for q in questions:
        if q.answer not in q.choices:  # catch typos in the data early
            raise ValueError(f"answer {q.answer!r} is not a choice: {q.prompt}")
    return questions


def questions_demo() -> None:
    first = load_questions(QUESTIONS)[0]
    print(first.render())
    for reply in ["b", "DEF", "a", "  def "]:
        print(f"reply {reply!r:8} correct: {first.is_correct(reply)}")


def main() -> None:
    questions_demo()


if __name__ == "__main__":
    main()
