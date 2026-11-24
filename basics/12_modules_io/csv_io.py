"""Reading and writing CSV files with the `csv` module.

CSV looks simple enough to split on commas by hand, until a field contains a
comma, a quote or a line break: "Smith, Jr." must be written in quotes, and a
quote inside a field is doubled. The csv module handles all of that.

    csv.writer / csv.reader          rows as lists
    csv.DictWriter / csv.DictReader  rows as dicts keyed by the header line

Open CSV files with newline="" so the module controls line endings itself.
Every value comes back as a string; converting types is up to you.
"""

import csv
import tempfile
from pathlib import Path


ROWS = [
    ["name", "city", "score"],
    ["Ana", "Lisbon", "91"],
    ["Bo Smith, Jr.", "New York", "78"],   # a comma inside a field
    ['Cy "The Fox"', "Oslo", "85"],        # quotes inside a field
]


def lists_demo() -> None:
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "scores.csv"
        with path.open("w", newline="") as f:
            csv.writer(f).writerows(ROWS)

        print("the file on disk:")
        print(path.read_text().rstrip())

        with path.open(newline="") as f:
            rows = list(csv.reader(f))
        print(f"read back identical: {rows == ROWS}")
        # A naive split breaks on the comma inside "Bo Smith, Jr.".
        naive = path.read_text().splitlines()[2].split(",")
        print(f"naive split of row 2: {naive}")


def main() -> None:
    lists_demo()


if __name__ == "__main__":
    main()
