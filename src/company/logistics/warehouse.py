from ..products.products import AbstractProduct
from ..hr.employees import AbstractEmployee
from .transport import AbstractTransport
from .cargo_manager import CargoManager
from ..hr.employee_manager import EmployeeManagerMixin
from ..common.descriptors import NonNegative
from ..common.validation import validate_non_negative
from ..common.exceptions import ImpossibleLoading, ImpossibleUnloading


class Warehouse(EmployeeManagerMixin):
    capacity = NonNegative()
    carrying_capacity = NonNegative()

    def __init__(self, capacity: float) -> None:
        super().__init__()
        self.capacity = capacity
        self.carrying_capacity = float("inf")
        self._cargo_manager = CargoManager(self.capacity, self.carrying_capacity)
        self._employees: set[AbstractEmployee] = set()

    def load_transport(
        self,
        transport: AbstractTransport,
        products: dict[AbstractProduct, int],
        fill_rate: float = 0.9,
    ) -> None:
        validate_non_negative(fill_rate)
        if not self._cargo_manager.can_unload(products):
            raise ImpossibleUnloading("Warehouse unloading is impossible")
        if not transport.can_load(products, fill_rate):
            raise ImpossibleLoading("Transport loading is impossible")

        self._cargo_manager.unload_products(products)
        transport.load_products(products, fill_rate)
        print("Product exchange between warehouse and transport was successfully ended")

    def unload_transport(
        self, transport: AbstractTransport, products: dict[AbstractProduct, int], fill_rate: float = 0.9
    ) -> None:
        validate_non_negative(fill_rate)
        if not self._cargo_manager.can_load(products, fill_rate):
            raise ImpossibleLoading("Warehouse loading is impossible")
        if not transport.can_unload(products):
            raise ImpossibleUnloading("Transport unloading is impossible")

        self._cargo_manager.load_products(products, fill_rate)
        transport.unload_products(products)
        print("Product exchange between warehouse and transport was successfully ended")

    def supply(self, products: dict[AbstractProduct, int], fill_rate: float = 0.9) -> None:
        validate_non_negative(fill_rate)
        try:
            self._cargo_manager.load_products(products, fill_rate)
            print("Supplement was successfully placed")
        except ImpossibleLoading as e:
            print(f"Supplement can't be placed in the warehouse: {e}")
            raise

    def is_empty(self) -> bool:
        empty = self._cargo_manager.is_empty()
        print("Warehouse is empty") if empty else print("Warehouse is not empty")
        return empty

    def get_product_names(self) -> list[str]:
        return self._cargo_manager.get_product_names()

    @property
    def cargo(self) -> dict[AbstractProduct, int]:
        return self._cargo_manager.cargo
