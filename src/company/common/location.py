from enum import Enum
from dataclasses import dataclass, fields 


class Region(Enum):
    """
    Enumeration of global continental regions used for location classification.

    Values:
        EUROPE: The European continent.
        ASIA: The Asian continent.
        NORTH_AMERICA: The North American continent.
        SOUTH_AMERICA: The South American continent.
        AUSTRALIA: The Australian continent (Oceania).
        ANTARCTICA: The Antarctic continent.
    """
    EUROPE = "Europe",
    ASIA = "Asia",
    NORTH_AMERICA = "North America",
    SOUTH_AMERICA = "South America",
    AUSTRALIA = "Australia",
    ANTARCTICA = "Antarctica"
    
@dataclass
class Location:
    """
    Data class representing a specific physical address with validation.

    This class enforces a constraint that no string-based address fields 
    (country, city, street, building) can be empty or consist solely of whitespace.

    Attributes:
        region (Region): The broad continental region of the location.
        country (str): The name of the country.
        city (str): The name of the city.
        street (str): The name of the street.
        building (str): The building number or identifier.
    """
    region: Region
    country: str
    city: str
    street: str
    building: str
    
    def __post_init__(self):
        """
        Validate that string attributes are not empty after initialization.

        Iterates through all fields defined in the dataclass. If a field is a string,
        it checks if the stripped string is empty.

        Raises:
            ValueError: If any string field is empty or contains only whitespace.
        """
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, str):
                if not value.strip():
                    raise ValueError(f"Field '{field.name}' can't be empty")
