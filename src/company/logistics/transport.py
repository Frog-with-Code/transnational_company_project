from abc import ABC
from enums import *
from ..common.location import Location
from ..hr.employees import AbstractEmployee
from ..products.products import AbstractProduct
from datetime import date
from ..common.enums import normalize_enum
from math import isclose
from dataclasses import dataclass


class AbstractTransport(ABC):
    specific_fields: set[str] = set()
    common_fields: set[str] = {
        "transport_id",
        "model",
        "production_year",
        "tech_inspection_date",
        "carrying_capacity",
        "capacity",
        "max_speed",
        "current_location",
        "fuel_consumption",
    }

    def __init__(
        self,
        *,
        transport_id: str,
        model: str,
        production_year: int,
        tech_inspection_date: date,
        carrying_capacity: float,
        capacity: float,
        max_speed: float,
        current_location: Location,
        fuel_consumption: float
    ):
        self.transport_id = transport_id
        self.model = model
        self.production_year = production_year
        self.tech_inspection_date = tech_inspection_date
        self.carrying_capacity = carrying_capacity
        self.capacity = capacity
        self.max_speed = max_speed
        self.current_location = current_location
        self.fuel_consumption = fuel_consumption

        self.workers: set[AbstractEmployee] = set()
        self.status: TransportStatus = TransportStatus.AVAILABLE
        self.cargo: dict[AbstractProduct, int] = dict()
        self.free_space: float = self.capacity
        self.free_mass: float = self.carrying_capacity

    def get_model_info(self) -> dict:
        return {
            "model": self.model,
            "production_year": self.production_year,
            "carrying_capacity": self.carrying_capacity,
            "capacity": self.capacity,
            "max_speed": self.max_speed,
            "fuel_consumption": self.fuel_consumption,
        }

    def can_work(self) -> bool:
        return self.status == TransportStatus.AVAILABLE

    def add_worker(self, worker: AbstractEmployee) -> None:
        self.workers.add(worker)

    def remove_worker(self, worker: AbstractEmployee) -> None:
        self.workers.discard(worker)

    def calculate_min_delivery_time(self, distance: float) -> float:
        return distance / self.max_speed

    def calculate_fuel_cost(self, distance: float, fuel_price: float) -> float:
        return distance / 100 * self.fuel_consumption * fuel_price

    def load_products(
        self, products: dict[AbstractProduct, int], fill_rate: float
    ) -> bool:
        self.status = TransportStatus.LOADING
        free_space = self.capacity * fill_rate
        required_space = 0
        required_mass = 0
        for product in products.keys():
            required_space += product.volume * products[product]
            required_mass += product.mass * products[product]

        if required_space <= free_space and required_mass <= self.carrying_capacity:
            for product in products.keys():
                if product in self.cargo:
                    self.cargo[product] += products[product]
                else: self.cargo[product] = products[product]

            self.free_mass = self.free_mass - required_mass
            self.free_space = self.free_space - required_space
            return True
        else:
            return False

    def unload_products(self, products: dict[AbstractProduct, int]) -> bool:
        self.status = TransportStatus.UNLOADING
        if not set(products) - set(self.cargo):
            return False
        target_products = self.cargo & products
        for product in target_products:
            if self.cargo[target_products] < products[product]:
                return False

        for product in target_products:
            self.cargo[product] = self.cargo[product] - products[product]
            self.free_space -= product.volume * products[product]
            self.free_mass -= product.mass * products[product]

        return True

    def delivery(self, destination: Location) -> None:
        self.status = TransportStatus.IN_TRANSIT
        self.current_location = destination

    @classmethod
    def get_specific_fields(cls) -> set[str]:
        return cls.specific_fields

    @classmethod
    def get_necessary_fields(cls) -> set[str]:
        return cls.specific_fields | cls.common_fields


@dataclass
class Wagon:
    capacity: float
    carrying_capacity: float


class Train(AbstractTransport):
    specific_fields = {"wagons", "track_gauge"}

    def __init__(
        self, wagons: list[Wagon] | None, track_gauge: float, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        if wagons is None:
            self.wagons = []
            self.wagon_num = 0
        else:
            self.wagons = wagons
            self.wagon_num = len(wagons)
            for wagon in wagons:
                self._add_wagon_capacities(wagon)
        self.track_gauge = track_gauge

    def _add_wagon_capacities(self, wagon: Wagon) -> None:
        self.capacity += wagon.capacity
        self.carrying_capacity += wagon.carrying_capacity

    def is_tracks_compatible(self, track_gauge: float) -> bool:
        return isclose(self.track_gauge, track_gauge)

    def attach_wagon(self, wagon: Wagon) -> None:
        self.wagon_num += 1
        self._add_wagon_capacities(wagon)

    def detach_wagon(
        self, wagon_capacity: float, wagon_carrying_capacity: float
    ) -> Wagon:
        if (
            wagon_capacity < self.free_space
            and wagon_carrying_capacity < self.free_mass
        ):
            for wagon in self.wagons:
                if isclose(wagon.capacity, wagon_capacity) and isclose(
                    wagon.carrying_capacity, wagon_carrying_capacity
                ):
                    self.wagons.remove(wagon)
                    self.capacity -= wagon.capacity
                    self.carrying_capacity -= wagon.carrying_capacity
                    self.wagon_num -= 1
                    return wagon
        return None


class Plane(AbstractTransport):
    specific_fields = {"max_height", "max_range", "runway_length_required"}

    def __init__(
        self,
        max_height: float,
        max_range: float,
        runway_length_required: float,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.max_height = max_height
        self.max_range = max_range
        self.runway_length_required = runway_length_required
        
    def can_take_off(self, runway_length: float) -> bool:
        return runway_length >= self.runway_length_required

    def calculate_flight_range(self) -> float:
        free_percent = (self.free_space / self.capacity)
        factor = max(free_percent, 0.5)
        return self.max_range * factor

class Car(AbstractTransport):
    specific_fields = {"fuel_type", "is_refrigerated"}

    def __init__(self, fuel_type: CarFuelType | str, is_refrigerated: bool, **kwargs):
        super().__init__(**kwargs)
        self.fuel_type = normalize_enum(fuel_type, CarFuelType)
        self.is_refrigerated = is_refrigerated
        
    def is_fuel_compatible(self, fuel_type: CarFuelType) -> bool:
        return self.fuel_type == fuel_type


class Ship(AbstractTransport):
    specific_fields = {"ship_type"}

    def __init__(self, ship_type: ShipType | str, max_draft: float, **kwargs):
        super().__init__(**kwargs)
        self.fuel = normalize_enum(ship_type, ShipType)
        self.max_draft = max_draft
        
    def can_draft(self, chanel_depth: float) -> bool:
        return self.max_draft > chanel_depth 
