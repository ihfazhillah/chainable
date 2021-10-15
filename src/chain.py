import functools


class ChainArgumentNotCallable(Exception):
    pass


class Chain:
    """
    Chaining functions using pipe operators. The next function will receive
    result of the previous function call as it first argument.

    For now: all function will be called except the last one.
    To get it's result, you should call it.

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

    def __init__(self, fn, *args, **kwargs):
        if not callable(fn):
            raise ChainArgumentNotCallable

        self.fn = fn
        self.args = args

    def __or__(self, other):
        res = self.fn(*self.args)
        other_args = [res, *other.args]
        other.args = other_args
        return other

    def __call__(self, *args, **kwargs):
        return self.fn(*self.args)


def chainable(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        chain = Chain(fn, *args, **kwargs)
        return chain

    return inner
