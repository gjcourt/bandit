from bandit.math.decorators import zero_division_protect


@zero_division_protect
def ctr(hits, attempts):
    return float(hits)/attempts

