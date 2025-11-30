from enum import Enum
from dataclasses import dataclass, fields 

class Region(Enum):
    EUROPE = "Europe",
    ASIA = "Asia",
    NORTH_AMERICA = "North America",
    SOUTH_AMERICA = "South America",
    AUSTRALIA = "Australia",
    ANTARCTICA = "Antarctica"
    
@dataclass
class Location:
    region: Region
    country: str
    city: str
    street: str
    building: str
    
    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, str):
                if not value.strip():
                    raise ValueError(f"Поле '{field.name}' не может быть пустым")