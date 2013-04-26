from functools import wraps


def zero_division_protect(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ZeroDivisionError, e:
            return 0
    return inner


def normalize(f):
    @wraps(f)
    def inner(*args, **kwargs):
        scores = f(*args, **kwargs)
        max_score = max(scores) if scores else 1.
        if max_score == 0:
            max_score = 1.
        return [s/float(max_score) for s in scores]
    return inner

