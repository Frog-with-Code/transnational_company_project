from ..products.products import AbstractProduct
from ..hr.employees import AbstractEmployee
from transport import AbstractTransport
from cargo_manager import CargoManager
from ..hr.employee_manager import EmployeeManagerMixin


class Warehouse(EmployeeManagerMixin):
    def __init__(self, capacity: float) -> None:
        super().__init__()
        self.capacity = capacity
        self.carrying_capacity = float("inf")
        self._cargo_manager = CargoManager(self.capacity, self.carrying_capacity)
        self._employees: set[AbstractEmployee] = set()

    def load_transport(
        self, transport: AbstractTransport, products: dict[AbstractProduct, int]
    ) -> bool:
        if self._cargo_manager.can_unload(products) and transport.can_load(products):
            self._cargo_manager.unload_products(products)
            transport.load_products(products)
            print(
                "Product exchange between warehouse and transport was successfully ended"
            )
            return True
        else:
            print("Transport loading is impossible!")
            return False

    def unload_transport(
        self, transport: AbstractTransport, products: dict[AbstractProduct, int]
    ) -> bool:
        success = self._cargo_manager.can_load(products) and transport.can_unload(
            products
        )
        if success:
            self._cargo_manager.load_products(products)
            transport.unload_products(products)
            print(
                "Product exchange between warehouse and transport was successfully ended"
            )
        else:
            print("Transport unloading is impossible!")

        return success

    def supply(self, products: dict[AbstractProduct], int) -> bool:
        success = self._cargo_manager.load_products(products)
        print(
            "Supplement was successfully placed"
            if success
            else "Supplement can't be placed in the warehouse"
        )
        return success

    def is_empty(self) -> bool:
        empty = self._cargo_manager.is_empty()
        print("Warehouse is empty") if empty else print("Warehouse is not empty")
        return empty
    
    def get_product_names(self) -> list[str]:
        return self._cargo_manager.get_product_names()
    
    @property
    def cargo(self) -> dict[AbstractProduct, int]:
        return self._cargo_manager.cargo
    
