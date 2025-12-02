from __future__ import annotations
from abc import ABC
from hr import AbstractEmployee
from ..hr.employee_manager import EmployeeManagerMixin
from ..finance.budget import Budget, Money, Currency
from ..common.exceptions import (
    CompanyAlreadyCooperatedError,
    CompanyNotCooperatedError,
    CompanyOwnershipStakeError
)
from ..common.location import Location


class AbstractCompany(ABC, EmployeeManagerMixin):
    def __init__(
        self,
        *,
        name: str,
        location: Location,
        director: AbstractEmployee,
        starting_capital: Money = None,
    ) -> None:
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
        return self._budget.balance

    def withdraw(self, money: Money) -> None:
        self._budget.withdraw(money)
        print(f"[{self.name}] Withdrawn: {money}")

    def deposit(self, money: Money) -> None:
        self._budget.deposit(money)
        print(f"[{self.name}] Deposited: {money}")

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AbstractCompany):
            return NotImplemented
        return self.name == other.name and self.location == other.location


class HeadquarterCompany(AbstractCompany):
    def __init__(
        self,
        *,
        name: str,
        location: Location,
        director: AbstractEmployee,
        starting_capital: Money = None,
    ) -> None:
        super().__init__(
            name=name, location=location, director=director, starting_capital=starting_capital
        )
        self._subsidiaries: set[SubsidiaryCompany] = set()
        self._associated_companies: set[AssociatedCompany] = set()

    def add_subsidiary(self, company: SubsidiaryCompany) -> None:
        if company in self._subsidiaries:
            raise CompanyAlreadyCooperatedError(
                f"{company.name} is already a subsidiary"
            )
        self._subsidiaries.add(company)
        print(f"Subsidiary added: {company.name}")

    def add_associated_company(self, company: AssociatedCompany) -> None:
        if company in self._associated_companies:
            raise CompanyAlreadyCooperatedError(f"{company.name} is already associated")
        self._associated_companies.add(company)
        print(f"Associated company added: {company.name}")

    def remove_subsidiary(self, company: SubsidiaryCompany) -> None:
        if company not in self._subsidiaries:
            raise CompanyNotCooperatedError(f"{company.name} is not a subsidiary yet")
        self._subsidiaries.remove(company)
        print(f"Subsidiary removed: {company.name}")

    def remove_associated_company(self, company: AssociatedCompany) -> None:
        if company not in self._associated_companies:
            raise CompanyNotCooperatedError(f"{company.name} is not associated yet")
        self._associated_companies.remove(company)
        print(f"Associated company removed: {company.name}")

    def get_consolidated_balance(self) -> Money:
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
        return (
            self._subsidiaries.copy(),
            self._associated_companies.copy(),
        )


class SubsidiaryCompany(AbstractCompany):
    def __init__(
        self, *, ownership_stake: float, parent_company: HeadquarterCompany, **kwargs
    ) -> None:
        super().__init__(**kwargs)

        if ownership_stake <= 50:
            raise CompanyOwnershipStakeError("Subsidiary must be >50% owned by parent.")

        self.ownership_stake = ownership_stake
        self._parent_company = parent_company

    @property
    def parent_company(self) -> HeadquarterCompany:
        return self._parent_company

    def is_fully_owned(self) -> bool:
        return self.ownership_stake >= 99.9

    def __str__(self) -> str:
        return (
            f"Subsidiary: {self.name} "
            f"({self.ownership_stake}% owned by {self.parent_company.name})"
        )


class AssociatedCompany(AbstractCompany):
    def __init__(
        self,
        *,
        name: str,
        location: Location,
        director: AbstractEmployee,
        ownership_stake: float,
        parent_company: HeadquarterCompany,
        starting_capital: Money = None,
    ) -> None:
        super().__init__(
            name=name, location=location, director=director, starting_capital=starting_capital
        )

        if not (20 <= ownership_stake <= 50):
            raise CompanyOwnershipStakeError(
                "Associated company stake must be between 20% and 50%."
            )

        self.ownership_stake = ownership_stake
        self._parent_company = parent_company

    @property
    def parent_company(self) -> HeadquarterCompany:
        return self._parent_company

    def __str__(self) -> str:
        return (
            f"Associated company: {self.name} "
            f"({self.ownership_stake}% owned by {self.parent_company.name})"
        )
