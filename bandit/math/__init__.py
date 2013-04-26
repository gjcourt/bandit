import math
import operator

from bandit.math.decorators import (
    normalize,
    zero_division_protect
)


@zero_division_protect
def mean(seq):
    return float(sum(seq))/len(seq)

def cross_product(v1, v2):
    return map(operator.mul, v1, v2)

def dot_product(v1, v2):
    return sum(cross_product(v1, v2))

def multi_cross(*vecs):
    return reduce(cross_product, vecs)

class one(float):
    """Float class with default value of 1"""
    def __new__(cls, *args, **kwargs):
        if not args:
            args = (1., )
        return super(one, cls).__new__(cls, *args, **kwargs)

def var(coll):
    m = mean(coll)
    return mean([(x-m)**2 for x in coll])

def std(coll):
    return math.sqrt(var(coll))

