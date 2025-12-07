from __future__ import annotations
from abc import ABC

from ..hr.employees import AbstractEmployee
from ..hr.employee_manager import EmployeeManagerMixin
from ..finance.budget import Budget, Money, Currency
from ..common.exceptions import (
    CompanyAlreadyCooperatedError,
    CompanyNotCooperatedError,
    CompanyOwnershipStakeError,
)
from ..common.location import Location


class AbstractCompany(ABC, EmployeeManagerMixin):
    """
    Abstract base class representing a corporate entity.

    Combines financial management (via internal Budget) and human resources 
    management (via EmployeeManagerMixin). It defines the fundamental identity 
    of a company through its name and location.

    Attributes:
        name (str): The legal name of the company.
        location (Location): The physical or legal address of the company.
        director (AbstractEmployee): The person currently leading the company.
    """
    def __init__(
        self,
        *,
        name: str,
        location: Location,
        director: AbstractEmployee,
        starting_capital: Money = None,
    ) -> None:
        """
        Initialize the company with capital and leadership.

        Args:
            name (str): Company name.
            location (Location): Company location.
            director (AbstractEmployee): The director/CEO.
            starting_capital (Money, optional): Initial financial assets. 
                Defaults to 0 USD if None.
        """
        super().__init__()

        if starting_capital is None:
            starting_capital = Money(0, Currency.USD)

        self._budget = Budget(starting_capital)
        self.name = name
        self.location = location
        self.director = director

        self._employees: set[AbstractEmployee] = set()

    @property
    def balance(self) -> Money:
        """
        Get the current financial balance of the company.

        Returns:
            Money: The current amount in the budget.
        """
        return self._budget.balance

    def withdraw(self, money: Money) -> None:
        """
        Remove funds from the company budget.

        Args:
            money (Money): The amount to withdraw.

        Raises:
            ValueError: If funds are insufficient (handled by Budget).
        """
        self._budget.withdraw(money)
        print(f"[{self.name}] Withdrawn: {money}")

    def deposit(self, money: Money) -> None:
        """
        Add funds to the company budget.

        Args:
            money (Money): The amount to deposit.
        """
        self._budget.deposit(money)
        print(f"[{self.name}] Deposited: {money}")

    def __hash__(self) -> int:
        """Return hash based on the company name."""
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        """
        Check equality based on name and location.

        Args:
            other (object): Object to compare.

        Returns:
            bool: True if name and location match, False otherwise.
        """
        if not isinstance(other, AbstractCompany):
            return NotImplemented
        return self.name == other.name and self.location == other.location


class HeadquarterCompany(AbstractCompany):
    """
    Represents the main holding or parent company.

    A HeadquarterCompany can own subsidiaries and have associated companies.
    It provides functionality to consolidate financial reports from its network.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._subsidiaries: set[SubsidiaryCompany] = set()
        self._associated_companies: set[AssociatedCompany] = set()

    def add_subsidiary(self, company: SubsidiaryCompany) -> None:
        """
        Register a new subsidiary under this headquarters.

        Args:
            company (SubsidiaryCompany): The company to acquire.

        Raises:
            CompanyAlreadyCooperatedError: If the company is already registered.
        """
        if company in self._subsidiaries:
            raise CompanyAlreadyCooperatedError(
                f"{company.name} is already a subsidiary"
            )
        self._subsidiaries.add(company)
        print(f"Subsidiary added: {company.name}")

    def add_associated_company(self, company: AssociatedCompany) -> None:
        """
        Register a new associated company.

        Args:
            company (AssociatedCompany): The company to associate.

        Raises:
            CompanyAlreadyCooperatedError: If the company is already associated.
        """
        if company in self._associated_companies:
            raise CompanyAlreadyCooperatedError(f"{company.name} is already associated")
        self._associated_companies.add(company)
        print(f"Associated company added: {company.name}")

    def remove_subsidiary(self, company: SubsidiaryCompany) -> None:
        """
        Remove a subsidiary from the network.

        Args:
            company (SubsidiaryCompany): The company to remove.

        Raises:
            CompanyNotCooperatedError: If the company is not currently a subsidiary.
        """
        if company not in self._subsidiaries:
            raise CompanyNotCooperatedError(f"{company.name} is not a subsidiary yet")
        self._subsidiaries.remove(company)
        print(f"Subsidiary removed: {company.name}")

    def remove_associated_company(self, company: AssociatedCompany) -> None:
        """
        Remove an associated company from the network.

        Args:
            company (AssociatedCompany): The company to remove.

        Raises:
            CompanyNotCooperatedError: If the company is not currently associated.
        """
        if company not in self._associated_companies:
            raise CompanyNotCooperatedError(f"{company.name} is not associated yet")
        self._associated_companies.remove(company)
        print(f"Associated company removed: {company.name}")

    def get_consolidated_balance(self) -> Money:
        """
        Calculate the total balance of the HQ and all its subsidiaries.

        Aggregates funds by currency.

        Returns:
            dict[Currency, Money]: A dictionary where keys are currencies and 
            values are the total Money objects for that currency.
        """
        total_amount = {}
        total_amount[self.balance.currency] = self.balance

        for sub in self._subsidiaries:
            sub_balance = sub.balance
            if sub_balance.currency in total_amount:
                total_amount[sub_balance.currency] += sub_balance
            else:
                total_amount[sub_balance.currency] = sub_balance

        return total_amount

    @property
    def connected_companies(
        self,
    ) -> tuple[set[SubsidiaryCompany], set[AssociatedCompany]]:
        """
        Get all linked entities.

        Returns:
            tuple[set[SubsidiaryCompany], set[AssociatedCompany]]: 
            Copies of the sets containing subsidiaries and associated companies.
        """
        return (
            self._subsidiaries.copy(),
            self._associated_companies.copy(),
        )


class SubsidiaryCompany(AbstractCompany):
    """
    Represents a company that is controlled by a parent company.

    A subsidiary must be more than 50% owned by the parent company.

    Attributes:
        ownership_stake (float): The percentage of ownership held by the parent.
    """
    def __init__(
        self, *, ownership_stake: float, parent_company: HeadquarterCompany, **kwargs
    ) -> None:
        """
        Initialize the subsidiary.

        Args:
            ownership_stake (float): Percentage of ownership (must be > 50).
            parent_company (HeadquarterCompany): The controlling entity.
            **kwargs: Arguments passed to AbstractCompany.

        Raises:
            CompanyOwnershipStakeError: If ownership_stake is <= 50.
        """
        super().__init__(**kwargs)

        if ownership_stake <= 50:
            raise CompanyOwnershipStakeError("Subsidiary must be >50% owned by parent.")

        self.ownership_stake = ownership_stake
        self._parent_company = parent_company

    @property
    def parent_company(self) -> HeadquarterCompany:
        """Get the controlling parent company."""
        return self._parent_company

    def is_fully_owned(self) -> bool:
        """
        Check if the subsidiary is a wholly owned subsidiary.

        Returns:
            bool: True if ownership stake is >= 99.9%.
        """
        return self.ownership_stake >= 99.9

    def __str__(self) -> str:
        return (
            f"Subsidiary: {self.name} "
            f"({self.ownership_stake}% owned by {self.parent_company.name})"
        )


class AssociatedCompany(AbstractCompany):
    """
    Represents a company where the parent has significant influence but not control.

    An associated company must be between 20% and 50% owned by the parent company.

    Attributes:
        ownership_stake (float): The percentage of ownership held by the parent.
    """
    def __init__(
        self, *, ownership_stake: float, parent_company: HeadquarterCompany, **kwargs
    ) -> None:
        """
        Initialize the associated company.

        Args:
            ownership_stake (float): Percentage of ownership (20 <= stake <= 50).
            parent_company (HeadquarterCompany): The investing entity.
            **kwargs: Arguments passed to AbstractCompany.

        Raises:
            CompanyOwnershipStakeError: If ownership_stake is not between 20 and 50.
        """
        super().__init__(**kwargs)

        if not (20 <= ownership_stake <= 50):
            raise CompanyOwnershipStakeError(
                "Associated company stake must be between 20% and 50%."
            )

        self.ownership_stake = ownership_stake
        self._parent_company = parent_company

    @property
    def parent_company(self) -> HeadquarterCompany:
        """Get the investing parent company."""
        return self._parent_company

    def __str__(self) -> str:
        return (
            f"Associated company: {self.name} "
            f"({self.ownership_stake}% owned by {self.parent_company.name})"
        )
