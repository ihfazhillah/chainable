import pytest

from src.chain import Chain, ChainArgumentNotCallable, chainable, ChainErrorException


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

    def test_before_chain_called_dont_call_it_instead_add_to_internal_list(self):
        @chainable
        def add(a, b):
            return a + b

        @chainable
        def multiply(a, b):
            return a * b

        chain = add(1, 2) | add(3) | multiply(4)
        assert len(chain.chains) == 3

        assert chain() == 24

    def test_chainable_no_or_operator(self):
        @chainable
        def add(a, b):
            return a + b

        chain = add(1, 2)
        assert chain() == 3

    def test_add_exception_handler_on_the_last_chain(self):
        @chainable
        def add(a, b):
            return a + b

        @chainable
        def should_raises(x):
            raise Exception(x)

        def error_handler(chain_exception):
            return (
                chain_exception.index,
                chain_exception.fn,
                chain_exception.args,
                chain_exception.exception.__class__.__name__,
            )

        chains = add(1, 2) | should_raises() | add(2, 3)
        chains.on_error(error_handler)

        assert chains() == (1, "should_raises", (), "Exception")

    def test_exception_handler_for_no_chain(self):
        @chainable
        def exc(a):
            raise Exception()

        chain = exc(1)
        chain.on_error(lambda x: x.exception.__class__.__name__)

        assert chain() == "Exception"

    def test_when_error_handler_not_defined_raise_chain_error_exception(self):
        @chainable
        def exc(a):
            raise Exception()

        with pytest.raises(ChainErrorException):
            exc(10)()

    def test_error_raised_when_first_chain_error(self):
        @chainable
        def exc(a):
            raise Exception()

        @chainable
        def a(a, b):
            return a

        # when construction, no exception, because we not call any
        chains = exc(1) | a(1)
        with pytest.raises(ChainErrorException):
            chains()

    def test_first_chain_no_attribute(self):
        @chainable
        def first():
            return 10

        @chainable
        def second(a):
            return a

        chains = first() | second()
        assert chains() == 10
