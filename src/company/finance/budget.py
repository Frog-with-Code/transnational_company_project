from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from ..common.exceptions import DifferentCurrenciesError
from datetime import datetime, replace
from enum import Enum

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    BYN = "BYN"

@dataclass(frozen=True)
class Money:
    amount: Decimal = 0
    currency: Currency = Currency("USD")

    def validate_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise DifferentCurrenciesError(
                f"This operation with different currencies ({self.currency} and {other.currency}) is impossible!"
            )

    def __eq__(self, other: Money) -> bool:
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other: Money) -> bool:
        self.validate_currency(other)
        return self.amount < other.amount

    def __le__(self, other: Money) -> bool:
        self.validate_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: Money) -> bool:
        self.validate_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: Money) -> bool:
        self.validate_currency(other)
        return self.amount >= other.amount

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"


class Budget:
    def __init__(self, balance: Money = Money(0, Currency.USD)) -> None:
        self._balance = balance

    @property
    def currency(self) -> Currency:
        return self._balance.currency

    @property
    def balance(self) -> Money:
        return self._balance

    def _can_withdraw(self, money: Money) -> bool:
        return self._balance.amount >= money.amount

    def withdraw(self, money: Money) -> None:
        self.currency.validate_currency(money)
        if self._can_withdraw(money):
            self._balance = replace(
                self._balance, amount=self._balance.amount - money.amount
            )

    def deposit(self, money: Money) -> None:
        self.currency.validate_currency(money)
        self._balance = replace(
            self._balance, amount=self._balance.amount + money.amount
        )


class CurrencyService:
    def __init__(self, rates: dict[Currency, Decimal]) -> None:
        self._rates = rates
        self._creation_date = datetime.now()

    def convert(self, money: Money, target_currency: Currency) -> Money:
        if money.currency == target_currency:
            return money

        to_usd = money.amount * self._rates[money.currency]
        return Money(to_usd / self._rates[target_currency], target_currency)
    
    @property
    def rates(self) -> dict[Currency, Decimal]:
        return self._rates.copy()
