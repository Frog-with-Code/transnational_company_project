import pytest
from company.company_structure.companies import (
    HeadquarterCompany,
    SubsidiaryCompany,
    AssociatedCompany
)
from company.hr.employees import Seller
from company.hr.enums import EmployeeRole, EmployeeClassification
from company.finance.budget import Money, Currency
from company.common.exceptions import (
    CompanyAlreadyCooperatedError,
    CompanyNotCooperatedError,
    CompanyOwnershipStakeError
)

@pytest.fixture
def director():
    return Seller(
        name="Boss", surname="Big", personal_id=1,
        role=EmployeeRole.DIRECTOR, classification=EmployeeClassification.FULL_TIME,
        experience=10, salary=Money(5000, Currency.USD)
    )

@pytest.fixture
def hq(location, director):
    return HeadquarterCompany(
        name="Main Corp",
        location=location,
        director=director,
        starting_capital=Money(100000, Currency.USD)
    )

class TestAbstractCompany:
    def test_finance_operations(self, hq):
        assert hq.balance == Money(100000, Currency.USD)
        
        hq.deposit(Money(50000, Currency.USD))
        assert hq.balance == Money(150000, Currency.USD)
        
        hq.withdraw(Money(20000, Currency.USD))
        assert hq.balance == Money(130000, Currency.USD)

class TestSubsidiaryCompany:
    def test_creation_valid(self, hq, location, director):
        sub = SubsidiaryCompany(
            name="Sub Corp",
            location=location,
            director=director,
            starting_capital=Money(10000, Currency.USD),
            ownership_stake=51.0,
            parent_company=hq
        )
        assert sub.parent_company == hq
        assert sub.ownership_stake == 51.0

    def test_creation_invalid(self, hq, location, director):
        with pytest.raises(CompanyOwnershipStakeError):
            SubsidiaryCompany(
                name="Sub Corp",
                location=location,
                director=director,
                starting_capital=Money(10000, Currency.USD),
                ownership_stake=50.0,
                parent_company=hq
            )

class TestAssociatedCompany:
    def test_creation_valid(self, hq, location, director):
        assoc = AssociatedCompany(
            name="Assoc Corp",
            location=location,
            director=director,
            starting_capital=Money(10000, Currency.USD),
            ownership_stake=30.0,
            parent_company=hq
        )
        assert assoc.ownership_stake == 30.0

    def test_creation_invalid(self, hq, location, director):
        with pytest.raises(CompanyOwnershipStakeError):
            AssociatedCompany(
                name="Assoc Corp",
                location=location,
                director=director,
                ownership_stake=10.0,
                parent_company=hq
            )
        
        with pytest.raises(CompanyOwnershipStakeError):
            AssociatedCompany(
                name="Assoc Corp",
                location=location,
                director=director,
                ownership_stake=51.0,
                parent_company=hq
            )

class TestHeadquarterCompany:
    def test_manage_subsidiaries(self, hq, location, director):
        sub = SubsidiaryCompany(
            name="Sub 1", location=location, director=director,
            ownership_stake=60, parent_company=hq
        )
        
        hq.add_subsidiary(sub)
        subs, _ = hq.connected_companies
        assert sub in subs
        
        with pytest.raises(CompanyAlreadyCooperatedError):
            hq.add_subsidiary(sub)
            
        hq.remove_subsidiary(sub)
        subs, _ = hq.connected_companies
        assert sub not in subs
        
        with pytest.raises(CompanyNotCooperatedError):
            hq.remove_subsidiary(sub)

    def test_manage_associated(self, hq, location, director):
        assoc = AssociatedCompany(
            name="Assoc 1", location=location, director=director,
            ownership_stake=40, parent_company=hq
        )
        
        hq.add_associated_company(assoc)
        _, assocs = hq.connected_companies
        assert assoc in assocs
        
        with pytest.raises(CompanyAlreadyCooperatedError):
            hq.add_associated_company(assoc)
            
        hq.remove_associated_company(assoc)
        
        with pytest.raises(CompanyNotCooperatedError):
            hq.remove_associated_company(assoc)

    def test_consolidated_balance(self, hq, location, director):
        sub1 = SubsidiaryCompany(
            name="Sub 1", location=location, director=director,
            starting_capital=Money(10000, Currency.USD),
            ownership_stake=60, parent_company=hq
        )
        
        sub2 = SubsidiaryCompany(
            name="Sub 2", location=location, director=director,
            starting_capital=Money(10000, Currency.EUR),
            ownership_stake=60, parent_company=hq
        )
        
        hq.add_subsidiary(sub1)
        hq.add_subsidiary(sub2)
        
        balance_dict = hq.get_consolidated_balance()
        
        assert Currency.USD in balance_dict
        assert Currency.EUR in balance_dict
        assert balance_dict[Currency.USD].amount == 110000
        assert balance_dict[Currency.EUR].amount == 10000
