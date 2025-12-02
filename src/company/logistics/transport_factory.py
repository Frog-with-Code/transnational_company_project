from datetime import date
from typing import Literal, Annotated, Union, Type
from pydantic import BaseModel, Field, ConfigDict, TypeAdapter

from ..common.location import Location
from ..hr.employees import AbstractEmployee
from ..products.products import AbstractProduct
from .enums import TransportStatus, CarFuelType, ShipType
from .transport import *

class BaseTransportSchema(BaseModel):
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
    transport_type: Literal["train"]
    track_gauge: float = Field(ge=0)

class PlaneSchema(BaseTransportSchema):
    transport_type: Literal["plane"]
    max_height: float = Field(ge=0)
    max_range: float = Field(ge=0)
    runway_length_required: float = Field(ge=0)

class CarSchema(BaseTransportSchema):
    transport_type: Literal["car"]
    fuel_type: CarFuelType | str
    is_refrigerated: bool

class ShipSchema(BaseTransportSchema):
    transport_type: Literal["ship"]
    ship_type: ShipType | str
    max_draft: float = Field(ge=0)

TransportInput = Annotated[
    Union[TrainSchema, PlaneSchema, CarSchema, ShipSchema],
    Field(discriminator="transport_type"),
]

transport_validator = TypeAdapter(TransportInput)

class TransportFactory:
    _map: dict[str, Type[AbstractTransport]] = {
        "train": Train,
        "plane": Plane,
        "car": Car,
        "ship": Ship,
    }

    def create_by_params(self, **raw_data) -> AbstractTransport:
        model = transport_validator.validate_python(raw_data)
        valid_data = model.model_dump()

        transport_type = valid_data.pop("transport_type")
        transport_cls = self._map[transport_type]

        return transport_cls(**valid_data)

