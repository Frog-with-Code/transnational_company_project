from abc import ABC
from math import isclose
from dataclasses import dataclass, fields
from datetime import date

from .enums import *
from ..common.location import Location
from ..hr.employees import AbstractEmployee
from ..products.products import AbstractProduct
from ..common.enums import normalize_enum
from .cargo_manager import CargoManager
from ..hr.employee_manager import EmployeeManagerMixin
from ..common.descriptors import NonNegative
from ..common.validation import validate_non_negative
from ..common.exceptions import ImpossibleUnloading


class AbstractTransport(ABC, EmployeeManagerMixin):
    """
    Abstract base class representing a generic transport vehicle.

    Integrates cargo management (via CargoManager) and employee management 
    (via EmployeeManagerMixin). It enforces non-negative constraints on physical 
    attributes.

    Attributes:
        production_year (int): Year of manufacture.
        carrying_capacity (float): Max weight capacity (kg/tons).
        capacity (float): Max volume capacity (cubic meters).
        max_speed (float): Maximum speed (km/h).
        fuel_consumption (float): Fuel usage per 100km (or relevant unit).
        transport_id (str): Unique identifier.
        model (str): Vehicle model name.
        tech_inspection_date (date): Date of last technical inspection.
        current_location (Location): Current geographical location.
        status (TransportStatus): Current operational status (e.g., AVAILABLE, LOADING).
    """
    production_year = NonNegative()
    carrying_capacity = NonNegative()
    capacity = NonNegative()
    max_speed = NonNegative()
    fuel_consumption = NonNegative()
    
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
        super().__init__()
        self.transport_id = transport_id
        self.model = model
        self.production_year = production_year
        self.tech_inspection_date = tech_inspection_date
        self.carrying_capacity = carrying_capacity
        self.capacity = capacity
        self.max_speed = max_speed
        self.current_location = current_location
        self.fuel_consumption = fuel_consumption

        self._employees: set[AbstractEmployee] = set()
        self.status: TransportStatus = TransportStatus.AVAILABLE
        self._cargo_manager = CargoManager(self.capacity, self.carrying_capacity)

    @property
    def model_info(self) -> dict:
        """
        Get a summary of the transport's physical specifications.

        Returns:
            dict: Dictionary containing model, year, capacities, speed, and fuel info.
        """
        return {
            "model": self.model,
            "production_year": self.production_year,
            "carrying_capacity": self.carrying_capacity,
            "capacity": self.capacity,
            "max_speed": self.max_speed,
            "fuel_consumption": self.fuel_consumption,
        }

    def can_work(self) -> bool:
        """
        Check if the transport is available for new assignments.

        Returns:
            bool: True if status is AVAILABLE, False otherwise.
        """
        return self.status == TransportStatus.AVAILABLE

    def calculate_min_delivery_time(self, distance: float) -> float:
        """
        Calculate the minimum time required to travel a specific distance.

        Args:
            distance (float): The distance to travel (must be non-negative).

        Returns:
            float: Time in hours.
        """
        validate_non_negative(distance)
        return distance / self.max_speed

    def calculate_fuel_cost(self, distance: float, fuel_price: float) -> float:
        """
        Calculate the cost of fuel for a specific trip.

        Args:
            distance (float): Trip distance.
            fuel_price (float): Price per unit of fuel.

        Returns:
            float: Total fuel cost based on consumption rate.
        """
        validate_non_negative(distance, fuel_price)
        return distance / 100 * self.fuel_consumption * fuel_price

    def can_load(self, products: dict[AbstractProduct, int], fill_rate: float) -> bool:
        """
        Check if products can be loaded into the transport.

        Args:
            products (dict[AbstractProduct, int]): Products to load.
            fill_rate (float): Packing efficiency coefficient.

        Returns:
            bool: True if products fit in available space/mass.
        """
        validate_non_negative(fill_rate)
        return self._cargo_manager.can_load(products, fill_rate)

    def can_unload(self, products: dict[AbstractProduct, int]) -> bool:
        """
        Check if specific products can be unloaded.

        Args:
            products (dict[AbstractProduct, int]): Products to unload.

        Returns:
            bool: True if products exist in cargo.
        """
        return self._cargo_manager.can_unload(products)

    def load_products(
        self, products: dict[AbstractProduct, int], fill_rate: float
    ) -> bool:
        """
        Attempt to load products into the transport.

        Updates status to LOADING during operation. Prints success/failure message.

        Args:
            products (dict[AbstractProduct, int]): Products to load.
            fill_rate (float): Packing efficiency coefficient.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        self.status = TransportStatus.LOADING
        success = self._cargo_manager.load_products(products, fill_rate)
        (
            print("Goods was successfully loaded")
            if success
            else print("Loading is impossible")
        )
        return success

    def unload_products(self, products: dict[AbstractProduct, int]) -> bool:
        """
        Attempt to unload products from the transport.

        Updates status to UNLOADING during operation. Prints success/failure message.

        Args:
            products (dict[AbstractProduct, int]): Products to unload.

        Returns:
            bool: True if unloading was successful, False otherwise.
        """
        self.status = TransportStatus.UNLOADING
        success = self._cargo_manager.unload_products(products)
        (
            print("Goods was successfully unloaded")
            if success
            else print("Unloading is impossible")
        )
        return success

    def delivery(self, destination: Location) -> None:
        """
        Simulate a delivery trip to a destination.

        Updates status to IN_TRANSIT and changes current_location.

        Args:
            destination (Location): The target location.
        """
        self.status = TransportStatus.IN_TRANSIT
        self.current_location = destination

    @classmethod
    def get_specific_fields(cls) -> set[str]:
        """
        Get fields specific to the concrete transport class.

        Returns:
            set[str]: A set of field names.
        """
        return cls.specific_fields

    @classmethod
    def get_necessary_fields(cls) -> set[str]:
        """
        Get all required fields for initialization (common + specific).

        Returns:
            set[str]: A combined set of field names.
        """
        return cls.specific_fields | cls.common_fields
    
    def get_product_names(self) -> list[str]:
        """
        Get a list of product keys currently loaded.

        Returns:
            list[str]: List of product identifiers/objects.
        """
        return self._cargo_manager.get_product_names()
    
    @property
    def cargo(self) -> dict[AbstractProduct, int]:
        """
        Get current cargo inventory.

        Returns:
            dict[AbstractProduct, int]: Copy of the cargo dictionary.
        """
        return self._cargo_manager.cargo
    
    def is_empty(self) -> bool:
        """
        Check if transport has no cargo.

        Returns:
            bool: True if empty.
        """
        return self._cargo_manager.is_empty()


@dataclass
class Wagon:
    """
    Data class representing a train wagon.

    Attributes:
        capacity (float): Volume capacity.
        carrying_capacity (float): Weight capacity.
    """
    capacity: float
    carrying_capacity: float
    
    def __post_init__(self):
        """Validate that capacity fields are non-negative."""
        for field in fields(self):
            value = getattr(self, field.name)
            validate_non_negative(value)


class Train(AbstractTransport):
    """
    Represents a train which is composed of multiple wagons.

    The total capacity of the train is the sum of its wagons.
    """
    track_gauge = NonNegative()
    
    def __init__(
        self, track_gauge: float, wagons: list[Wagon] | None, **kwargs
    ) -> None:
        """
        Initialize a Train.

        Args:
            track_gauge (float): The width of the track gauge.
            wagons (list[Wagon] | None): Initial list of attached wagons.
            **kwargs: Arguments passed to AbstractTransport.
        """
        super().__init__(**kwargs)
        if wagons is None:
            self._wagons = []
            self.wagon_num = 0
        else:
            self._wagons = wagons
            self.wagon_num = len(wagons)
            for wagon in wagons:
                self._add_wagon_capacities(wagon)
                
        self.track_gauge = track_gauge

    def _capture_cargo(self, wagon: Wagon) -> None:
        """
        Increase train capacity by the wagon's capacity.

        Args:
            wagon (Wagon): The wagon being added.
        """
        self.capacity += wagon.capacity
        self.carrying_capacity += wagon.carrying_capacity
        self._cargo_manager.free_space += wagon.capacity
        self._cargo_manager.free_mass += wagon.carrying_capacity

    def _release_cargo(self, wagon: Wagon) -> None:
        """
        Decrease train capacity by the wagon's capacity.

        Args:
            wagon (Wagon): The wagon being removed.
        """
        self.capacity -= wagon.capacity
        self.carrying_capacity -= wagon.carrying_capacity
        self._cargo_manager.free_space -= wagon.capacity
        self._cargo_manager.free_mass -= wagon.carrying_capacity

    def is_tracks_compatible(self, track_gauge: float) -> bool:
        """
        Check if the train fits a specific track gauge.

        Args:
            track_gauge (float): The gauge to check against.

        Returns:
            bool: True if gauges match (using float tolerance).
        """
        validate_non_negative(track_gauge)
        return isclose(self.track_gauge, track_gauge)

    def attach_wagon(self, wagon: Wagon) -> None:
        """
        Attach a new wagon to the train, increasing total capacity.

        Args:
            wagon (Wagon): Wagon to attach.
        """
        self.wagon_num += 1
        self._wagons.append(wagon)
        self._capture_cargo(wagon)

    def detach_wagon(
        self, wagon_capacity: float, wagon_carrying_capacity: float
    ) -> Wagon:
        """
        Detach a wagon matching the specified parameters.

        Args:
            wagon_capacity (float): The volume capacity of the wagon to find.
            wagon_carrying_capacity (float): The weight capacity of the wagon to find.

        Returns:
            Wagon: The detached wagon object if found.
            None: If no matching wagon is found.

        Raises:
            ImpossibleUnloading: If removing the wagon would leave insufficient space/mass 
                                 for the currently loaded cargo.
        """
        validate_non_negative(wagon_capacity, wagon_carrying_capacity)
        if (
            self._cargo_manager.free_space - wagon_capacity < 0
            or self._cargo_manager.free_mass - wagon_carrying_capacity < 0
        ):
            raise ImpossibleUnloading("Can't detach wagon with cargo")
        
        for wagon in self._wagons:
            if isclose(wagon.capacity, wagon_capacity) and isclose(
                wagon.carrying_capacity, wagon_carrying_capacity
            ):
                self._wagons.remove(wagon)
                self.wagon_num -= 1
                self._release_cargo(wagon)
                return wagon
        return None


class Plane(AbstractTransport):
    """
    Represents an aircraft transport.
    """
    max_height = NonNegative()
    max_range = NonNegative()
    runway_length_required = NonNegative()
    
    def __init__(
        self,
        max_height: float,
        max_range: float,
        runway_length_required: float,
        **kwargs
    ):
        """
        Initialize a Plane.

        Args:
            max_height (float): Service ceiling.
            max_range (float): Maximum flight range at optimal load.
            runway_length_required (float): Required runway length for takeoff.
            **kwargs: Arguments passed to AbstractTransport.
        """
        super().__init__(**kwargs)
        self.max_height = max_height
        self.max_range = max_range
        self.runway_length_required = runway_length_required

    def can_take_off(self, runway_length: float) -> bool:
        """
        Check if a runway is long enough for this plane.

        Args:
            runway_length (float): Length of the available runway.

        Returns:
            bool: True if sufficient, False otherwise.
        """
        validate_non_negative(runway_length)
        return runway_length >= self.runway_length_required

    def calculate_flight_range(self) -> float:
        """
        Calculate flight range based on current cargo load.

        The range is reduced as cargo mass increases, down to a minimum of 50% max range.

        Returns:
            float: The calculated range.
        """
        free_percent = self._cargo_manager.free_mass / self.carrying_capacity
        factor = max(free_percent, 0.5)
        return self.max_range * factor


class Car(AbstractTransport):
    """
    Represents a road vehicle.
    """
    def __init__(self, fuel_type: CarFuelType | str, is_refrigerated: bool, **kwargs):
        """
        Initialize a Car.

        Args:
            fuel_type (CarFuelType | str): Type of fuel (e.g., BENZIN, DIESEL).
            is_refrigerated (bool): Whether the car has temperature control.
            **kwargs: Arguments passed to AbstractTransport.
        """
        super().__init__(**kwargs)
        self.fuel_type = normalize_enum(fuel_type, CarFuelType)
        self.is_refrigerated = is_refrigerated

    def is_fuel_compatible(self, fuel_type: CarFuelType) -> bool:
        """
        Check if the car is compatible with a specific fuel type.

        Args:
            fuel_type (CarFuelType): Fuel to check.

        Returns:
            bool: True if compatible.
        """
        return self.fuel_type == fuel_type


class Ship(AbstractTransport):
    """
    Represents a watercraft transport.
    """
    max_draft = NonNegative()
    
    def __init__(self, ship_type: ShipType | str, max_draft: float, **kwargs):
        """
        Initialize a Ship.

        Args:
            ship_type (ShipType | str): Classification of the ship.
            max_draft (float): The vertical distance between the waterline and the bottom of the hull.
            **kwargs: Arguments passed to AbstractTransport.
        """
        super().__init__(**kwargs)
        self.ship_type = normalize_enum(ship_type, ShipType)
        self.max_draft = max_draft

    def can_draft(self, chanel_depth: float) -> bool:
        """
        Check if the ship's draft is strictly greater than the channel depth.

        Note:
            Logic suggests this returns True if the ship is too deep for the channel.

        Args:
            chanel_depth (float): Depth of the water channel.

        Returns:
            bool: True if max_draft > chanel_depth.
        """
        validate_non_negative(chanel_depth)
        return self.max_draft > chanel_depth
