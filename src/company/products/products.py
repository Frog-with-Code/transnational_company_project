from abc import ABC
from dataclasses import dataclass, fields
from ..common.validation import validate_non_negative

@dataclass(frozen=True)
class AbstractProduct(ABC):
    name: str
    volume: float
    mass: float 
    
    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            validate_non_negative(value)
            