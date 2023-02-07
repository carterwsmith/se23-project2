import pytest
from src.dummy import TEST_BOOL, TEST_STRING

def test_dummy_bool():
    assert TEST_BOOL == True

def test_dummy_string():
    assert TEST_STRING == 'Hello World'

