"""Converting between Celsius, Fahrenheit and Kelvin through a hub.

With n scales, writing every pairwise formula takes n * (n - 1) functions.
Picking one hub scale (Celsius here) cuts that to 2 * n: each scale only needs
"to Celsius" and "from Celsius", and any conversion is a trip through the hub.
Adding Rankine later is two lines, not six.

The formulas are all affine (multiply, then shift), so they invert cleanly.
Kelvin (written K, never °K) and Rankine start at absolute zero, so anything
colder than -273.15 °C is rejected instead of silently returned.
"""

from enum import Enum

ABSOLUTE_ZERO_C = -273.15


class Scale(Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"
    RANKINE = "R"

    @property
    def unit(self) -> str:
        return "K" if self is Scale.KELVIN else f"°{self.value}"


def to_celsius(value: float, scale: Scale) -> float:
    match scale:
        case Scale.CELSIUS:
            return value
        case Scale.FAHRENHEIT:
            return (value - 32) * 5 / 9
        case Scale.KELVIN:
            return value + ABSOLUTE_ZERO_C
        case Scale.RANKINE:
            return (value - 491.67) * 5 / 9


def from_celsius(celsius: float, scale: Scale) -> float:
    match scale:
        case Scale.CELSIUS:
            return celsius
        case Scale.FAHRENHEIT:
            return celsius * 9 / 5 + 32
        case Scale.KELVIN:
            return celsius - ABSOLUTE_ZERO_C
        case Scale.RANKINE:
            return (celsius + 273.15) * 9 / 5


def convert(value: float, source: Scale, target: Scale) -> float:
    celsius = to_celsius(value, source)
    if celsius < ABSOLUTE_ZERO_C - 1e-9:
        raise ValueError(f"{value} {source.unit} is below absolute zero")
    return from_celsius(celsius, target)


def main() -> None:
    print("landmarks:")
    for label, c in [("absolute zero", ABSOLUTE_ZERO_C), ("water freezes", 0),
                     ("body", 37), ("water boils", 100)]:
        row = ", ".join(f"{convert(c, Scale.CELSIUS, s):8.2f} {s.unit}"
                        for s in Scale)
        print(f"  {label:<14} {row}")

    crossover = -40.0
    print(f"\n-40 °C in °F: {convert(crossover, Scale.CELSIUS, Scale.FAHRENHEIT)}")

    worst = 0.0
    for s in Scale:
        for t in Scale:
            for v in [0.0, 12.5, 300.0, 1000.0]:
                back = convert(convert(v, s, t), t, s)
                worst = max(worst, abs(back - v))
    print(f"largest round-trip error over all pairs: {worst:.2e}")

    try:
        convert(-10, Scale.KELVIN, Scale.CELSIUS)
    except ValueError as err:
        print(f"rejected: {err}")


if __name__ == "__main__":
    main()
