from typing import Type, TypeVar
from enum import Enum

E = TypeVar("E", bound=Enum)


def normalize_enum(value: str | E | list[E], enum_class: Type[E]) -> E:
    if isinstance(value, str):
        return enum_class(value)
    elif isinstance(value, list):
        return [enum_class(item) if isinstance(item, str) else item for item in value]
    else : return value