def validate_non_negative(*args: int | float) -> None:
    for value in args:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Value must be numeric, {type(value).__name__} was given")
        if value < 0:
            raise ValueError(f"Value {value} must be positive")