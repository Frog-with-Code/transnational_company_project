import pytest
from datetime import date
from pydantic import ValidationError

from company.logistics.transport_factory import TransportFactory
from company.logistics.transport import Car, Train, Plane, Ship
from company.logistics.enums import CarFuelType, ShipType
from math import isclose


class TestTransportFactory:
    @pytest.fixture
    def factory(self):
        return TransportFactory()

    @pytest.fixture
    def base_params(self, location):
        return {
            "transport_id": "TEST-001",
            "model": "Generic Transport",
            "production_year": 2023,
            "tech_inspection_date": date(2024, 1, 1),
            "carrying_capacity": 1000.0,
            "capacity": 100.0,
            "max_speed": 60.0,
            "current_location": location,
            "fuel_consumption": 10.0
        }

    def test_create_car(self, factory, base_params):
        params = {
            **base_params,
            "transport_type": "car",
            "fuel_type": CarFuelType.DIESEL,
            "is_refrigerated": True
        }
        
        transport = factory.create_by_params(**params)
        
        assert isinstance(transport, Car)
        assert transport.transport_id == "TEST-001"
        assert transport.fuel_type == CarFuelType.DIESEL
        assert transport.is_refrigerated is True

    def test_create_car_with_string_enum(self, factory, base_params):
        params = {
            **base_params,
            "transport_type": "car",
            "fuel_type": "Diesel",
            "is_refrigerated": False
        }
        
        transport = factory.create_by_params(**params)
        assert isinstance(transport, Car)
        assert transport.fuel_type == CarFuelType.DIESEL

    def test_create_train(self, factory, base_params):
        params = {
            **base_params,
            "transport_type": "train",
            "track_gauge": 1520.0,
            "wagons": []
        }
        
        transport = factory.create_by_params(**params)
        
        assert isinstance(transport, Train)
        assert isclose(transport.track_gauge, 1520.0)
        assert transport.wagon_num == 0

    def test_create_plane(self, factory, base_params):
        params = {
            **base_params,
            "transport_type": "plane",
            "max_height": 10000.0,
            "max_range": 5000.0,
            "runway_length_required": 2000.0
        }
        
        transport = factory.create_by_params(**params)
        
        assert isinstance(transport, Plane)
        assert isclose(transport.max_height, 10000.0)
        assert isclose(transport.max_range, 5000.0)
        assert isclose(transport.runway_length_required, 2000.0)

    def test_create_ship(self, factory, base_params):
        params = {
            **base_params,
            "transport_type": "ship",
            "ship_type": ShipType.TANKER,
            "max_draft": 20.0
        }
        
        transport = factory.create_by_params(**params)
        
        assert isinstance(transport, Ship)
        assert transport.ship_type == ShipType.TANKER
        assert transport.max_draft == 20.0

    def test_validation_error_missing_field(self, factory, base_params):
        params = {
            **base_params,
            "transport_type": "car",
            "fuel_type": CarFuelType.DIESEL
        }
        
        with pytest.raises(ValidationError):
            factory.create_by_params(**params)

    def test_validation_error_invalid_type(self, factory, base_params):
        params = {
            **base_params,
            "transport_type": "plane",
            "max_height": "очень высоко",
            "max_range": 5000.0,
            "runway_length_required": 2000.0
        }
        
        with pytest.raises(ValidationError):
            factory.create_by_params(**params)

    def test_unknown_transport_type(self, factory, base_params):
        params = {
            **base_params,
            "transport_type": "spaceship",
        }
        
        with pytest.raises(ValidationError):
            factory.create_by_params(**params)

    def test_negative_values_validation(self, factory, base_params):
        params = {
            **base_params,
            "transport_type": "train",
            "track_gauge": -100.0 
        }
        
        with pytest.raises(ValidationError):
            factory.create_by_params(**params)
