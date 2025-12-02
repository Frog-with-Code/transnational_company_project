from ..common.validation import validate_non_negative
from decimal import Decimal
class NonNegative:
    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = '_' + name

    def __get__(self, obj: object | None, objtype: type | None = None) -> float:
        return getattr(obj, self.private_name)

    def __set__(self, obj: object | None, value: float | int | Decimal) -> None:
        validate_non_negative(value)
        setattr(obj, self.private_name, value)