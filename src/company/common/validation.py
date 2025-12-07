from decimal import Decimal 

def validate_non_negative(*args: int | float | Decimal) -> None:
    for value in args:
        if not isinstance(value, (int, float, Decimal)):
            raise TypeError(f"Value {value} must be numeric, {type(value).__name__} was given")
        if value < 0:
            raise ValueError(f"Value {value} must be positive")