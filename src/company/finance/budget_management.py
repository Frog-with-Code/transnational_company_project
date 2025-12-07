from .budget import *
from .transaction import *
from dataclasses import replace
from ..common.exceptions import ForbiddenTransactionError


class BudgetManagementService:
    """
    Service layer responsible for orchestrating financial transactions between companies.

    This service handles currency conversion, transaction atomicity (rollback on failure),
    and maintains a historical record of all financial operations. It acts as the 
    central controller for money movement.

    Attributes:
        currency_service (CurrencyService): Service used for currency conversion rates.
        _transaction_history (list[Transaction]): Internal log of all processed transactions.
    """
    def __init__(self, currency_service: CurrencyService) -> None:
        """
        Initialize the budget manager.

        Args:
            currency_service (CurrencyService): The provider for currency exchange logic.
        """
        self.currency_service = currency_service
        self._transaction_history: list[Transaction] = []

    def transfer(
        self,
        source_money: Money,
        source_company: AbstractCompany,
        target_company: AbstractCompany,
        description: str = "",
    ) -> Transaction:
        """
        Execute a transfer of funds from one company to another.

        This method performs the following steps:
        1. Validates the source currency.
        2. Converts the amount to the target company's currency.
        3. Attempts to withdraw from the source and deposit to the target.
        4. Implements a rollback mechanism: if the deposit fails, the withdrawal is reversed.

        Args:
            source_money (Money): The amount and currency to take from the source.
            source_company (AbstractCompany): The entity sending the money.
            target_company (AbstractCompany): The entity receiving the money.
            description (str, optional): A note describing the transfer purpose.

        Returns:
            Transaction: A record of the operation containing status (COMPLETED/FAILED),
            timestamps, and converted amounts.
        """
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
                # Rollback withdrawal if deposit fails
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
        """
        Retrieve the history of all transactions.

        Returns:
            list[Transaction]: A shallow copy of the transaction list to prevent 
            external modification of the history.
        """
        return self._transaction_history[:]

    def deposit(
        self, source_money: Money, company: AbstractCompany, description: str = ""
    ) -> Transaction:
        """
        Inject funds into a company from an external source.

        Automatically converts the incoming money to the company's operating currency.

        Args:
            source_money (Money): The amount being deposited.
            company (AbstractCompany): The company receiving the funds.
            description (str, optional): Source or reason for the deposit.

        Returns:
            Transaction: The recorded deposit transaction.
        """
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
        """
        Reverse a specific past transfer transaction.

        Finds a transaction by ID and creates a new counter-transaction 
        sending money back from the original target to the original source.

        Args:
            transaction_id (UUID): The unique identifier of the transaction to refund.

        Raises:
            ForbiddenTransactionError: If the transaction is not of type TRANSFER.
            AttributeError: If the transaction_id is not found (implicit in implementation).
        """
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
