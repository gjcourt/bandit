Bandit
======

Bandit is a lightweight framework allowing you to create multi-arm bandit tests with ease.


Install
-------

    pip install bandit


Usage
-----

    >>> from bandit.test import Test
    >>> from bandit.choice import choice
    >>> class MyTest(Test):
    >>>     pass
    >>>
    >>> test = MyTest([choice(i, i) for i in range(3)])
    >>>
    >>> test.select(2)
    [Choice(id=0, obj=0), Choice(id=1, obj=1)]
    >>>
    >>> test.data()
    Data(hits=Counter(), attempts=Counter({0: 1, 1: 1}))


Examples
-------

Check out an example test in the [repo](https://github.com/gjcourt/bandit/blob/master/bandit/example/simple.py).
