import pytest

from company.finance.transaction import Transaction, TransactionType, TransactionStatus
from company.finance.budget import Money, Currency
from company.common.exceptions import ForbiddenTransactionError

class TestTransaction:
    @pytest.fixture
    def mock_company(self, mocker):
        return mocker.Mock()

    def test_create_transfer_success(self, mock_company):
        t = Transaction(
            transaction_type=TransactionType.TRANSFER,
            source_money=Money(100, Currency.USD),
            target_money=Money(100, Currency.USD),
            source_company=mock_company,
            target_company=mock_company,
            description="Test transfer"
        )
        assert t.status == TransactionStatus.PENDING
        assert t.transaction_id is not None

    def test_create_transfer_missing_parties(self, mock_company):
        with pytest.raises(ForbiddenTransactionError):
            Transaction(
                transaction_type=TransactionType.TRANSFER,
                source_money=Money(100, Currency.USD),
                target_money=Money(100, Currency.USD),
                source_company=mock_company,
                target_company=None
            )

    def test_create_deposit_success(self, mock_company):
        t = Transaction(
            transaction_type=TransactionType.DEPOSIT,
            source_money=Money(100, Currency.USD),
            target_money=Money(100, Currency.USD),
            source_company=None,
            target_company=mock_company
        )
        assert t.transaction_type == TransactionType.DEPOSIT

    def test_create_deposit_invalid(self, mock_company):
        with pytest.raises(ForbiddenTransactionError):
            Transaction(
                transaction_type=TransactionType.DEPOSIT,
                source_money=Money(100, Currency.USD),
                target_money=Money(100, Currency.USD),
                source_company=mock_company,
                target_company=mock_company
            )
