import pytest

from src.chain import Chain, ChainArgumentNotCallable, chainable


class TestChain:
    def test_accept_only_callable(self):
        Chain(lambda x: print("hello world"))
        with pytest.raises(ChainArgumentNotCallable):
            Chain("hello world")

    def test_next_chain_receive_prev_return_as_first_argument(self):
        def add(a, b):
            return a + b

        result = Chain(add, 1, 2) | Chain(add, 2)
        assert result() == 5

        result = Chain(add, 1, 2) | Chain(add, 2) | Chain(add, 4)
        assert result() == 9

    def test_chainable_decorator(self):
        @chainable
        def add(a, b):
            return a + b

        @chainable
        def multiply(a, b):
            return a * b

        @chainable
        def divide_by_10(x):
            return x / 10

        result = add(1, 2) | add(2) | multiply(10) | divide_by_10()
        assert result() == 5
