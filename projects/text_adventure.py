"""Project: a small text adventure game.

You build it in four steps:

    1. the world     rooms, exits and items described as plain data, then
                     checked so a typo in an exit name is caught at start-up
    2. the parser    turn typed text into a Command with a match statement
    3. the game      move between rooms, pick things up, carry an inventory,
                     open a locked door, see nothing in the dark without a lamp
    4. winning       escape with the crown; the demo plays a scripted
                     walkthrough, `python text_adventure.py --play` lets you type

Keeping the world as data and the rules as code means you can design a new
adventure by editing only the ROOMS dict.

Uses:
    04_strings             split, join, lower
    05_control_flow        match statements with guards and captures
    07_collections         dicts, lists, copy.deepcopy
    09_classes             dataclasses, class patterns in match
"""

import copy
import sys
from dataclasses import dataclass, field


ROOMS = {
    "hall": {
        "description": "A dusty entrance hall. The front door creaks in the wind.",
        "exits": {"north": "library", "east": "kitchen", "down": "cellar"},
        "items": [],
    },
    "kitchen": {
        "description": "A cold kitchen that smells of old soup.",
        "exits": {"west": "hall"},
        "items": ["lamp", "spoon"],
    },
    "library": {
        "description": "Shelves of mouldy books. A ladder leads up to a trapdoor.",
        "exits": {"south": "hall", "up": "tower"},
        "items": ["book"],
        "locked": {"up": "brass key"},  # exit -> item that unlocks it
    },
    "cellar": {
        "description": "A damp cellar full of broken barrels.",
        "exits": {"up": "hall"},
        "items": ["brass key"],
        "dark": True,
    },
    "tower": {
        "description": "A round tower room. Moonlight falls on a velvet cushion.",
        "exits": {"down": "library"},
        "items": ["crown"],
    },
}


@dataclass
class Room:
    name: str
    description: str
    exits: dict[str, str]
    items: list[str] = field(default_factory=list)
    locked: dict[str, str] = field(default_factory=dict)
    dark: bool = False


def build_world(data: dict[str, dict]) -> dict[str, Room]:
    # deepcopy so a game that moves items around never edits ROOMS itself;
    # every new game then starts from the same untouched world.
    world = {name: Room(name, **copy.deepcopy(spec)) for name, spec in data.items()}
    for room in world.values():
        for direction, target in room.exits.items():
            if target not in world:
                raise ValueError(f"{room.name}: exit {direction} -> unknown {target!r}")
    return world


def world_demo() -> None:
    world = build_world(ROOMS)
    for room in world.values():
        notes = ["dark" if room.dark else "", "locked" if room.locked else ""]
        extra = ", ".join(n for n in notes if n)
        print(f"{room.name:<8} exits {sorted(room.exits)} {extra}".rstrip())
    try:
        build_world({"hall": {"description": "", "exits": {"north": "nowhere"}}})
    except ValueError as exc:
        print(f"ValueError: {exc}")


DIRECTIONS = {"n": "north", "s": "south", "e": "east", "w": "west",
              "u": "up", "d": "down"}
DIRECTIONS |= {d: d for d in list(DIRECTIONS.values())}
FILLER = {"the", "a", "an", "to"}


@dataclass
class Command:
    verb: str
    noun: str = ""


def parse(text: str) -> Command:
    words = [w for w in text.lower().split() if w not in FILLER]
    match words:
        case []:
            return Command("nothing")
        case ["go" | "walk" | "climb", direction] if direction in DIRECTIONS:
            return Command("go", DIRECTIONS[direction])
        case [direction] if direction in DIRECTIONS:  # just "n" or "north"
            return Command("go", DIRECTIONS[direction])
        case ["take" | "get" | "grab", *item] if item:
            return Command("take", " ".join(item))
        case ["drop", *item] if item:
            return Command("drop", " ".join(item))
        case ["look" | "l"]:
            return Command("look")
        case ["inventory" | "inv" | "i"]:
            return Command("inventory")
        case ["quit" | "q"]:
            return Command("quit")
        case _:
            return Command("unknown", text.strip())


def parser_demo() -> None:
    for text in ["go north", "N", "climb the up", "take the brass key", "i",
                 "drop", "look", "", "dance wildly"]:
        print(f"{text!r:22} -> {parse(text)}")


class Game:
    def __init__(self, data: dict[str, dict], start: str = "hall") -> None:
        self.world = build_world(data)
        self.here = self.world[start]
        self.inventory: list[str] = []
        self.over = False
        self.moves = 0

    def can_see(self) -> bool:
        return not self.here.dark or "lamp" in self.inventory

    def describe(self) -> str:
        if not self.can_see():
            return "It is pitch dark. You might trip over something."
        text = self.here.description
        if self.here.items:
            text += f"\nYou see: {', '.join(self.here.items)}."
        return text + f"\nExits: {', '.join(sorted(self.here.exits))}."

    def go(self, direction: str) -> str:
        if direction not in self.here.exits:
            return "You can't go that way."
        news = ""
        key = self.here.locked.get(direction)
        if key:
            if key not in self.inventory:
                return "It's locked."
            del self.here.locked[direction]  # stays unlocked from now on
            news = f"You unlock the way {direction} with the {key}.\n"
        self.here = self.world[self.here.exits[direction]]
        return news + self.describe()

    def take(self, item: str) -> str:
        if not self.can_see():
            return "You fumble around in the dark and find nothing."
        if item not in self.here.items:
            return f"There is no {item} here."
        self.here.items.remove(item)
        self.inventory.append(item)
        return f"Taken: {item}."

    def drop(self, item: str) -> str:
        if item not in self.inventory:
            return f"You are not carrying a {item}."
        self.inventory.remove(item)
        self.here.items.append(item)
        return f"Dropped: {item}."

    def step(self, text: str) -> str:
        self.moves += 1
        # Class patterns: Command("go", d) matches a Command whose verb is
        # "go" and binds its noun to d (dataclasses support this for free).
        match parse(text):
            case Command("go", direction):
                return self.go(direction)
            case Command("take", item):
                return self.take(item)
            case Command("drop", item):
                return self.drop(item)
            case Command("look"):
                return self.describe()
            case Command("inventory"):
                return f"You carry: {', '.join(self.inventory) or 'nothing'}."
            case Command("quit"):
                self.over = True
                return "Bye."
            case Command("nothing"):
                return "Say something."
            case Command(noun=said):
                return f"I don't understand {said!r}."


def game_demo() -> None:
    game = Game(ROOMS)
    for text in ["e", "take lamp", "take sword", "w", "u", "n", "up", "i"]:
        print(f"> {text}")
        print(game.step(text))


class Adventure(Game):
    goal = "crown"

    def step(self, text: str) -> str:
        reply = super().step(text)
        # Winning: be back in the hall, carrying the crown.
        if self.here.name == "hall" and self.goal in self.inventory:
            self.over = True
            reply += f"\nYou slip out of the front door with the {self.goal}. You win!"
        return reply


WALKTHROUGH = [
    "look", "down", "take brass key", "up", "east", "take the lamp", "west",
    "d", "take brass key", "u", "dance", "north", "up", "take crown",
    "drop lamp", "i", "down", "south",
]


def walkthrough_demo() -> None:
    game = Adventure(ROOMS)
    print(game.describe())
    commands = iter(WALKTHROUGH)
    while not game.over:
        if "--play" in sys.argv:
            try:
                text = input("> ")
            except EOFError:
                break
        else:
            text = next(commands, "quit")
            print(f"> {text}")
        print(game.step(text))
    print(f"[{game.moves} moves]")


def main() -> None:
    world_demo()
    print()
    parser_demo()
    print()
    game_demo()
    print()
    walkthrough_demo()


if __name__ == "__main__":
    main()
