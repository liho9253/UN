from functools import wraps


def decorator_permission(func):
    @wraps(func)
    def wrapper():
        if("1" == "1"):
            func()

    return wrapper


@decorator_permission
def test_decorator():
    print('test')