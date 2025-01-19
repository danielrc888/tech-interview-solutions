import os


import pytest


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Set the desired working directory here
    target_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(target_directory)
    yield
