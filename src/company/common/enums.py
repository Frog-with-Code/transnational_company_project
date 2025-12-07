from typing import Type, TypeVar
from enum import Enum


E = TypeVar("E", bound=Enum)


def normalize_enum(value: str | E | list[E | str], enum_class: Type[E]) -> E | list[E]:
    """
    Normalize a string, an Enum member, or a list of them into the target Enum type.

    This utility ensures that inputs are converted to their proper Enum instances.
    It is useful when handling input data that might mix raw string values (e.g., from JSON)
    with actual Enum objects.

    Args:
        value (str | E | list[str | E]): The input value(s) to convert.
            - If a string, it is converted to the Enum member with that value.
            - If an Enum member, it is returned as is.
            - If a list, a new list is returned with all items normalized.
        enum_class (Type[E]): The specific Enum class to use for conversion.

    Returns:
        E | list[E]: The normalized Enum member (or a list of them).
    """
    if isinstance(value, str):
        return enum_class(value)
    elif isinstance(value, list):
        return [enum_class(item) if isinstance(item, str) else item for item in value]
    else:
        return value
