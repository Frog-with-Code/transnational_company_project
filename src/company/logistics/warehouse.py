from ..products.products import AbstractProduct
from ..hr.employees import AbstractEmployee
from transport import AbstractTransport


class Warehouse:
    def __init__(self, capacity: float, workers: set[AbstractEmployee] | None) -> None:
        self.capacity = capacity
        if workers is None:
            self.workers = []
        else:
            self.workers = workers.copy()

        self.products: dict[AbstractProduct, int] = dict()

    def load_transport(
        self, transport: AbstractTransport, target_products: dict[AbstractProduct, int]
    ) -> bool:
        if not set(target_products) - set(self.products):
            return False

        for product in target_products.keys():
            if target_products[product] < self.products[product]:
                return False
            
        if transport.load_products(target_products):
            pass