from abc import ABC
from dataclasses import dataclass, fields
from ..common.validation import validate_non_negative

@dataclass(frozen=True)
class AbstractProduct(ABC):
    name: str
    volume: float
    mass: float 
    
    def __post_init__(self):
        validate_non_negative(self.volume)
        validate_non_negative(self.mass)
            