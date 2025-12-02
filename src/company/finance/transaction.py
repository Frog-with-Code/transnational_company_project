from .budget import Money
from ..company_structure.companies import AbstractCompany
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from ..common.exceptions import ForbiddenTransactionError

class TransactionType(Enum):
    TRANSFER = "Transfer"
    REFUND = "Refund"
    DEPOSIT = "Deposit"
    
class TransactionStatus(Enum):
    COMPLETED = "Completed"
    FAILED = "Failed"
    PENDING = "Pending"

@dataclass(frozen=True)
class Transaction:
    transaction_type: TransactionType
    source_money: Money
    target_money: Money
    source_company: Optional[AbstractCompany] = None
    destination_company: Optional[AbstractCompany] = None
    description: str = ""
    transaction_id: UUID = field(default_factory=uuid4)
    status: TransactionStatus = TransactionStatus.PENDING
    time: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if self.transaction_type == TransactionType.TRANSFER:
            if not self.source_company or not self.destination_company:
                raise ForbiddenTransactionError("Transfer must have both source and destination")
        
        elif self.transaction_type == TransactionType.DEPOSIT:
            if not self.destination_company:
                raise ForbiddenTransactionError("Deposit must have a destination")
            if self.source_company:
                raise ForbiddenTransactionError("Deposit cannot have a source company")