from datetime import date
from typing import Literal, Annotated, Union, Type
from pydantic import BaseModel, Field, ConfigDict, TypeAdapter

from ..common.location import Location
from .enums import CarFuelType, ShipType
from .transport import *


class BaseTransportSchema(BaseModel):
    """
    Base Pydantic model defining shared attributes for all transport types.

    This schema handles validation for common fields like ID, capacity, and physical
    properties. It allows arbitrary types to support the `Location` object.

    Attributes:
        transport_id (str): Unique identifier for the vehicle.
        model (str): The model name or designation.
        production_year (int): Year of manufacture (must be non-negative).
        tech_inspection_date (date): Date of the last technical inspection.
        carrying_capacity (float): Maximum weight the vehicle can carry (must be non-negative).
        capacity (float): Maximum volume available for cargo (must be non-negative).
        max_speed (float): Maximum speed in km/h (must be greater than 0).
        current_location (Location): Current geographical position of the transport.
        fuel_consumption (float): Fuel usage rate (must be non-negative).
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    transport_id: str
    model: str
    production_year: int = Field(ge=0)
    tech_inspection_date: date
    carrying_capacity: float = Field(ge=0)
    capacity: float = Field(ge=0)
    max_speed: float = Field(gt=0)
    current_location: Location
    fuel_consumption: float = Field(ge=0)
    
class TrainSchema(BaseTransportSchema):
    """
    Schema for Train validation.

    Attributes:
        transport_type (Literal["train"]): Discriminator field fixed to "train".
        track_gauge (float): Width of the track gauge (must be non-negative).
        wagons (list[Wagon] | None): List of attached wagons, if any.
    """
    transport_type: Literal["train"]
    track_gauge: float = Field(ge=0)
    wagons: list[Wagon] | None


class PlaneSchema(BaseTransportSchema):
    """
    Schema for Plane validation.

    Attributes:
        transport_type (Literal["plane"]): Discriminator field fixed to "plane".
        max_height (float): Maximum flight altitude (must be non-negative).
        max_range (float): Maximum flight distance without refueling (must be non-negative).
        runway_length_required (float): Minimum runway length needed for takeoff (must be non-negative).
    """
    transport_type: Literal["plane"]
    max_height: float = Field(ge=0)
    max_range: float = Field(ge=0)
    runway_length_required: float = Field(ge=0)


class CarSchema(BaseTransportSchema):
    """
    Schema for Car validation.

    Attributes:
        transport_type (Literal["car"]): Discriminator field fixed to "car".
        fuel_type (CarFuelType | str): Type of fuel used (Enum or string).
        is_refrigerated (bool): Indicates if the car has a refrigeration unit.
    """
    transport_type: Literal["car"]
    fuel_type: CarFuelType | str
    is_refrigerated: bool


class ShipSchema(BaseTransportSchema):
    """
    Schema for Ship validation.

    Attributes:
        transport_type (Literal["ship"]): Discriminator field fixed to "ship".
        ship_type (ShipType | str): Classification of the ship (Enum or string).
        max_draft (float): Maximum depth of the ship's keel below the waterline (must be non-negative).
    """
    transport_type: Literal["ship"]
    ship_type: ShipType | str
    max_draft: float = Field(ge=0)


TransportInput = Annotated[
    Union[TrainSchema, PlaneSchema, CarSchema, ShipSchema],
    Field(discriminator="transport_type"),
]
"""
Union type for all transport schemas, discriminated by the `transport_type` field.
Used for polymorphic validation where the specific type is determined at runtime.
"""


transport_validator = TypeAdapter(TransportInput)
"""
Pydantic TypeAdapter configured to validate data against the `TransportInput` union.
"""


class TransportFactory:
    """
    Factory class for creating domain transport objects from raw data.

    This factory uses Pydantic schemas to validate input data before instantiating
    the corresponding domain class (e.g., `Train`, `Plane`, `Car`, `Ship`).
    """
    _map: dict[str, Type[AbstractTransport]] = {
        "train": Train,
        "plane": Plane,
        "car": Car,
        "ship": Ship,
    }


    def create_by_params(self, **raw_data) -> AbstractTransport:
        """
        Create a validated transport instance from a dictionary of parameters.

        This method first validates the `raw_data` against the `TransportInput` schema
        to ensure data integrity. It then determines the correct domain class based
        on `transport_type` and instantiates it.

        Args:
            **raw_data: Arbitrary keyword arguments representing transport data.
                        Must include 'transport_type'.

        Returns:
            AbstractTransport: An instance of a concrete transport class (Train, Car, etc.).

        Raises:
            ValidationError: If the input data does not match the required schema.
            KeyError: If the transport type is not found in the internal map.
        """
        model = transport_validator.validate_python(raw_data)
        valid_data = model.model_dump()


        transport_type = valid_data.pop("transport_type")
        transport_cls = self._map[transport_type]


        return transport_cls(**valid_data)
