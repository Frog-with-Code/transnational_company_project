import pytest

from company.hr.employee_manager import EmployeeManagerMixin
from company.hr.employees import Seller
from company.hr.enums import EmployeeRole, EmployeeClassification
from company.finance.budget import Money, Currency
from company.common.exceptions import EmployeeAlreadyHiredError, EmployeeNotHiredError

class FakeCompany(EmployeeManagerMixin):
    def __init__(self):
        self._employees = set()

class TestEmployeeManager:
    @pytest.fixture
    def manager(self):
        return FakeCompany()

    @pytest.fixture
    def employee(self):
        return Seller(
            name="Alice", surname="Seller", personal_id=1,
            role=EmployeeRole.STAFF, classification=EmployeeClassification.FULL_TIME,
            experience=2, salary=Money(1000, Currency.USD)
        )

    def test_hire_employee(self, manager, employee):
        manager.hire(employee)
        assert manager.has_employee(employee)
        assert len(manager.employees) == 1

    def test_hire_duplicate_employee_raises_error(self, manager, employee):
        manager.hire(employee)
        with pytest.raises(EmployeeAlreadyHiredError):
            manager.hire(employee)

    def test_fire_employee(self, manager, employee):
        manager.hire(employee)
        manager.fire(employee)
        assert not manager.has_employee(employee)
        assert len(manager.employees) == 0

    def test_fire_unhired_employee_raises_error(self, manager, employee):
        with pytest.raises(EmployeeNotHiredError):
            manager.fire(employee)

    def test_calculate_payroll(self, manager):
        emp1 = Seller(
            name="A", surname="A", personal_id=1,
            role=EmployeeRole.STAFF, classification=EmployeeClassification.FULL_TIME,
            experience=1, salary=Money(1000, Currency.USD)
        )
        emp2 = Seller(
            name="B", surname="B", personal_id=2,
            role=EmployeeRole.STAFF, classification=EmployeeClassification.FULL_TIME,
            experience=1, salary=Money(2000, Currency.USD)
        )
        
        manager.hire(emp1)
        manager.hire(emp2)
        
        payroll = manager.calculate_payroll()
        assert payroll == Money(3000, Currency.USD)
