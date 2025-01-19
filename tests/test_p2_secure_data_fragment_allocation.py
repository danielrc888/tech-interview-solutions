import pytest

from decimal import Decimal
from solutions.p2_secure_data_fragment_allocation import distribute_fragments


def test_distribute_fragments_success():
    data_centers = [10, 20, 30]
    fragments = 5
    returned_min_risk = distribute_fragments(data_centers, fragments)
    expected_min_risk = 400
    assert returned_min_risk == expected_min_risk


def test_high_risk_factors():
    data_centers = [10, 20, 30, 600, 800, 1e30, 10e9]
    fragments = 5
    returned_min_risk = distribute_fragments(data_centers, fragments)
    expected_min_risk = 400
    assert returned_min_risk == expected_min_risk


def test_large_number_of_fragments():
    data_centers = [2]
    fragments = int(1e4)
    returned_min_risk = distribute_fragments(data_centers, fragments)
    expected_min_risk = Decimal(2) ** Decimal(1e4)
    assert returned_min_risk == expected_min_risk


def test_no_data_centers_error():
    data_centers = []
    fragments = 5
    with pytest.raises(ValueError, match="Error: data centers length equal zero"):
        distribute_fragments(data_centers, fragments)


def test_no_fragments_error():
    data_centers = [10, 20, 30]
    fragments = 0
    with pytest.raises(ValueError, match="Error: fragments length equal zero"):
        distribute_fragments(data_centers, fragments)
