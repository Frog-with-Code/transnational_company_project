from abc import ABC
from dataclasses import dataclass
from ..common.validation import validate_non_negative


@dataclass(frozen=True)
class AbstractProduct(ABC):
    """
    Abstract base class representing a physical product.

    This class is defined as a frozen dataclass, making instances immutable and hashable,
    which allows them to be used as dictionary keys (e.g., in cargo management).

    Attributes:
        name (str): The name of the product.
        volume (float): The volume occupied by a single unit of the product (must be non-negative).
        mass (float): The mass/weight of a single unit of the product (must be non-negative).
    """
    name: str
    volume: float
    mass: float 
    
    def __post_init__(self):
        """
        Validate product dimensions after initialization.

        Raises:
            ValueError: If volume or mass are negative (via validate_non_negative).
        """
        validate_non_negative(self.volume)
        validate_non_negative(self.mass)
