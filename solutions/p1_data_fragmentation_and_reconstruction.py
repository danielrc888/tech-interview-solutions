from typing import Dict


def simple_hash(text: str) -> str:
    """
    Given a text it returns a 120-bit (15-byte) hash value represented
    as 30-character hexadecimal number. It is based on polynomial rolling hash
    function but adapted to output 30 characters fixed-length.

    Data collision probability: 1/2**120
    Time complexity: O(n) where n in the length of text
    """
    # m: prime greather than 2**120 to reduce probability of data collision
    # p: arbitrary prime different than m
    p, m = 2**90 + 133, 2**120 + 451
    p_pow = 1
    p_pow = 1
    hash_value = 0
    for char in text:
        hash_value = (hash_value + (1 + ord(char) - ord("a")) * p_pow) % m
        p_pow = (p_pow * p) % m

    hash_string = hex(hash_value)[2:]
    hash_string = hash_string.zfill(30)[:30]
    return hash_string


def validate_fragments(fragments: Dict):
    """
    Raises an exception if fragments doesn't pass validation

    It checks
        - missing fragments
        - `data` and `hash` attributes exists for all fragments
    """
    ordered_keys = sorted(list(fragments.keys()))
    if len(ordered_keys) == 0:
        raise ValueError("Error: There is no fragment to reconstruct")
    for i in range(len(ordered_keys)):
        if i + 1 != ordered_keys[i]:
            raise ValueError("Error: Missing fragments")
    for value in fragments.values():
        if not isinstance(value, dict):
            raise TypeError("Error: Some fragment value is not a dict")
        if "data" not in value:
            raise ValueError("Error: Some fragment value doesn't have `data` attr")
        if "hash" not in value:
            raise ValueError("Error: Some fragment value doesn't have `hash` attr")


def reconstruct_data(fragments: Dict) -> str:
    """
    Reconstruct data based on their `fragments` where each fragment
    is verified by its `data` and `hash` attributes
    """
    validate_fragments(fragments)
    n_fragments = len(list(fragments.keys()))
    reconstructed_text = ""

    # Iterates over all fragments
    for i in range(1, n_fragments + 1):
        f_data = fragments[i]["data"]
        f_hash = fragments[i]["hash"]
        if simple_hash(f_data) != f_hash:
            raise ValueError("Error: Data integrity verification failed.")
        reconstructed_text += f_data
    return reconstructed_text
