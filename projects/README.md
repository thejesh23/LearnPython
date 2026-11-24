# Projects

Small but complete programs that pull many chapters together. Each one is a
single file you can read top to bottom and run with `python3 projects/<file>`.
By default each project plays a scripted demo, so you see it working at once.
The games also take `--play` for a real interactive session.

Every project was built up in a few commits, from the core idea to the
finished program, so `git log --follow projects/<file>` replays its
construction step by step.

Tackle them roughly in this order. "Ready after" is the last `basics/` chapter
the project relies on.

| # | Project | What you build | Ready after |
|---|---------|----------------|-------------|
| 1 | [`quiz_game.py`](quiz_game.py) | A multiple-choice quiz with scoring and streaks | 09 |
| 2 | [`text_adventure.py`](text_adventure.py) | A small text adventure: rooms, items, a `match`-based command parser | 09 |
| 3 | [`word_frequency_report.py`](word_frequency_report.py) | Which words a text leans on most, with a text bar chart | 13 |
| 4 | [`password_tools.py`](password_tools.py) | A secure password generator and a strength checker | 13 |
| 5 | [`hangman.py`](hangman.py) | Hangman, plus a computer player that narrows down the word list | 13 |
| 6 | [`contact_book.py`](contact_book.py) | A contact book with validation, search and CSV import/export | 13 |
| 7 | [`markdown_to_html.py`](markdown_to_html.py) | A mini Markdown to HTML converter | 13 |
| 8 | [`log_analyzer.py`](log_analyzer.py) | Turn thousands of web-server log lines into a short report | 13 |
| 9 | [`inventory_system.py`](inventory_system.py) | A shop inventory with stock movements, reports and its own tests | 14 |
| 10 | [`todo_cli.py`](todo_cli.py) | A to-do list you drive from the command line, stored as JSON | 17 |
| 11 | [`expense_tracker.py`](expense_tracker.py) | An expense tracker on SQLite with monthly reports | 18 |
| 12 | [`url_shortener.py`](url_shortener.py) | A URL shortener: short codes, a database and a tiny web server | 19 |

## How to get the most out of a project

1. Run it and read the output.
2. Read the module docstring: it lists the chapters the project draws on.
3. Read the code top to bottom. Each section matches one commit in its history.
4. Change something: add a command, a new report column, another game rule.
   Then run it again.
5. Rebuild it from scratch without looking, and compare.
