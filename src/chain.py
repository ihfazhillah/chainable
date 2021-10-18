import dataclasses
import functools
from typing import Any


class ChainArgumentNotCallable(Exception):
    pass


@dataclasses.dataclass
class ChainError:
    index: int
    fn: str
    args: Any
    exception: Exception


class ChainErrorException(Exception):
    def __init__(self, index, fn, arguments, original_exception, *args):
        self.index = index
        self.fn = fn
        self.arguments = arguments
        self.original_exception = original_exception
        self.message = f"Exception raises on chain index: {self.index}. Fun: {self.fn}. Args: {self.arguments}"
        super(ChainErrorException, self).__init__(self.message, *args)


class Chain:
    """
    Chaining functions using pipe operators. The next function will receive
    result of the previous function call as it first argument.

    ```python
    @chainable
    def add(a, b):
        return a + b

    chain = add(1, 2) | add(3) | add(4)
    # ((1 + 2) + 3) + 4

    chain()
    # 10
    ```
    """

    chains = []

    def __init__(self, fn, *args, **kwargs):
        if not callable(fn):
            raise ChainArgumentNotCallable

        self.fn = fn
        self.args = args
        self._on_error = None

    def on_error(self, fn):
        self._on_error = fn

    def __or__(self, other):
        left_most = len(self.chains) == 0
        if left_most:
            other.chains = [self, other]
        else:
            other.chains = [*self.chains, other]

        return other

    def __call__(self, *args, **kwargs):
        error_handler = self.get_on_error()
        index = 0
        try:
            chain = self.chains[0]
        except IndexError:
            chain = self

        try:
            result = chain.fn(*chain.args)
            if not self.chains:
                return result

            for index, chain in enumerate(self.chains[1:], 1):
                result = chain.fn(result, *chain.args)
        except Exception as e:
            error_args = [index, chain.fn.__name__, chain.args, e]
            if error_handler:
                return error_handler(ChainError(*error_args))
            raise ChainErrorException(*error_args)
        return result

    def __str__(self):
        string = "chains of:\n"
        if not self.chains:
            string += f" {self.fn.__name__} - {self.args},\n"
        else:
            for chain in self.chains:
                string += f" {chain.fn.__name__} - {chain.args},\n"
        string += "]"
        return string

    def __repr__(self):
        return self.__str__()

    def get_on_error(self):
        return self._on_error


def chainable(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        chain = Chain(fn, *args, **kwargs)
        return chain

    return inner
