"""Classes — bundling data with the functions that operate on it.

`__init__` is not a constructor; the object already exists by then. It is an
*initialiser* that sets up attributes on the freshly made instance.

`self` is the instance, passed explicitly as the first parameter of every
method. Python makes that wiring visible rather than hiding it in a keyword.

Attributes assigned in `__init__` belong to the instance. Attributes assigned
in the class body are shared by every instance — a distinction that matters
enormously when the shared value is mutable.
"""


class Dog:
    species = "Canis familiaris"  # class attribute: shared by all instances

    def __init__(self, name: str, age: int) -> None:
        self.name = name  # instance attributes: one per object
        self.age = age
        self._tricks: list[str] = []  # leading _ means "internal"

    def speak(self) -> str:
        return f"{self.name} says woof"

    def learn(self, trick: str) -> None:
        self._tricks.append(trick)

    @property
    def tricks(self) -> tuple[str, ...]:
        """Read-only view, so callers cannot mutate the internal list."""
        return tuple(self._tricks)

    @classmethod
    def puppy(cls, name: str) -> "Dog":
        """An alternative constructor — Python's answer to overloading."""
        return cls(name, 0)

    @staticmethod
    def is_valid_age(age: int) -> bool:
        """No self, no cls — just a function that belongs here logically."""
        return 0 <= age <= 30


def main() -> None:
    rex = Dog("Rex", 3)
    print(f"{rex.name}, {rex.age}, {rex.species}")
    print(rex.speak())

    rex.learn("sit")
    rex.learn("roll over")
    print(f"tricks = {rex.tricks}")

    pup = Dog.puppy("Bud")
    print(f"{pup.name} is {pup.age}")
    print(f"is_valid_age(40) -> {Dog.is_valid_age(40)}")

    # Every instance sees the same class attribute...
    print(f"shared species: {rex.species is pup.species}")
    # ...until one shadows it with an instance attribute of the same name.
    rex.species = "Very Good Dog"
    print(f"rex: {rex.species}, pup: {pup.species}, class: {Dog.species}")

    # Attributes live in a dict, and can be added at runtime.
    print(f"rex.__dict__ = {rex.__dict__}")


if __name__ == "__main__":
    main()
