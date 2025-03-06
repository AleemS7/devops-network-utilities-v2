import pytest
import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(root_dir, "src", "subnet_calculator", "cli"))

from subnet import calculate_subnet

def test_calculate_subnet_valid():
    result = calculate_subnet("192.168.1.0", 24)
    assert "network" in result
    assert result["network"] == "192.168.1.0/24"
    assert result["num_hosts"] == 254

def test_calculate_subnet_invalid_ip():
    with pytest.raises(ValueError):
        calculate_subnet("999.999.999.999", 24)

def test_calculate_subnet_invalid_cidr():
    with pytest.raises(ValueError):
        calculate_subnet("192.168.1.0", 999)
