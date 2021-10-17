# Chaining functions using pipe operator. 

The next function will receive
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

## Error Handling

You can also add an error handler to the last chain, and it'll be used as exception handler.

```python
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
```

When no exception handler defined, the `ChainErrorException` exception will be raised