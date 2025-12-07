import pytest

from company.common.descriptors import NonNegative

class DescriptorHost:
    value = NonNegative()
    
    def __init__(self, value):
        self.value = value

class TestNonNegativeDescriptor:
    def test_valid_value(self):
        obj = DescriptorHost(10)
        assert obj.value == 10
        
        obj.value = 0
        assert obj.value == 0
        
        obj.value = 100.5
        assert obj.value == 100.5

    def test_negative_value_init(self):
        with pytest.raises(ValueError):
            DescriptorHost(-1)

    def test_negative_value_assignment(self):
        obj = DescriptorHost(10)
        with pytest.raises(ValueError):
            obj.value = -5
            
    def test_non_numeric_value_init(self):
        with pytest.raises(TypeError):
            DescriptorHost("a")
