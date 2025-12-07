from ..common.validation import validate_non_negative
from decimal import Decimal


class NonNegative:
    """
    A data descriptor that enforces a non-negative constraint on an attribute.

    This descriptor ensures that any value assigned to the attribute is greater
    than or equal to zero. It delegates the actual validation logic to the
    `validate_non_negative` utility function.

    Attributes:
        private_name (str): The internal name used to store the value in the instance
                            (e.g., '_speed' for a descriptor named 'speed').
    """
    def __set_name__(self, owner: type, name: str) -> None:
        """
        Callback to set the name of the attribute on the owner class.

        Args:
            owner (type): The class owning the descriptor.
            name (str): The name of the attribute to which the descriptor is assigned.
        """
        self.private_name = '_' + name

    def __get__(self, obj: object | None, objtype: type | None = None) -> float:
        """
        Retrieve the value of the attribute.

        Args:
            obj (object | None): The instance accessed, or None if accessed via class.
            objtype (type | None): The type of the instance.

        Returns:
            float: The stored non-negative value.
        """
        return getattr(obj, self.private_name)

    def __set__(self, obj: object | None, value: float | int | Decimal) -> None:
        """
        Validate and set the value of the attribute.

        Args:
            obj (object | None): The instance being modified.
            value (float | int | Decimal): The new value to assign.

        Raises:
            ValueError: If the value is negative (via validate_non_negative).
        """
        validate_non_negative(value)
        setattr(obj, self.private_name, value)
