import pytest

from company.products.products import AbstractProduct
from company.products.products import AbstractProduct
from company.logistics.cargo_manager import CargoManager
from company.common.exceptions import ImpossibleLoading, ImpossibleUnloading


class TestCargoManager:
    @pytest.fixture
    def simple_product(self):
        class TestProduct(AbstractProduct):
            pass
        return TestProduct(name="Box", volume=1.0, mass=10.0)

    @pytest.fixture
    def heavy_product(self):
        class TestProduct(AbstractProduct):
            pass
        return TestProduct(name="Iron", volume=0.5, mass=100.0)

    @pytest.fixture
    def cargo_manager(self):
        return CargoManager(capacity=100.0, carrying_capacity=1000.0)
    
    def test_initial_state(self, cargo_manager):
        assert cargo_manager.free_space == 100.0
        assert cargo_manager.free_mass == 1000.0
        assert cargo_manager.is_empty() is True

    def test_load_success(self, cargo_manager, simple_product):
        products = {simple_product: 10}
        cargo_manager.load_products(products)
        
        assert cargo_manager.free_space == 90.0
        assert cargo_manager.free_mass == 900.0
        assert cargo_manager.cargo[simple_product] == 10
        assert not cargo_manager.is_empty()

    def test_load_fail_capacity(self, cargo_manager, simple_product):
        products = {simple_product: 101}
        with pytest.raises(ImpossibleLoading):
            cargo_manager.load_products(products)

    def test_load_fail_mass(self, cargo_manager, heavy_product):
        products = {heavy_product: 11}
        with pytest.raises(ImpossibleLoading):
            cargo_manager.load_products(products)

    def test_unload_success(self, cargo_manager, simple_product):
        cargo_manager.load_products({simple_product: 10})
        cargo_manager.unload_products({simple_product: 5})
        
        assert cargo_manager.cargo[simple_product] == 5
        assert cargo_manager.free_space == 95.0
        assert cargo_manager.free_mass == 950.0

    def test_unload_fail_missing(self, cargo_manager, simple_product):
        with pytest.raises(ImpossibleUnloading):
            cargo_manager.unload_products({simple_product: 1})

    def test_fill_rate_limit(self, cargo_manager, simple_product):
        products = {simple_product: 60}
        
        with pytest.raises(ImpossibleLoading):
            cargo_manager.load_products(products, fill_rate=0.5)

