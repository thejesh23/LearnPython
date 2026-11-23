"""Colour conversions: hex strings, RGB triples and HSL.

A hex colour like #FF8800 is just three bytes written in base 16, so hex to
RGB is three base-16 parses and RGB to hex is three two-digit formats. The
three-digit shorthand #F80 doubles each digit (F80 -> FF8800).

HSL describes the same colour as hue (an angle on the colour wheel),
saturation and lightness, which is what you want when you need "the same
colour, but darker". The conversion is hand-written here and checked against
the standard library's colorsys, which works in 0..1 floats and spells the
model HLS.
"""

import colorsys

RGB = tuple[int, int, int]


def hex_to_rgb(text: str) -> RGB:
    digits = text.removeprefix("#")
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    if len(digits) != 6:
        raise ValueError(f"bad colour: {text!r}")
    try:
        return (int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16))
    except ValueError:
        raise ValueError(f"bad colour: {text!r}") from None


def rgb_to_hex(rgb: RGB) -> str:
    if any(not 0 <= c <= 255 for c in rgb):
        raise ValueError(f"channel out of range: {rgb}")
    return "#" + "".join(f"{c:02X}" for c in rgb)


def rgb_to_hsl(rgb: RGB) -> tuple[float, float, float]:
    r, g, b = (c / 255 for c in rgb)
    high, low = max(r, g, b), min(r, g, b)
    light = (high + low) / 2
    if high == low:
        return 0.0, 0.0, light  # a grey has no hue
    span = high - low
    sat = span / (2 - high - low) if light > 0.5 else span / (high + low)
    if high == r:
        hue = (g - b) / span % 6
    elif high == g:
        hue = (b - r) / span + 2
    else:
        hue = (r - g) / span + 4
    return hue * 60, sat, light


def hsl_to_rgb(hue: float, sat: float, light: float) -> RGB:
    chroma = (1 - abs(2 * light - 1)) * sat
    x = chroma * (1 - abs(hue / 60 % 2 - 1))
    m = light - chroma / 2
    sector = int(hue // 60) % 6
    r, g, b = [(chroma, x, 0), (x, chroma, 0), (0, chroma, x),
               (0, x, chroma), (x, 0, chroma), (chroma, 0, x)][sector]
    return tuple(round((c + m) * 255) for c in (r, g, b))  # type: ignore[return-value]


def darken(text: str, amount: float) -> str:
    hue, sat, light = rgb_to_hsl(hex_to_rgb(text))
    return rgb_to_hex(hsl_to_rgb(hue, sat, max(0.0, light - amount)))


def main() -> None:
    for text in ["#FF8800", "#f80", "#336699", "#000", "#FFFFFF", "808080"]:
        rgb = hex_to_rgb(text)
        hue, sat, light = rgb_to_hsl(rgb)
        print(f"{text:>8} -> {rgb} -> {rgb_to_hex(rgb)}  "
              f"hsl({hue:5.1f}, {sat:.0%}, {light:.0%})")

    print(f"\n#336699 darkened by 15%: {darken('#336699', 0.15)}")

    mismatches = 0
    for r in range(0, 256, 17):
        for g in range(0, 256, 17):
            for b in range(0, 256, 17):
                hue, sat, light = rgb_to_hsl((r, g, b))
                h2, l2, s2 = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
                if abs(sat - s2) > 1e-9 or abs(light - l2) > 1e-9 or (
                        sat and abs(hue - h2 * 360) > 1e-6):
                    mismatches += 1
                if hsl_to_rgb(hue, sat, light) != (r, g, b):
                    mismatches += 1
    print(f"mismatches against colorsys and round trip: {mismatches}")

    for bad in ["#12345", "#GGGGGG"]:
        try:
            hex_to_rgb(bad)
        except ValueError as err:
            print(f"rejected: {err}")


if __name__ == "__main__":
    main()
