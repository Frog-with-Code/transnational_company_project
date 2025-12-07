import pytest
from datetime import date
from decimal import Decimal

from company.hr.employee_factory import EmployeeFactory
from company.hr.employees import *
from company.hr.enums import *
from company.finance.budget import Money, Currency

class TestEmployeeFactory:
    @pytest.fixture
    def factory(self):
        return EmployeeFactory()

    @pytest.fixture
    def base_params(self):
        return {
            "name": "John",
            "surname": "Doe",
            "role": EmployeeRole.STAFF,
            "classification": EmployeeClassification.FULL_TIME,
            "experience": 5,
            "salary": Money(Decimal(2000), Currency.USD)
        }

    def test_create_it_specialist(self, factory, base_params):
        params = {
            **base_params,
            "profession": "it_specialist",
            "specialization": ITSpecialization.BACKEND,
            "programming_langs": ["Python", "SQL"],
            "qualification_level": ITQualificationLevel.SENIOR
        }
        
        employee = factory.create_by_params(**params)
        
        assert isinstance(employee, ITSpecialist)
        assert employee.name == "John"
        assert employee.profession == "it_specialist"
        assert employee.specialization == ITSpecialization.BACKEND
        assert "Python" in employee.programming_langs

    def test_create_driver(self, factory, base_params):
        params = {
            **base_params,
            "profession": "driver",
            "license_category": "B",
            "license_expire_date": date(2030, 1, 1),
            "workwear": ["boots"],
            "medical_check_date": date(2022, 1, 12)
        }
        
        employee = factory.create_by_params(**params)
        
        assert isinstance(employee, Driver)
        assert employee.name == "John"
        assert employee.profession == "driver"
        assert employee.license_category == "B"
        assert employee.license_expire_date == date(2030, 1, 1)

    def test_create_accountant_strings_enum(self, factory, base_params):
        params = {
            **base_params,
            "profession": "accountant",
            "erp_systems": ["1C", "SAP"],
            "certifications": ["ACCA", "CFA"]
        }
        
        employee = factory.create_by_params(**params)
        
        assert isinstance(employee, Accountant)
        assert employee.name == "John"
        assert employee.profession == "accountant"
        assert FinancialQualification.ACCA in employee.certifications
        assert FinancialQualification.CFA in employee.certifications

    def test_create_cleaner(self, factory, base_params):
        params = {
            **base_params,
            "profession": "cleaner",
            "skills": ["Dry cleaning"],
            "hazardous_waste_trained": True,
            "workwear": ["boots", "gloves", "overall"],
            "medical_check_date": date(2022, 1, 12)
        }
        
        employee = factory.create_by_params(**params)
        
        assert isinstance(employee, Cleaner)
        assert employee.name == "John"
        assert employee.profession == "cleaner"
        assert employee.hazardous_waste_trained is True
        
    def test_create_seller(self, factory, base_params):
        params = {
            **base_params,
            "profession": "seller"
        }
        
        employee = factory.create_by_params(**params)
        
        assert isinstance(employee, Seller)
        assert employee.name == "John"
        assert employee.profession == "seller"   
        
    def test_create_hr_specialist(self, factory, base_params):
        params = {
            **base_params,
            "profession": "hr_specialist"
        }
        
        employee = factory.create_by_params(**params)
        
        assert isinstance(employee, HRSpecialist)
        assert employee.name == "John"
        assert employee.profession == "hr_specialist"
        
    def test_validation_error_missing_fields(self, factory, base_params):
        params = {
            **base_params,
            "profession": "it_specialist",
        }
        
        with pytest.raises(ValueError):
            factory.create_by_params(**params)

    def test_validation_error_invalid_type(self, factory, base_params):
        params = {
            **base_params,
            "profession": "driver",
            "license_category": "B",
            "license_expire_date": "not-a-date"
        }
        
        with pytest.raises(ValueError):
            factory.create_by_params(**params)

    def test_auto_increment_id(self, factory, base_params):
        params = {
            **base_params,"profession": "seller"}
        
        emp1 = factory.create_by_params(**params)
        emp2 = factory.create_by_params(**params)
        
        assert emp1.personal_id != emp2.personal_id
        assert emp2.personal_id == emp1.personal_id + 1
