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
from collections import Counter


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


# Stop words are so common that they top every count and say nothing about
# the text. Real tools ship lists of a few hundred; this short one is enough.
STOP_WORDS = frozenset(
    """
    a about above after all am an and any are as at be been before but by can
    could did do does for from had has have he her here him his how i if in
    into is it its me my no nor not now of on or our out over she should so
    some than that the their them then there these they this those to too
    under up us was we were what when which while who whom will with would
    you your
    """.split()
)


def count_words(words: list[str]) -> Counter[str]:
    return Counter(words)


def count_content_words(words: list[str]) -> Counter[str]:
    """Count only the words that carry meaning."""
    return Counter(w for w in words if w not in STOP_WORDS)


def counting_demo() -> None:
    print("== stage 2: counting ==")
    words = tokenise(GETTYSBURG)
    everything = count_words(words)
    content = count_content_words(words)
    print(f"top 6, all words:     {everything.most_common(6)}")
    print(f"top 6, content words: {content.most_common(6)}")
    # "here" is in the stop list, which hides one of Lincoln's key words.
    # Stop lists are a blunt tool: check what they remove.
    print(f"'here' appears {everything['here']} times but is filtered out")
    print(f"a missing word counts as zero: {content['telephone']}")


def bar_chart(pairs: list[tuple[str, int]], width: int = 30) -> list[str]:
    """One line per (label, count), with a bar scaled to the biggest count."""
    if not pairs:
        return ["(nothing to chart)"]
    biggest = pairs[0][1]
    label_width = max(len(label) for label, _ in pairs)
    lines = []
    for label, count in pairs:
        # Scale so the largest bar is `width` long; every bar gets at least
        # one character so small counts stay visible.
        bar = "#" * max(1, round(count / biggest * width))
        lines.append(f"  {label:<{label_width}}  {count:>3}  {bar}")
    return lines


def report(title: str, text: str, top: int = 8) -> str:
    words = tokenise(text)
    counts = count_words(words)
    content = count_content_words(words)
    average = sum(len(w) for w in words) / len(words)
    # max with key=len returns the first of the longest words it meets.
    longest = max(counts, key=len)
    lines = [
        title,
        "=" * len(title),
        f"  words              {len(words):>6}",
        f"  distinct words     {len(counts):>6}",
        f"  distinct / total   {len(counts) / len(words):>6.2f}",
        f"  average length     {average:>6.2f}",
        f"  longest word       {longest}",
        "",
        f"Top {top} content words",
        *bar_chart(content.most_common(top)),
    ]
    return "\n".join(lines)


def report_demo() -> None:
    print("== stage 3: the report ==")
    print(report("The Gettysburg Address", GETTYSBURG))


def main() -> None:
    tokenise_demo()
    print()
    counting_demo()
    print()
    report_demo()


if __name__ == "__main__":
    main()
