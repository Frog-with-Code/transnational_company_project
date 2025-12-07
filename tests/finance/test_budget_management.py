import pytest
from decimal import Decimal

from company.finance.budget_management import BudgetManagementService
from company.finance.budget import Money, Currency, CurrencyService, Budget
from company.finance.transaction import TransactionType, TransactionStatus
from company.common.exceptions import InsufficientBudgetError, ForbiddenTransactionError


class FakeCompany:
    def __init__(self, currency=Currency.USD, amount=1000):
        self.budget = Budget(Money(amount, currency))

    def withdraw(self, money):
        self.budget.withdraw(money)

    def deposit(self, money):
        self.budget.deposit(money)

    @property
    def balance(self) -> Money:
        return self.budget.balance


class TestBudgetManagementService:
    @pytest.fixture
    def currency_service(self):
        rates = {
            Currency.USD: Decimal("1.0"),
            Currency.EUR: Decimal("1.1"),
        }
        return CurrencyService(rates)

    @pytest.fixture
    def service(self, currency_service):
        return BudgetManagementService(currency_service)

    @pytest.fixture
    def company_a(self):
        return FakeCompany(Currency.USD, 1000)

    @pytest.fixture
    def company_b(self):
        return FakeCompany(Currency.USD, 500)

    def test_transfer_success(self, service, company_a, company_b):
        amount = Money(200, Currency.USD)

        transaction = service.transfer(
            source_money=amount,
            source_company=company_a,
            target_company=company_b,
            description="Payment",
        )

        assert transaction.status == TransactionStatus.COMPLETED
        assert company_a.balance.amount == 800
        assert company_b.balance.amount == 700
        assert len(service.transaction_history) == 1

    def test_transfer_with_conversion(self, service):
        company_usd = FakeCompany(Currency.USD, 1000)
        company_eur = FakeCompany(Currency.EUR, 0)

        amount_usd = Money(110, Currency.USD)

        transaction = service.transfer(
            source_money=amount_usd,
            source_company=company_usd,
            target_company=company_eur,
        )

        assert transaction.status == TransactionStatus.COMPLETED
        assert company_usd.balance.amount == 890

    def test_transfer_insufficient_funds(self, service, company_a, company_b):
        amount = Money(2000, Currency.USD)

        with pytest.raises(InsufficientBudgetError):
            service.transfer(amount, company_a, company_b)

        assert company_a.balance.amount == 1000
        assert company_b.balance.amount == 500
        assert len(service.transaction_history) == 0

    def test_transfer_rollback_on_deposit_fail(self, service, company_a, mocker):
        amount = Money(100, Currency.USD)

        bad_company = mocker.Mock(spec=FakeCompany)
        bad_company.balance = Budget(Money(0, Currency.USD))
        bad_company.deposit.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            service.transfer(amount, company_a, bad_company)

        assert company_a.balance.amount == 1000

    def test_deposit(self, service, company_a):
        amount = Money(500, Currency.USD)
        transaction = service.deposit(amount, company_a, "Investments")

        assert transaction.transaction_type == TransactionType.DEPOSIT
        assert company_a.balance.amount == 1500
        assert len(service.transaction_history) == 1

    def test_refund_success(self, service, company_a, company_b):
        t_original = service.transfer(Money(100, Currency.USD), company_a, company_b)

        service.refund(t_original.transaction_id)

        assert len(service.transaction_history) == 2
        refund_transaction = service.transaction_history[-1]

        assert refund_transaction.transaction_type == TransactionType.TRANSFER
        assert "Refund for" in refund_transaction.description

        assert company_a.balance.amount == 1000
        assert company_b.balance.amount == 500

    def test_refund_fail_not_transfer(self, service, company_a):
        t_deposit = service.deposit(Money(100, Currency.USD), company_a)

        with pytest.raises(ForbiddenTransactionError):
            service.refund(t_deposit.transaction_id)
