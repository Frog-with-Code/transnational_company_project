from enum import Enum


class TransportStatus(Enum):
    """
    Represents the current operational status of a transport vehicle.

    Values:
        AVAILABLE: The transport is free and can be assigned to a new task.
        IN_TRANSIT: The transport is currently performing a trip.
        IN_REPAIR: The transport is undergoing maintenance or repair.
        WRITTEN_OFF: The transport is decommissioned and no longer in use.
        LOADING: The transport is currently being loaded with cargo.
        UNLOADING: The transport is currently being unloaded.
    """
    AVAILABLE = "Available"
    IN_TRANSIT = "Busy"
    IN_REPAIR = "In repair"
    WRITTEN_OFF = "Written off"
    LOADING = "Loading"
    UNLOADING = "Unloading"
    

class ShipType(Enum):
    """
    Types of cargo ships used in the transport system.

    Values:
        TANKER: Designed to carry liquid cargo (e.g., oil, chemicals).
        CONTAINERSHIP: Designed for standardized cargo containers.
        BALKER: Bulk carrier for unpackaged bulk cargo (e.g., ore, grain).
        LASH: LASH (Lighter Aboard Ship) type vessel for barges.
        ROLLKER: Roll-on/roll-off type ship for wheeled cargo.
    """
    TANKER = "Tanker"
    CONTAINERSHIP = "Containership"
    BALKER = "Balker"
    LASH = "LASH"
    ROLLKER = "Rollker"


class CarFuelType(Enum):
    """
    Fuel types supported by road transport vehicles.

    Values:
        BENZIN: Petrol/gasoline-powered vehicle.
        ELECTRICITY: Fully electric vehicle.
        DIESEL: Diesel-powered vehicle.
    """
    BENZIN = "Benzin"
    ELECTRICITY = "Electricity"
    DIESEL = "Diesel"
