"""An inventory system for a small shop, with its own test suite.

You build the stock-keeping core of a shop: a product catalogue, a ledger of
stock movements (goods received, orders shipped, corrections after a count),
a low-stock report that says what to reorder, and a unittest suite that pins
the rules down.

Two design ideas worth noticing:

    The ledger is the truth. Stock on hand is not a number you overwrite;
    it is the sum of every movement. You can always answer "why is it 7?"
    by reading the history.

    Errors have names. Asking for a product that does not exist and trying
    to ship more than you have are different problems, so they are
    different exception classes that callers can catch separately.

Money is kept as Decimal, never float: 0.1 + 0.2 is not 0.3 in floating
point, and prices must add up exactly.

Uses:
    05_control_flow        match with guards on the movement kind
    06_functions           passing a function (the clock) as an argument
    07_collections         dicts keyed by SKU, sorting reports
    08_iterators           itertools.count behind a fake clock
    09_classes             dataclasses, __post_init__ validation, enums
    11_errors              a custom exception hierarchy with extra fields
    13_standard_library    decimal, datetime
    14_testing             unittest: TestCase, setUp, assertRaises
"""

import itertools
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from enum import Enum


class InventoryError(Exception):
    """Base class: `except InventoryError` catches every problem below."""


class InvalidProduct(InventoryError):
    pass


class UnknownProduct(InventoryError):
    def __init__(self, sku: str) -> None:
        super().__init__(f"no product with SKU {sku!r}")
        self.sku = sku


class InsufficientStock(InventoryError):
    def __init__(self, sku: str, requested: int, available: int) -> None:
        super().__init__(
            f"cannot take {requested} of {sku}: only {available} in stock"
        )
        # Extra fields let a caller react, e.g. offer the available amount.
        self.sku = sku
        self.requested = requested
        self.available = available


@dataclass(frozen=True)
class Product:
    sku: str  # "stock keeping unit": the shop's own product code
    name: str
    price: Decimal
    reorder_level: int = 5  # reorder when stock falls to this or below

    def __post_init__(self) -> None:
        # A dataclass writes __init__ for us; __post_init__ runs right after
        # it, which is the place to reject bad values.
        if not self.sku or not self.sku.isupper():
            raise InvalidProduct(f"SKU must be upper case, got {self.sku!r}")
        if self.price <= 0:
            raise InvalidProduct(f"price must be positive, got {self.price}")
        if self.reorder_level < 0:
            raise InvalidProduct("reorder level cannot be negative")


CATALOGUE = [
    Product("MUG-01", "Coffee mug", Decimal("8.50"), reorder_level=10),
    Product("TEE-M", "T-shirt, medium", Decimal("15.00")),
    Product("TEE-L", "T-shirt, large", Decimal("15.00")),
    Product("PEN-3", "Pen, pack of 3", Decimal("3.20"), reorder_level=20),
    Product("BAG-01", "Tote bag", Decimal("12.75"), reorder_level=3),
]


def products_demo() -> None:
    print("== stage 1: products and errors ==")
    for product in CATALOGUE[:2]:
        print(product)
    for bad in [("mug-02", "x", Decimal("1")), ("MUG-02", "x", Decimal("-1"))]:
        try:
            Product(*bad)
        except InvalidProduct as exc:
            print(f"InvalidProduct: {exc}")
    # Every specific error is also an InventoryError.
    print(f"is an InventoryError: {isinstance(UnknownProduct('X'), InventoryError)}")


class Kind(Enum):
    RECEIVE = "receive"  # goods arrive from a supplier
    SHIP = "ship"  # goods leave for a customer
    ADJUST = "adjust"  # a correction after counting the shelf


@dataclass(frozen=True)
class Movement:
    sku: str
    kind: Kind
    quantity: int  # signed: +3 adds three to stock, -2 removes two
    note: str
    at: datetime


def fake_clock(start: datetime, step: timedelta) -> Callable[[], datetime]:
    """A stand-in for datetime.now that moves forward `step` per call."""
    times = (start + step * i for i in itertools.count())
    return lambda: next(times)


class Inventory:
    def __init__(self, clock: Callable[[], datetime] = datetime.now) -> None:
        self.products: dict[str, Product] = {}
        self.ledger: list[Movement] = []
        # The clock is passed in rather than called directly, so a demo or a
        # test can supply a fake one and get the same timestamps every run.
        self.clock = clock

    def add_product(self, product: Product) -> None:
        if product.sku in self.products:
            raise InvalidProduct(f"duplicate SKU {product.sku!r}")
        self.products[product.sku] = product

    def product(self, sku: str) -> Product:
        try:
            return self.products[sku]
        except KeyError:
            # `from None` hides the KeyError: our error says it all.
            raise UnknownProduct(sku) from None

    def on_hand(self, sku: str) -> int:
        self.product(sku)  # raises UnknownProduct for a bad SKU
        return sum(m.quantity for m in self.ledger if m.sku == sku)

    def _record(self, sku: str, kind: Kind, quantity: int, note: str) -> None:
        self.product(sku)
        # The first case that matches wins. A guard (`if ...`) makes a case
        # match only when its condition is also true.
        match kind:
            case Kind.RECEIVE | Kind.SHIP if quantity <= 0:
                raise ValueError(f"{kind.value} quantity must be positive")
            case Kind.SHIP:
                available = self.on_hand(sku)
                if quantity > available:
                    raise InsufficientStock(sku, quantity, available)
                quantity = -quantity
            case Kind.ADJUST if self.on_hand(sku) + quantity < 0:
                raise InsufficientStock(sku, -quantity, self.on_hand(sku))
        self.ledger.append(Movement(sku, kind, quantity, note, self.clock()))

    def receive(self, sku: str, quantity: int, note: str = "") -> None:
        self._record(sku, Kind.RECEIVE, quantity, note)

    def ship(self, sku: str, quantity: int, note: str = "") -> None:
        self._record(sku, Kind.SHIP, quantity, note)

    def adjust(self, sku: str, change: int, note: str) -> None:
        self._record(sku, Kind.ADJUST, change, note)

    def history(self, sku: str) -> list[Movement]:
        return [m for m in self.ledger if m.sku == sku]


def sample_inventory() -> Inventory:
    inv = Inventory(clock=fake_clock(datetime(2024, 5, 1, 9, 0), timedelta(minutes=25)))
    for product in CATALOGUE:
        inv.add_product(product)
    inv.receive("MUG-01", 24, "PO-1001")
    inv.receive("TEE-M", 12, "PO-1001")
    inv.receive("TEE-L", 6, "PO-1001")
    inv.receive("PEN-3", 50, "PO-1002")
    inv.receive("BAG-01", 4, "PO-1002")
    inv.ship("MUG-01", 15, "order 1")
    inv.ship("TEE-L", 4, "order 2")
    inv.ship("PEN-3", 32, "order 3")
    inv.adjust("MUG-01", -1, "one broken in the store room")
    inv.ship("BAG-01", 1, "order 4")
    return inv


def movements_demo() -> None:
    print("== stage 2: stock movements ==")
    inv = sample_inventory()
    print(f"MUG-01 on hand: {inv.on_hand('MUG-01')}")
    for m in inv.history("MUG-01"):
        print(f"  {m.at:%Y-%m-%d %H:%M}  {m.kind.value:<8}{m.quantity:>+4}  {m.note}")

    for action in [
        lambda: inv.ship("TEE-L", 5, "order 5"),
        lambda: inv.receive("HAT-01", 3),
        lambda: inv.receive("TEE-M", 0),
    ]:
        try:
            action()
        except InsufficientStock as exc:
            print(f"InsufficientStock: {exc} (could offer {exc.available})")
        except InventoryError as exc:
            print(f"{type(exc).__name__}: {exc}")
        except ValueError as exc:
            print(f"ValueError: {exc}")


def main() -> None:
    products_demo()
    print()
    movements_demo()


if __name__ == "__main__":
    main()
