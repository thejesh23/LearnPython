"""Project: a contact book with search and CSV import/export.

You build it in four steps:

    1. a Contact      a frozen dataclass that checks its own fields, so a bad
                      email can never get into the book
    2. the book       add, remove and search contacts, refuse duplicates
    3. CSV            export to a spreadsheet-friendly file and import one back,
                      collecting bad rows instead of stopping at the first
    4. a session      import a messy file, search it, print a table

The main idea is *validate at the edge*: data is checked once, when a Contact
is created, and every other part of the program can then trust it.

Uses:
    04_strings             f-string alignment, str methods
    07_collections         dicts, sorting with a key
    09_classes             dataclasses, __post_init__
    11_errors              custom exceptions
    12_modules_io          csv, pathlib, temp files
    13_standard_library    regular expressions
"""

import csv
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


class ValidationError(ValueError):
    """A field value that a Contact refuses to hold."""


# Good enough to catch typos; full email validation is famously hard.
EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", re.IGNORECASE)


@dataclass(frozen=True)
class Contact:
    name: str
    email: str
    phone: str = ""
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # frozen=True blocks normal assignment, so tidy fields this way.
        object.__setattr__(self, "name", " ".join(self.name.split()))
        object.__setattr__(self, "email", self.email.strip().lower())
        if not self.name:
            raise ValidationError("name is empty")
        if not EMAIL.fullmatch(self.email):
            raise ValidationError(f"bad email {self.email!r}")
        digits = re.sub(r"[\s()+-]", "", self.phone)
        if self.phone and not (digits.isdigit() and 7 <= len(digits) <= 15):
            raise ValidationError(f"bad phone {self.phone!r}")


def contact_demo() -> None:
    ada = Contact("  Ada   Lovelace ", "ADA@Example.com", "+44 20 7946 0000")
    print(ada)
    for name, email, phone in [("", "x@y.io", ""), ("Bo", "bo@nowhere", ""),
                               ("Cy", "cy@site.org", "call me")]:
        try:
            Contact(name, email, phone)
        except ValidationError as exc:
            print(f"rejected: {exc}")


class ContactBook:
    def __init__(self) -> None:
        # Keyed by email: two contacts may share a name, never an address.
        self._by_email: dict[str, Contact] = {}

    def __len__(self) -> int:
        return len(self._by_email)

    def add(self, contact: Contact) -> None:
        if contact.email in self._by_email:
            raise ValidationError(f"{contact.email} is already in the book")
        self._by_email[contact.email] = contact

    def remove(self, email: str) -> Contact:
        return self._by_email.pop(email.lower())

    def all(self) -> list[Contact]:
        return sorted(self._by_email.values(), key=lambda c: c.name.lower())

    def search(self, text: str) -> list[Contact]:
        needle = text.lower()
        return [c for c in self.all()
                if needle in c.name.lower() or needle in c.email
                or needle in (t.lower() for t in c.tags)]


def book_demo() -> None:
    book = ContactBook()
    book.add(Contact("Grace Hopper", "grace@navy.mil", tags=("work",)))
    book.add(Contact("Alan Turing", "alan@bletchley.uk", tags=("work", "chess")))
    book.add(Contact("Linus", "linus@example.org", tags=("friend",)))
    try:
        book.add(Contact("Grace H.", "Grace@navy.mil"))
    except ValidationError as exc:
        print(f"rejected: {exc}")
    print(f"{len(book)} contacts: {[c.name for c in book.all()]}")
    for query in ["work", "LIN", "nobody"]:
        print(f"search {query!r}: {[c.name for c in book.search(query)]}")


FIELDS = ["name", "email", "phone", "tags"]


def export_csv(book: ContactBook, path: Path) -> None:
    # newline="" lets the csv module choose line endings itself.
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for c in book.all():
            writer.writerow({"name": c.name, "email": c.email, "phone": c.phone,
                             "tags": ";".join(c.tags)})


def import_csv(book: ContactBook, path: Path) -> list[str]:
    """Add every good row; return one message per row that was skipped."""
    problems = []
    with path.open(newline="") as f:
        # start=2 because line 1 is the header.
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            try:
                tags = tuple(t.strip() for t in (row.get("tags") or "").split(";"))
                contact = Contact(row.get("name") or "", row.get("email") or "",
                                  row.get("phone") or "", tuple(t for t in tags if t))
                book.add(contact)
            except ValidationError as exc:
                problems.append(f"line {line_no}: {exc}")
    return problems


def csv_demo() -> None:
    book = ContactBook()
    book.add(Contact("Margaret Hamilton", "margaret@nasa.gov", "555 0100 123"))
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "contacts.csv"
        export_csv(book, path)
        print("exported contacts.csv:")
        for line in path.read_text().splitlines():
            print(f"  {line}")
        copy = ContactBook()
        print(f"re-import problems: {import_csv(copy, path)}")
        print(f"round trip equal: {copy.all() == book.all()}")


MESSY_CSV = """\
name,email,phone,tags
Ada Lovelace,ada@example.com,+44 20 7946 0000,math;friend
Katherine Johnson,KJ@nasa.gov,,math; work
,nobody@example.com,,
Dennis Ritchie,dmr@bell-labs,,work
Ken Thompson,ken@bell-labs.com,(555) 123-4567,work
Ada Lovelace,ADA@example.com,,
Barbara Liskov,barbara@mit.edu,12,
"""


def print_table(contacts: list[Contact]) -> None:
    print(f"{'Name':<18} {'Email':<20} {'Phone':<17} Tags")
    print("-" * 66)
    for c in contacts:
        print(f"{c.name:<18} {c.email:<20} {c.phone or '-':<17} "
              f"{', '.join(c.tags)}")


def session_demo() -> None:
    book = ContactBook()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "messy.csv"
        path.write_text(MESSY_CSV)
        problems = import_csv(book, path)
    print(f"imported {len(book)} contacts, skipped {len(problems)} rows:")
    for problem in problems:
        print(f"  {problem}")
    print()
    print_table(book.all())
    print()
    print("tagged 'math':")
    print_table(book.search("math"))


def main() -> None:
    contact_demo()
    print()
    book_demo()
    print()
    csv_demo()
    print()
    session_demo()


if __name__ == "__main__":
    main()
