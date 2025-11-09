from transport import *
from pathlib import Path
import json


class TransportFactory:
    transport_types = {"train": Train, "plane": Plane, "car": Car, "ship": Ship}

    def __init__(self) -> None:
        pass

    def create_by_params(
        self,
        *,
        transport_type: AbstractTransport,
        transport_id: str,
        model: str,
        production_year: int,
        tech_inspection_date: date,
        carrying_capacity: float,
        capacity: float,
        max_speed: float,
        current_location: Location,
        fuel_consumption: float,
        **kwargs
    ) -> AbstractTransport:
        transport_class = TransportFactory.transport_types[transport_type]
        return transport_class(
            transport_id=transport_id,
            model=model,
            production_year=production_year,
            tech_inspection_date=tech_inspection_date,
            carrying_capacity=carrying_capacity,
            capacity=capacity,
            max_speed=max_speed,
            current_location=current_location,
            fuel_consumption=fuel_consumption,
            **kwargs
        )

    def create_from_file(self, abs_path: Path) -> None:
        with open(abs_path) as f:
            data = json.load(f)["transport"]

        # TODO implement location parsing
        transport_class = TransportFactory.transport_types[data["transport_type"]]

        required_fields = transport_class.get_necessary_fields()
        provided_fields = set(data.keys())
        provided_fields.remove("transport_type")
        if required_fields - provided_fields:
            raise ValueError

        specific_fields = {
            key: data[key] for key in transport_class.get_specific_fields()
        }
        return transport_class(data)
