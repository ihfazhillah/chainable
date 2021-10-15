# Chaining functions using pipe operator. 

The next function will receive
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