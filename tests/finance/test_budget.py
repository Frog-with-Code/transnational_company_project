import pytest
from decimal import Decimal

from company.finance.budget import Money, Budget, Currency, CurrencyService
from company.common.exceptions import DifferentCurrenciesError, InsufficientBudgetError


class TestMoney:
    def test_create_money(self):
        m = Money(100, Currency.USD)
        assert m.amount == 100
        assert m.currency == Currency.USD

    def test_create_money_negative(self):
        with pytest.raises(ValueError):
            Money(-10, Currency.USD)

    def test_money_equality(self):
        assert Money(100, Currency.USD) == Money(100, Currency.USD)
        assert Money(100, Currency.USD) != Money(200, Currency.USD)
        assert Money(100, Currency.USD) != Money(100, Currency.EUR)

    def test_money_comparison(self):
        m1 = Money(50, Currency.USD)
        m2 = Money(100, Currency.USD)

        assert m1 < m2
        assert m2 > m1
        assert m1 <= m2
        assert m1 <= Money(50, Currency.USD)

    def test_money_comparison_different_currencies(self):
        m1 = Money(50, Currency.USD)
        m2 = Money(100, Currency.EUR)

        with pytest.raises(DifferentCurrenciesError):
            m1 < m2

    def test_money_arithmetic(self):
        m1 = Money(100, Currency.USD)
        m2 = Money(50, Currency.USD)

        assert m1 + m2 == Money(150, Currency.USD)
        assert m1 - m2 == Money(50, Currency.USD)
        assert m1 * 2 == Money(200, Currency.USD)
        assert m1 * 0.5 == Money(50, Currency.USD)

    def test_money_arithmetic_different_currencies(self):
        m1 = Money(100, Currency.USD)
        m2 = Money(50, Currency.EUR)

        with pytest.raises(DifferentCurrenciesError):
            m1 + m2


class TestBudget:
    @pytest.fixture
    def budget(self):
        return Budget(Money(1000, Currency.USD))

    def test_initial_balance(self, budget):
        assert budget.balance == Money(1000, Currency.USD)
        assert budget.currency == Currency.USD

    def test_deposit(self, budget):
        budget.deposit(Money(500, Currency.USD))
        assert budget.balance == Money(1500, Currency.USD)

    def test_withdraw_success(self, budget):
        budget.withdraw(Money(500, Currency.USD))
        assert budget.balance == Money(500, Currency.USD)

    def test_withdraw_insufficient(self, budget):
        with pytest.raises(InsufficientBudgetError):
            budget.withdraw(Money(1500, Currency.USD))

    def test_withdraw_wrong_currency(self, budget):
        with pytest.raises(DifferentCurrenciesError):
            budget.withdraw(Money(100, Currency.EUR))


class TestCurrencyService:
    @pytest.fixture
    def service(self):
        rates = {
            Currency.USD: Decimal("1.0"),
            Currency.EUR: Decimal("1.1"),
            Currency.BYN: Decimal("0.3"),
        }
        return CurrencyService(rates)

    def test_convert_same_currency(self, service):
        m = Money(100, Currency.USD)
        converted = service.convert(m, Currency.USD)
        assert converted == m

    def test_convert_eur_to_usd(self, service):
        m = Money(100, Currency.EUR)
        converted = service.convert(m, Currency.USD)
        assert converted.currency == Currency.USD
        assert converted.amount == Decimal("110.0")

    def test_convert_usd_to_byn(self, service):
        m = Money(30, Currency.USD)
        converted = service.convert(m, Currency.BYN)
        assert converted.currency == Currency.BYN
        assert converted.amount, Decimal("100.0")
