from ..products.products import AbstractProduct
from ..common.exceptions import ImpossibleLoading, ImpossibleUnloading


class CargoManager:
    def __init__(self, capacity: float, carrying_capacity: float) -> None:
        self.free_space = capacity
        self.free_mass = carrying_capacity
        self._cargo: dict[AbstractProduct, int] = {}

    @staticmethod
    def get_requirements(products: dict[AbstractProduct, int]) -> tuple[float, float]:
        required_space = 0.0
        required_mass = 0.0
        for product, amount in products.items():
            required_space += product.volume * amount
            required_mass += product.mass * amount
        return required_space, required_mass

    def can_load(
        self, products: dict[AbstractProduct, int], fill_rate: float = 0.9
    ) -> bool:
        usable_space = self.free_space * fill_rate
        required_space, required_mass = CargoManager.get_requirements(products)

        return required_space <= usable_space and required_mass <= self.free_mass

    def _commit_load(
        self,
        products: dict[AbstractProduct, int],
        required_space: float,
        required_mass: float,
    ) -> None:
        for product, amount in products.items():
            self._cargo[product] = self._cargo.get(product, 0) + amount

        self.free_space -= required_space
        self.free_mass -= required_mass

    def load_products(
        self, products: dict[AbstractProduct, int], fill_rate: float = 0.9
    ) -> None:
        if not self.can_load(products, fill_rate):
            raise ImpossibleLoading("There isn't enough space or carrying capacity in transport")

        required_space, required_mass = CargoManager.get_requirements(products)
        self._commit_load(products, required_space, required_mass)

    def can_unload(self, products: dict[AbstractProduct, int]) -> bool:
        if set(products) - set(self._cargo):
            return False

        for product, amount in products.items():
            if self._cargo[product] < amount:
                return False

        return True

    def _commit_unload(self, products: dict[AbstractProduct, int]) -> None:
        for product, amount in products.items():
            self._cargo[product] -= amount

            if self._cargo[product] == 0:
                del self._cargo[product]

            self.free_space += product.volume * amount
            self.free_mass += product.mass * amount

    def unload_products(self, products: dict[AbstractProduct, int]) -> None:
        if not self.can_unload(products):
            raise ImpossibleUnloading("There isn't enough products in transport")

        self._commit_unload(products)

    def is_empty(self) -> bool:
        return len(self._cargo) == 0
    
    @property
    def cargo(self) -> dict[AbstractProduct, int]:
        return self._cargo.copy()
    
    def get_product_names(self) -> list[str]:
        return list(self._cargo.keys())
