import pytest


from solutions.p1_data_fragmentation_and_reconstruction import (
    reconstruct_data,
    simple_hash,
)


def test_simple_hash_lenght():
    text = "hello world text!"
    hashed_text = simple_hash(text)
    assert len(hashed_text) == 30


def test_simple_hash_text_zero_length():
    text = ""
    hashed_text = simple_hash(text)
    assert len(hashed_text) == 30


def test_reconstruct_data_success_case_1():
    fragments = {
        1: {"data": "Hello ", "hash": simple_hash("Hello ")},
        2: {"data": "World", "hash": simple_hash("World")},
        3: {"data": "!", "hash": simple_hash("!")},
    }
    original_data = reconstruct_data(fragments)
    expected_data = "Hello World!"
    assert original_data == expected_data


def test_reconstruct_data_success_case_2():
    fragments = {
        1: {"data": "Yeager", "hash": simple_hash("Yeager")},
        2: {"data": "AI", "hash": simple_hash("AI")},
    }
    original_data = reconstruct_data(fragments)
    expected_data = "YeagerAI"
    assert original_data == expected_data


def test_data_integrity_error():
    fragments = {
        1: {"data": "Hello ", "hash": "other hash"},
        2: {"data": "World", "hash": simple_hash("World")},
        3: {"data": "!", "hash": simple_hash("!")},
    }
    with pytest.raises(ValueError, match="Error: Data integrity verification failed."):
        reconstruct_data(fragments)


def test_missing_fragments_error():
    # Missing fragment 2
    fragments = {
        1: {"data": "Hello ", "hash": "other hash"},
        3: {"data": "!", "hash": simple_hash("!")},
    }
    with pytest.raises(ValueError, match="Error: Missing fragments"):
        reconstruct_data(fragments)


def test_zero_fragments_error():
    fragments = {}
    with pytest.raises(ValueError, match="Error: There is no fragment to reconstruct"):
        reconstruct_data(fragments)


def test_invalid_fragment_value():
    fragments = {
        1: "this is not dict",
        2: {"data": "!", "hash": simple_hash("!")},
    }
    with pytest.raises(TypeError, match="Error: Some fragment value is not a dict"):
        reconstruct_data(fragments)


def test_data_attr_is_not_in_fragment_error():
    fragments = {
        1: {"hash": simple_hash("some")},
        2: {"data": "!", "hash": simple_hash("!")},
    }
    with pytest.raises(
        ValueError, match="Error: Some fragment value doesn't have `data` attr"
    ):
        reconstruct_data(fragments)


def test_hash_attr_is_not_in_fragment_error():
    fragments = {
        1: {"data": "some data"},
        2: {"data": "!", "hash": simple_hash("!")},
    }
    with pytest.raises(
        ValueError, match="Error: Some fragment value doesn't have `hash` attr"
    ):
        reconstruct_data(fragments)
