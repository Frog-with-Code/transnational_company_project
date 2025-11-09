from enum import Enum

class TransportStatus(Enum):
    AVAILABLE = "Available"
    IN_TRANSIT = "Busy"
    IN_REPAIR = "In repair"
    WRITTEN_OFF = "Written off"
    LOADING = "Loading"
    UNLOADING = "Unloading"
    
class ShipType(Enum):
    TANKER = "Tanker"
    CONTAINERSHIP = "Containership"
    BALKER = "Balker"
    LASH = "LASH"
    ROLLKER = "Rollker"

class CarFuelType(Enum):
    BENZIN = "Benzin"
    ELECTRICITY = "Electricity"
    DIESEL = "Diesel"