import functools
from typing import Any


class ChainArgumentNotCallable(Exception):
    pass


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

    def __or__(self, other):
        left_most = len(self.chains) == 0
        if left_most:
            other.chains = [self, other]
        else:
            other.chains = [*self.chains, other]

        return other

    def __call__(self, *args, **kwargs):
        if len(self.chains) == 0:
            # it means no pipe operator around
            return self.fn(*self.args)

        first_chain = self.chains[0]
        res = first_chain.fn(*first_chain.args)
        return functools.reduce(self._call_func, self.chains[1:], res)

    @staticmethod
    def _call_func(res: Any, chain):
        return chain.fn(res, *chain.args)


def chainable(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        chain = Chain(fn, *args, **kwargs)
        return chain

    return inner
