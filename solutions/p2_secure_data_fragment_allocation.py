from typing import List, Callable
import math
from decimal import Decimal


def get_max_fragments(risk_to_log: float, risk_factor_to_log: float):
    """
    Given a `risk` and `risk_factor` in logaritmic form, it returns
    the max number of fragments that can be formed
    """
    return risk_to_log // risk_factor_to_log


def can_distribute_log(
    data_centers_to_log: List, fragments: int, max_risk_to_log: float
):
    """
    Given a `max_risk` in logaritmic form, it returns `True` if all fragments
    can be distributed across all `data_centers`. Otherwise, it returns `False`
    """
    total_fragments_needed = 0
    for risk_factor_to_log in data_centers_to_log:
        max_fragments = get_max_fragments(max_risk_to_log, risk_factor_to_log)
        total_fragments_needed += max_fragments
        if total_fragments_needed >= fragments:
            return True
    return total_fragments_needed >= fragments


def binary_search_min(
    condition_function: Callable,
    lower_bound: float,
    upper_bound: float,
    tolerance: float = 1e-6,
):
    """
    It returns the minimum value that satisfies the condition function using
    binary search between the `lowe_bound` and the `upper_bound`.
    """
    result = upper_bound
    while upper_bound - lower_bound > tolerance:
        mid = (lower_bound + upper_bound) / 2
        if condition_function(mid):
            upper_bound = mid  # If condition is met, search in the lower half
            result = upper_bound
        else:
            lower_bound = mid  # If condition is not met, search in the upper half
    return result


def distribute_fragments(data_centers: List, fragments: int):
    """
    It returns the minimized maximum risk achievable through optimal
    distribution of the data fragments across the data centers.

    Time complexity: O(log(D/tolerance))
    Where D is fragments * log(max(data_centers)) and tolerance is
    used to apply a binary search
    """
    if len(data_centers) == 0:
        raise ValueError("Error: data centers length equal zero")
    if fragments == 0:
        raise ValueError("Error: fragments length equal zero")

    # convert to log
    data_centers_to_log = [math.log2(risk_factor) for risk_factor in data_centers]

    # define the compare function for binary search
    def compare_function(value):
        return can_distribute_log(data_centers_to_log, fragments, value)

    max_risk_factor_log = max(data_centers_to_log)
    left, right = 0, max_risk_factor_log * fragments + 1

    # Result to log is an upper aproximation for the the real log2(result)
    result_to_log = binary_search_min(compare_function, left, right)

    result = 0
    for i, risk_factor in enumerate(data_centers):
        risk_factor_to_log = data_centers_to_log[i]
        max_fragments = get_max_fragments(result_to_log, risk_factor_to_log)
        result = max(result, Decimal(risk_factor) ** Decimal(max_fragments))
    return result
