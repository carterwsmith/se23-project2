import pytest
from src.main.dummy import TEST_BOOL, TEST_STRING

def test_dummy_bool():
    assert TEST_BOOL == False

def test_dummy_string():
    assert TEST_STRING == 'Hello World'

