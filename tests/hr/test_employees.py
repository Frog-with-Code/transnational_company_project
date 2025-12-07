import pytest
from datetime import date, timedelta

from company.hr.employees import ITSpecialist, Driver, Accountant, Cleaner
from company.hr.enums import *
from company.finance.budget import Money, Currency
from company.common.exceptions import EmployeePossibilityError


@pytest.fixture
def base_salary():
    return Money(1500, Currency.USD)


class TestFieldEmployee:
    @pytest.fixture
    def field_employee(self):
        return Driver(
            name="Bob",
            surname="Marley",
            personal_id=2,
            role=EmployeeRole.STAFF,
            classification=EmployeeClassification.FULL_TIME,
            experience=10,
            salary=base_salary,
            license_category="C",
            license_expire_date=date.today() + timedelta(days=365),
            workwear=[],
            medical_check_date=date(2022, 1, 2),
        )

    def test_can_work_remotely(self, field_employee):
        assert field_employee.can_work_remotely() is False

    def test_is_medically_fit(self, field_employee):
        field_employee.medical_check_date = date.today()
        assert field_employee.is_medically_fit() is True
        
        field_employee.medical_check_date = date.today() - timedelta(days=365)
        assert field_employee.is_medically_fit() is True

    def test_is_medically_fit_expired(self, field_employee):
        field_employee.medical_check_date = date.today() - timedelta(days=366)
        assert field_employee.is_medically_fit() is False


class TestITSpecialist:
    @pytest.fixture
    def it_specialist(self, base_salary):
        return ITSpecialist(
            name="Alice",
            surname="Smith",
            personal_id=1,
            role=EmployeeRole.STAFF,
            classification=EmployeeClassification.FULL_TIME,
            experience=3,
            salary=base_salary,
            specialization=ITSpecialization.BACKEND,
            programming_langs=["Python"],
            qualification_level=ITQualificationLevel.MIDDLE,
        )

    def test_project_management(self, it_specialist):
        assert it_specialist.get_active_projects_amount() == 0

        it_specialist.assign_project("Project Alpha")
        assert it_specialist.get_active_projects_amount() == 1
        assert "Project Alpha" in it_specialist.active_projects

        it_specialist.complete_project("Project Alpha")
        assert it_specialist.get_active_projects_amount() == 0

    def test_remote_work_capability(self, it_specialist):
        assert it_specialist.can_work_remotely() is True


class TestDriver:
    @pytest.fixture
    def driver(self, base_salary):
        return Driver(
            name="Bob",
            surname="Marley",
            personal_id=2,
            role=EmployeeRole.STAFF,
            classification=EmployeeClassification.FULL_TIME,
            experience=10,
            salary=base_salary,
            license_category="C",
            license_expire_date=date.today() + timedelta(days=365),
            workwear=[],
            medical_check_date=date(2022, 1, 2),
        )

    def test_license_validity(self, driver):
        assert driver.is_valid_license() is True

        driver.license_expire_date = date.today() - timedelta(days=1)
        assert driver.is_valid_license() is False

    def test_route_management(self, driver):
        driver.assign_route("Route 66")
        assert "Route 66" in driver.routes

        driver.unassign_route("Route 66")
        assert "Route 66" not in driver.routes

        driver.assign_route(["Route 1", "Route 2"])
        assert {"Route 1", "Route 2"}.issubset(driver.routes)


class TestAccountant:
    @pytest.fixture
    def accountant(self, base_salary):
        return Accountant(
            name="Charlie",
            surname="Chaplin",
            personal_id=3,
            role=EmployeeRole.STAFF,
            classification=EmployeeClassification.FULL_TIME,
            experience=5,
            salary=base_salary,
            erp_systems=["SAP"],
            certifications=[FinancialQualification.ACCA],
        )

    def test_audit_permission_success(self, accountant):
        assert accountant.can_handle_audit() is True

    def test_audit_permission_fail(self, accountant):
        accountant.certifications = []
        assert accountant.can_handle_audit() is False

        with pytest.raises(EmployeePossibilityError):
            accountant.start_audit()
            
    def test_end_audit_success(self, accountant):
        accountant.audit_status = "in_progress" 
        
        accountant.end_audit()
        
        assert accountant.audit_status == "none"

    def test_end_audit_no_active_audit(self, accountant):
        accountant.audit_status = "none"
        
        accountant.end_audit()
    
        assert accountant.audit_status == "none"


class TestCleaner:
    @pytest.fixture
    def cleaner(self, base_salary):
        return Cleaner(
            name="Dora",
            surname="Explorer",
            personal_id=4,
            role=EmployeeRole.STAFF,
            classification=EmployeeClassification.FULL_TIME,
            experience=1,
            salary=base_salary,
            skills=["Mopping"],
            hazardous_waste_trained=False,
            workwear=["boots", "gloves"],
            medical_check_date=date(2022, 1, 2),
        )

    def test_equipment_handling(self, cleaner):
        assert not cleaner.has_equipment()

        cleaner.give_equipment("Broom")
        assert cleaner.has_equipment()
        assert "Broom" in cleaner.equipment

        cleaner.take_equipment("Broom")
        assert not cleaner.has_equipment()
