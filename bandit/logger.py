from collections import Counter
from functools import partial


class LoggerError(Exception):
    pass


class Logger(object):
    test_name = None

    def __init__(self):
        self._hit_counter = Counter()
        self._attempt_counter = Counter()

    def hit(self, choice, **kwargs):
        self._hit_counter[choice.id] += 1

    def attempt(self, choice, **kwargs):
        self._attempt_counter[choice.id] += 1

    def data(self, **kwargs):
        return self._hit_counter, self._attempt_counter


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

