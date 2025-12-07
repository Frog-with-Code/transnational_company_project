from __future__ import annotations
from dataclasses import dataclass, replace
from decimal import Decimal, ROUND_HALF_UP
from ..common.exceptions import DifferentCurrenciesError, InsufficientBudgetError
from datetime import datetime
from enum import Enum
from ..common.validation import validate_non_negative


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

    def __add__(self, other: Money) -> Money:
        self.validate_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        self.validate_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: int | float | Decimal) -> Money:
        validate_non_negative(factor)
        return Money(self.amount * factor, self.currency)

    def __truediv__(self, factor: int | float | Decimal) -> Money:
        validate_non_negative(factor)
        raw_amount = self.amount / factor
        return Money(
            raw_amount.quantize(Decimal("0.00001"), rounding=ROUND_HALF_UP),
            self.currency,
        )

    def __post_init__(self) -> None:
        validate_non_negative(self.amount)


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
        self._balance.validate_currency(money)
        if not self._can_withdraw(money):
            raise InsufficientBudgetError(
                "There is not enough money in the budget for withdraw"
            )

        self._balance = self.balance - money

    def deposit(self, money: Money) -> None:
        self._balance.validate_currency(money)
        self._balance = self.balance + money


class CurrencyService:
    def __init__(self, rates: dict[Currency, Decimal]) -> None:
        self._rates = rates
        self._creation_date = datetime.now()

    def convert(self, money: Money, target_currency: Currency) -> Money:
        if money.currency == target_currency:
            return money

        conversion_factor = self._rates[money.currency] / self._rates[target_currency]

        return replace(
            money, amount=money.amount * conversion_factor, currency=target_currency
        )

    @property
    def rates(self) -> dict[Currency, Decimal]:
        return self._rates.copy()
