from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from .budget import Money
from ..company_structure.companies import AbstractCompany
from ..common.exceptions import ForbiddenTransactionError


class TransactionType(Enum):
    """
    Categorization of financial operations.

    Values:
        TRANSFER: Movement of funds from one internal entity to another.
        REFUND: Reversal of a previous transaction.
        DEPOSIT: Injection of funds from an external source into an entity.
    """
    TRANSFER = "Transfer"
    REFUND = "Refund"
    DEPOSIT = "Deposit"
    

class TransactionStatus(Enum):
    """
    The current state of a transaction in its lifecycle.

    Values:
        COMPLETED: The transaction finished successfully.
        FAILED: The transaction encountered an error and was rolled back.
        PENDING: The transaction is currently being processed or created.
    """
    COMPLETED = "Completed"
    FAILED = "Failed"
    PENDING = "Pending"


@dataclass(frozen=True)
class Transaction:
    """
    Immutable record of a financial operation.

    Stores all relevant details about a movement of money, including the source,
    destination, amounts involved (in both source and target currencies), and metadata.
    Validates logical consistency of fields based on the transaction type upon initialization.

    Attributes:
        transaction_type (TransactionType): The category of the operation.
        source_money (Money): The amount sent/withdrawn (in source currency).
        target_money (Money): The amount received/deposited (in target currency).
        source_company (Optional[AbstractCompany]): The entity sending funds (required for TRANSFER).
        target_company (Optional[AbstractCompany]): The entity receiving funds (required for TRANSFER/DEPOSIT).
        description (str): Human-readable note or reference.
        transaction_id (UUID): Unique identifier for the transaction (auto-generated).
        status (TransactionStatus): Result of the operation. Defaults to PENDING.
        time (datetime): Timestamp of creation (auto-generated).
    """
    transaction_type: TransactionType
    source_money: Money
    target_money: Money
    source_company: Optional[AbstractCompany] = None
    target_company: Optional[AbstractCompany] = None
    description: str = ""
    transaction_id: UUID = field(default_factory=uuid4)
    status: TransactionStatus = TransactionStatus.PENDING
    time: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """
        Validate transaction consistency rules.

        Raises:
            ForbiddenTransactionError: 
                - If a TRANSFER is missing a source or target company.
                - If a DEPOSIT is missing a target company.
                - If a DEPOSIT incorrectly specifies a source company.
        """
        if self.transaction_type == TransactionType.TRANSFER:
            if not self.source_company or not self.target_company:
                raise ForbiddenTransactionError("Transfer must have both source and destination")
        
        elif self.transaction_type == TransactionType.DEPOSIT:
            if not self.target_company:
                raise ForbiddenTransactionError("Deposit must have a destination")
            if self.source_company:
                raise ForbiddenTransactionError("Deposit cannot have a source company")
