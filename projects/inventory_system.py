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

from dataclasses import dataclass
from decimal import Decimal


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


def main() -> None:
    products_demo()


if __name__ == "__main__":
    main()
