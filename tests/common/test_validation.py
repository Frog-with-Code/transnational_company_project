import pytest

from company.common.validation import validate_non_negative

class TestValidation:
    def test_single_value_valid(self):
        validate_non_negative(10)
        validate_non_negative(0)
        validate_non_negative(0.0)

    def test_multiple_values_valid(self):
        validate_non_negative(10, 20, 0, 5.5)

    def test_single_value_invalid(self):
        with pytest.raises(ValueError):
            validate_non_negative(-1)

    def test_multiple_values_invalid(self):
        with pytest.raises(ValueError):
            validate_non_negative(10, -5, 20)
