from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class AbstractProduct:
    name: str
    volume: float
    mass: float 