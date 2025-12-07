from ..products.products import AbstractProduct
from ..common.exceptions import ImpossibleLoading, ImpossibleUnloading
from ..common.descriptors import NonNegative


class CargoManager:
    """
    Manages the loading and unloading of cargo based on volume and mass constraints.

    This class tracks the available space and mass capacity of a transport unit.
    It ensures that loading operations do not exceed limits and that unloading
    operations only remove existing items.

    Attributes:
        free_space (float): The current available volume in the transport. 
                            Managed by a descriptor to ensure non-negativity.
        free_mass (float): The current available carrying capacity (weight) in the transport.
                           Managed by a descriptor to ensure non-negativity.
    """
    free_space = NonNegative()
    free_mass = NonNegative()
    
    def __init__(self, capacity: float, carrying_capacity: float) -> None:
        """
        Initialize the CargoManager with specific limits.

        Args:
            capacity (float): The total volume capacity of the transport.
            carrying_capacity (float): The total weight carrying capacity.
        """
        self.free_space = capacity
        self.free_mass = carrying_capacity
        self._cargo: dict[AbstractProduct, int] = {}

    @staticmethod
    def get_requirements(products: dict[AbstractProduct, int]) -> tuple[float, float]:
        """
        Calculate the total volume and mass required for a batch of products.

        Args:
            products (dict[AbstractProduct, int]): A dictionary mapping product instances
                to their quantity.

        Returns:
            tuple[float, float]: A tuple containing (total_required_volume, total_required_mass).
        """
        required_space = 0.0
        required_mass = 0.0
        for product, amount in products.items():
            required_space += product.volume * amount
            required_mass += product.mass * amount
        return required_space, required_mass

    def can_load(
        self, products: dict[AbstractProduct, int], fill_rate: float = 0.9
    ) -> bool:
        """
        Check if the specified products can be loaded into the current free space.

        Args:
            products (dict[AbstractProduct, int]): The products to check.
            fill_rate (float, optional): A coefficient (0.0 to 1.0) representing the
                efficient packing ratio of the remaining space. Defaults to 0.9.

        Returns:
            bool: True if the products fit within the adjusted free space and mass, False otherwise.
        """
        usable_space = self.free_space * fill_rate
        required_space, required_mass = CargoManager.get_requirements(products)

        return required_space <= usable_space and required_mass <= self.free_mass

    def _commit_load(
        self,
        products: dict[AbstractProduct, int],
        required_space: float,
        required_mass: float,
    ) -> None:
        """
        Update the internal state to reflect loaded products.

        Args:
            products (dict[AbstractProduct, int]): The products being loaded.
            required_space (float): The total volume consumed by the products.
            required_mass (float): The total mass consumed by the products.
        """
        for product, amount in products.items():
            self._cargo[product] = self._cargo.get(product, 0) + amount

        self.free_space -= required_space
        self.free_mass -= required_mass

    def load_products(
        self, products: dict[AbstractProduct, int], fill_rate: float = 0.9
    ) -> None:
        """
        Load products into the transport if capacity allows.

        Args:
            products (dict[AbstractProduct, int]): The products to load.
            fill_rate (float, optional): Packing efficiency coefficient. Defaults to 0.9.

        Raises:
            ImpossibleLoading: If there is insufficient space or mass capacity.
        """
        if not self.can_load(products, fill_rate):
            raise ImpossibleLoading("There isn't enough space or carrying capacity in transport")

        required_space, required_mass = CargoManager.get_requirements(products)
        self._commit_load(products, required_space, required_mass)

    def can_unload(self, products: dict[AbstractProduct, int]) -> bool:
        """
        Check if the specified products exist in the cargo and can be unloaded.

        Args:
            products (dict[AbstractProduct, int]): The products and quantities to check.

        Returns:
            bool: True if the cargo contains at least the requested amount of every product.
        """
        if set(products) - set(self._cargo):
            return False

        for product, amount in products.items():
            if self._cargo[product] < amount:
                return False

        return True

    def _commit_unload(self, products: dict[AbstractProduct, int]) -> None:
        """
        Update the internal state to reflect unloaded products.

        Removes products from the internal dictionary if the count reaches zero
        and reclaims free space and mass.

        Args:
            products (dict[AbstractProduct, int]): The products being unloaded.
        """
        for product, amount in products.items():
            self._cargo[product] -= amount

            if self._cargo[product] == 0:
                del self._cargo[product]

            self.free_space += product.volume * amount
            self.free_mass += product.mass * amount

    def unload_products(self, products: dict[AbstractProduct, int]) -> None:
        """
        Unload products from the transport.

        Args:
            products (dict[AbstractProduct, int]): The products to unload.

        Raises:
            ImpossibleUnloading: If the requested products are not present in sufficient quantities.
        """
        if not self.can_unload(products):
            raise ImpossibleUnloading("There isn't enough products in transport")

        self._commit_unload(products)

    def is_empty(self) -> bool:
        """
        Check if the transport is completely empty.

        Returns:
            bool: True if no products are currently loaded.
        """
        return len(self._cargo) == 0
    
    @property
    def cargo(self) -> dict[AbstractProduct, int]:
        """
        Get a copy of the current cargo inventory.

        Returns:
            dict[AbstractProduct, int]: A copy of the dictionary mapping products to quantities.
        """
        return self._cargo.copy()
    
    def get_product_names(self) -> list[str]:
        """
        Retrieve the list of product objects currently in cargo.
        
        Note:
            Despite the method name and type hint, this returns the product instances (keys),
            not their string names, unless the product objects are strings.

        Returns:
            list[str]: A list of AbstractProduct keys from the cargo dictionary.
        """
        return list(self._cargo.keys())
