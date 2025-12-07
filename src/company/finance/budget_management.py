from .budget import *
from .transaction import *
from dataclasses import replace
from ..common.exceptions import ForbiddenTransactionError


class BudgetManagementService:
    def __init__(self, currency_service: CurrencyService) -> None:
        self.currency_service = currency_service
        self._transaction_history: list[Transaction] = []

    def transfer(
        self,
        source_money: Money,
        source_company: AbstractCompany,
        target_company: AbstractCompany,
        description: str = "",
    ) -> Transaction:

        source_money.validate_currency(source_company.balance)

        target_money = self.currency_service.convert(
            source_money, target_company.balance.currency
        )
        transaction = Transaction(
            source_company=source_company,
            target_company=target_company,
            source_money=source_money,
            target_money=target_money,
            description=description,
            transaction_type=TransactionType.TRANSFER,
        )

        try:
            source_company.withdraw(source_money)
            try:
                target_company.deposit(target_money)
            except Exception as deposit_error:
                source_company.deposit(source_money)
                raise deposit_error

            status = TransactionStatus.COMPLETED
        except ForbiddenTransactionError as e:
            status = TransactionStatus.FAILED
            print(f"Transaction failed with error {e}")

        transaction = replace(transaction, status=status)
        self._transaction_history.append(transaction)
        return transaction

    @property
    def transaction_history(self) -> list[Transaction]:
        return self._transaction_history[:]

    def deposit(
        self, source_money: Money, company: AbstractCompany, description: str = ""
    ) -> Transaction:
        target_money = self.currency_service.convert(
            source_money, company.balance.currency
        )
        company.deposit(target_money)
        transaction = Transaction(
            target_company=company,
            source_money=source_money,
            target_money=target_money,
            description=description,
            transaction_type=TransactionType.DEPOSIT,
        )
        self._transaction_history.append(transaction)
        return transaction

    def refund(self, transaction_id: UUID):
        transaction = next(
            (
                tr
                for tr in reversed(self._transaction_history)
                if tr.transaction_id == transaction_id
            ),
            None,
        )

        if transaction.transaction_type != TransactionType.TRANSFER:
            raise ForbiddenTransactionError("Can only refund transfers")

        self.transfer(
            source_money=transaction.target_money,
            source_company=transaction.target_company,
            target_company=transaction.source_company,
            description=f"Refund for {transaction_id}",
        )
