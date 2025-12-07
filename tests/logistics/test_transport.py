import pytest
from datetime import date
from math import isclose

from company.logistics.transport import *
from company.common.location import Location, Region
from company.common.exceptions import ImpossibleUnloading
from company.products.products import AbstractProduct


class BaseTransportTest:
    @pytest.fixture
    def transport(self):
        raise NotImplementedError

    def test_calculate_delivery_time(self, transport):
        dist = transport.max_speed * 2
        assert transport.calculate_min_delivery_time(dist) == 2.0

    def test_fuel_cost_calculation(self, transport):
        dist = 100
        price = 2.0
        expected = (dist / 100.0) * transport.fuel_consumption * price
        assert isclose(transport.calculate_fuel_cost(dist, price), expected)

    def test_delivery_status_change(self, transport):
        dest = Location(Region.ASIA, "China", "Beijing", "Road", "1")
        transport.delivery(dest)
        assert transport.status == TransportStatus.IN_TRANSIT


class TestCar(BaseTransportTest):
    @pytest.fixture
    def transport(self, location):
        return Car(
            transport_id="CAR-001",
            model="Tesla Semi",
            production_year=2023,
            tech_inspection_date=date(2024, 1, 1),
            carrying_capacity=2000.0,
            capacity=50.0,
            max_speed=100.0,
            current_location=location,
            fuel_consumption=15.0,
            fuel_type=CarFuelType.ELECTRICITY,
            is_refrigerated=True,
        )

    @pytest.fixture
    def car(self, transport):
        return transport

    def test_fuel_compatibility(self, car):
        assert car.is_fuel_compatible(CarFuelType.ELECTRICITY) is True
        assert car.is_fuel_compatible(CarFuelType.DIESEL) is False

    def test_refrigeration(self, car):
        assert car.is_refrigerated is True


class TestTrain(BaseTransportTest):
    @pytest.fixture
    def heavy_product(self):
        class TestProduct(AbstractProduct):
            pass

        return TestProduct(name="Iron", volume=5, mass=1000.0)

    @pytest.fixture
    def transport(self, location):
        return Train(
            transport_id="TRAIN-01",
            model="Locomotive",
            production_year=2020,
            tech_inspection_date=date(2024, 1, 1),
            carrying_capacity=0,
            capacity=0,
            max_speed=80.0,
            current_location=location,
            fuel_consumption=50.0,
            wagons=[],
            track_gauge=1520.0,
        )

    @pytest.fixture
    def train(self, transport):
        return transport

    def test_wagons_attaching_detaching(self, train):
        wagon = Wagon(capacity=100.0, carrying_capacity=5000.0)
        train.attach_wagon(wagon)

        assert train.wagon_num == 1
        assert train.capacity == 100.0
        assert train.carrying_capacity == 5000.0

        detached = train.detach_wagon(100.0, 5000.0)
        assert detached == wagon
        assert train.wagon_num == 0
        assert train.capacity == 0

    def test_wagon_loading_restrictions(self, train, heavy_product):
        train.attach_wagon(Wagon(capacity=100.0, carrying_capacity=5000.0))
        train.attach_wagon(Wagon(capacity=50.0, carrying_capacity=2500.0))

        train.load_products({heavy_product: 4}, 1)

        assert isclose(train._cargo_manager.free_mass, 3500.0)

        with pytest.raises(ImpossibleUnloading, match="Can't detach wagon with cargo"):
            train.detach_wagon(100.0, 5000.0)

        train.detach_wagon(50.0, 2500.0)
        assert train.wagon_num == 1
        assert isclose(train._cargo_manager.free_mass, 1000.0)


class TestPlane(BaseTransportTest):
    @pytest.fixture
    def transport(self, location):
        return Plane(
            transport_id="BOEING-747",
            model="747",
            production_year=2019,
            tech_inspection_date=date(2024, 1, 1),
            carrying_capacity=50000.0,
            capacity=500.0,
            max_speed=900.0,
            current_location=location,
            fuel_consumption=1000.0,
            max_height=10000.0,
            max_range=8000.0,
            runway_length_required=3000.0,
        )

    @pytest.fixture
    def plane(self, transport):
        return transport

    def test_take_off_conditions(self, plane):
        assert plane.can_take_off(3500.0) is True
        assert plane.can_take_off(2500.0) is False

    def test_flight_range(self, plane):
        assert plane.calculate_flight_range() == 8000.0


class TestShip(BaseTransportTest):
    @pytest.fixture
    def transport(self, location):
        return Ship(
            transport_id="SHIP-01",
            model="Evergiven",
            production_year=2015,
            tech_inspection_date=date(2024, 1, 1),
            carrying_capacity=100000.0,
            capacity=5000.0,
            max_speed=40.0,
            current_location=location,
            fuel_consumption=500.0,
            ship_type=ShipType.CONTAINERSHIP,
            max_draft=15.0,
        )

    @pytest.fixture
    def ship(self, transport):
        return transport

    def test_draft_check(self, ship):
        assert ship.can_draft(10.0) is True
