from collections import Counter
from functools import partial

from bandit.data import Data
from bandit.exceptions import LoggerError


class Logger(object):
    test_name = None

    def __init__(self):
        self.hits = Counter()
        self.attempts = Counter()

    def hit(self, choice, **kwargs):
        self.hits[choice.id] += 1

    def attempt(self, choice, **kwargs):
        self.attempts[choice.id] += 1

    def data(self, **kwargs):
        return Data(self.hits, self.attempts)


class LoggerRegistry(object):
    def __init__(self):
        self._registry = {}
        self._context = False

    def register(self, cls):
        if not issubclass(cls, Logger):
            raise LoggerError('You must registr a subclass of Logger')
        if not hasattr(cls, 'test_name'):
            raise LoggerError('Logger must contain a logging test_name')
        self._registry[cls.test_name] = cls()

    def hit(self, *args, **kwargs):
        test_name = kwargs.pop('test_name', None)
        return self._registry[test_name].hit(*args, **kwargs)

    def attempt(self, *args, **kwargs):
        test_name = kwargs.pop('test_name', None)
        return self._registry[test_name].attempt(*args, **kwargs)

    def data(self, *args, **kwargs):
        test_name = kwargs.pop('test_name', None)
        return self._registry[test_name].data()


registry = LoggerRegistry()


def register(cls):
    registry.register(cls)
    return cls


hit = partial(registry.hit, test_name=None)
attempt = partial(registry.attempt, test_name=None)
data = partial(registry.data, test_name=None)

