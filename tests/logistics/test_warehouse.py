import pytest
from datetime import date

from company.logistics.transport import Car
from company.logistics.warehouse import Warehouse
from company.products.products import AbstractProduct
from company.common.exceptions import ImpossibleLoading, ImpossibleUnloading

class TestWarehouse:
    @pytest.fixture
    def warehouse(self):
        return Warehouse(capacity=1000.0)
    
    @pytest.fixture
    def simple_product(self):
        class TestProduct(AbstractProduct):
            pass
        return TestProduct(name="Box", volume=1.0, mass=10.0)
    
    @pytest.fixture
    def large_product(self):
        class TestProduct(AbstractProduct):
            pass
        return TestProduct(name="Container", volume=100.0, mass=10.0)
    
    @pytest.fixture
    def car(location):
        return Car(
            transport_id="C1", model="M", production_year=2020, tech_inspection_date=date.today(),
            carrying_capacity=1000.0, capacity=100.0, max_speed=100, current_location=location,
            fuel_consumption=10, fuel_type="Diesel", is_refrigerated=False
        )

    def test_supply(self, warehouse, simple_product):
        products = {simple_product: 50}
        warehouse.supply(products)
        assert warehouse.cargo[simple_product] == 50

    def test_load_transport_from_warehouse(self, warehouse, simple_product, car):
        warehouse.supply({simple_product: 20})
        
        products_to_load = {simple_product: 10}
        warehouse.load_transport(car, products_to_load)
        
        assert warehouse.cargo[simple_product] == 10 
        assert car.cargo[simple_product] == 10 

    def test_unload_transport_to_warehouse(self, warehouse, simple_product, car):
        car._cargo_manager.load_products({simple_product: 10})
        
        warehouse.unload_transport(car, {simple_product: 10})
        
        assert car.is_empty()
        assert warehouse.cargo[simple_product] == 10
        
    def test_load_transport_impossible(self, warehouse, simple_product, car):
        warehouse.supply({simple_product: 20})
        products_to_load = {simple_product: 30}
        
        with pytest.raises(ImpossibleUnloading):
            warehouse.load_transport(car, products_to_load)
            
        car._cargo_manager.load_products({simple_product: 100}, 1)
        products_to_load = {simple_product: 10}
        
        with pytest.raises(ImpossibleLoading):
            warehouse.load_transport(car, products_to_load)
            
    def test_unload_transport_impossible(self, warehouse, simple_product, car, large_product):
        warehouse.supply({large_product: 9},1)
        products_to_unload = {large_product: 1}
        
        with pytest.raises(ImpossibleUnloading):
            warehouse.unload_transport(car, products_to_unload, 1)
            
        products_to_load = {large_product: 1}
        car._cargo_manager.load_products({large_product: 1}, 1)
        with pytest.raises(ImpossibleLoading):
            warehouse.unload_transport(car, products_to_load, 0.9)
            
    def test_supply_impossible(self, warehouse, large_product):
        with pytest.raises(ImpossibleLoading):
            warehouse.supply({large_product: 10})
        