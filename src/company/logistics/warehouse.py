from ..products.products import AbstractProduct
from ..hr.employees import AbstractEmployee
from .transport import AbstractTransport
from .cargo_manager import CargoManager
from ..hr.employee_manager import EmployeeManagerMixin
from ..common.descriptors import NonNegative
from ..common.validation import validate_non_negative
from ..common.exceptions import ImpossibleLoading, ImpossibleUnloading


class Warehouse(EmployeeManagerMixin):
    """
    Represents a storage facility for products.

    This class manages inventory space and employee assignments. It acts as a 
    central hub for transferring goods to and from transport vehicles. Unlike 
    transport, a warehouse typically has infinite weight carrying capacity 
    (assumed structure stability) but limited volume capacity.

    Attributes:
        capacity (float): Total volume available for storage.
        carrying_capacity (float): Total weight capacity (set to infinity by default).
    """
    capacity = NonNegative()
    carrying_capacity = NonNegative()

    def __init__(self, capacity: float) -> None:
        """
        Initialize the Warehouse.

        Args:
            capacity (float): The total volume capacity of the warehouse.
        """
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
        """
        Move products from the warehouse into a transport vehicle.

        This operation ensures that the products exist in the warehouse and that
        the transport has enough space to receive them before committing the transaction.

        Args:
            transport (AbstractTransport): The vehicle receiving the cargo.
            products (dict[AbstractProduct, int]): The products to transfer.
            fill_rate (float, optional): Packing efficiency for the transport. Defaults to 0.9.

        Raises:
            ImpossibleUnloading: If the warehouse does not have the specified products.
            ImpossibleLoading: If the transport does not have enough space/capacity.
        """
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
        """
        Move products from a transport vehicle into the warehouse.

        This operation ensures that the warehouse has enough space and that
        the transport actually contains the products before committing the transaction.

        Args:
            transport (AbstractTransport): The vehicle delivering the cargo.
            products (dict[AbstractProduct, int]): The products to transfer.
            fill_rate (float, optional): Packing efficiency for the warehouse storage. Defaults to 0.9.

        Raises:
            ImpossibleLoading: If the warehouse does not have enough space.
            ImpossibleUnloading: If the transport does not have the specified products.
        """
        validate_non_negative(fill_rate)
        if not self._cargo_manager.can_load(products, fill_rate):
            raise ImpossibleLoading("Warehouse loading is impossible")
        if not transport.can_unload(products):
            raise ImpossibleUnloading("Transport unloading is impossible")

        self._cargo_manager.load_products(products, fill_rate)
        transport.unload_products(products)
        print("Product exchange between warehouse and transport was successfully ended")

    def supply(self, products: dict[AbstractProduct, int], fill_rate: float = 0.9) -> None:
        """
        Add products directly to the warehouse (e.g., from an external supplier).

        Args:
            products (dict[AbstractProduct, int]): The products to add to inventory.
            fill_rate (float, optional): Packing efficiency coefficient. Defaults to 0.9.

        Raises:
            ImpossibleLoading: If the warehouse is full or cannot accommodate the supply.
        """
        validate_non_negative(fill_rate)
        try:
            self._cargo_manager.load_products(products, fill_rate)
            print("Supplement was successfully placed")
        except ImpossibleLoading as e:
            print(f"Supplement can't be placed in the warehouse: {e}")
            raise

    def is_empty(self) -> bool:
        """
        Check if the warehouse has no products in storage.

        Prints the status to stdout.

        Returns:
            bool: True if empty, False otherwise.
        """
        empty = self._cargo_manager.is_empty()
        print("Warehouse is empty") if empty else print("Warehouse is not empty")
        return empty

    def get_product_names(self) -> list[str]:
        """
        Retrieve a list of product keys currently stored in the warehouse.

        Returns:
            list[str]: A list of product identifiers/objects.
        """
        return self._cargo_manager.get_product_names()

    @property
    def cargo(self) -> dict[AbstractProduct, int]:
        """
        Get the current warehouse inventory.

        Returns:
            dict[AbstractProduct, int]: A copy of the dictionary mapping products to quantities.
        """
        return self._cargo_manager.cargo
