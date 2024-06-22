from functools import wraps


def print_decorator(func):

    @wraps(func)
    def decorator(*args, **kwargs):
        print(f"[before] {func.__name__} 호출")
        result = func(*args, **kwargs)
        print(f"[after] {func.__name__} 호출")
        return result
    return decorator
