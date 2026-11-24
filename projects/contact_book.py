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

import re
from dataclasses import dataclass


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


def main() -> None:
    contact_demo()
    print()
    book_demo()


if __name__ == "__main__":
    main()
