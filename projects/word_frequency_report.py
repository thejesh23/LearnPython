"""Word frequency report: which words does a text lean on most?

You build a small text-analysis tool. It takes a passage, splits it into
words, counts them, drops the "glue" words that every English text is full of,
and prints a report with a bar chart drawn in plain text. The last stage reads
the texts from files and compares two of them.

The sample texts are public domain: Abraham Lincoln's Gettysburg Address
(1863) and the opening of Charles Dickens's "A Tale of Two Cities" (1859).

Uses:
    04_strings             casefold, join, f-string alignment and padding
    05_control_flow        for loops over words and lines
    06_functions           small single-purpose functions, default arguments
    07_collections         lists, sets, set intersection, sorting
    12_modules_io          pathlib: writing and reading text files
    13_standard_library    re for tokenising, collections.Counter for counting
"""

import re


GETTYSBURG = """
Four score and seven years ago our fathers brought forth on this continent, a
new nation, conceived in Liberty, and dedicated to the proposition that all men
are created equal.

Now we are engaged in a great civil war, testing whether that nation, or any
nation so conceived and so dedicated, can long endure. We are met on a great
battle-field of that war. We have come to dedicate a portion of that field, as
a final resting place for those who here gave their lives that that nation
might live. It is altogether fitting and proper that we should do this.

But, in a larger sense, we can not dedicate—we can not consecrate—we can not
hallow—this ground. The brave men, living and dead, who struggled here, have
consecrated it, far above our poor power to add or detract. The world will
little note, nor long remember what we say here, but it can never forget what
they did here. It is for us the living, rather, to be dedicated here to the
unfinished work which they who fought here have thus far so nobly advanced. It
is rather for us to be here dedicated to the great task remaining before
us—that from these honored dead we take increased devotion to that cause for
which they gave the last full measure of devotion—that we here highly resolve
that these dead shall not have died in vain—that this nation, under God, shall
have a new birth of freedom—and that government of the people, by the people,
for the people, shall not perish from the earth.
"""

# A word is letters, optionally joined by an apostrophe or hyphen to more
# letters: "nation", "don't", "battle-field". Punctuation and dashes between
# words are simply never matched, so they disappear.
WORD = re.compile(r"[a-z]+(?:['-][a-z]+)*")


def tokenise(text: str) -> list[str]:
    """Lower-case the text, then pull out every word in order."""
    # casefold() is lower() made for comparisons; it also handles letters
    # such as the German sharp s that lower() leaves alone.
    return WORD.findall(text.casefold())


def tokenise_demo() -> None:
    print("== stage 1: tokenising ==")
    sample = "It was the best of times, it was the worst of times—"
    print(f"text:   {sample!r}")
    print(f"words:  {tokenise(sample)}")
    tricky = "Don't stop: a battle-field, 'quoted' -- dash"
    print(f"tricky: {tokenise(tricky)}")
    words = tokenise(GETTYSBURG)
    print(f"the Gettysburg Address has {len(words)} words")
    print(f"first ten: {' '.join(words[:10])}")


def main() -> None:
    tokenise_demo()


if __name__ == "__main__":
    main()
