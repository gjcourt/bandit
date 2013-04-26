from collections import Counter
from functools import partial


class LoggerError(Exception):
    pass


class Logger(object):
    key = None

    def __init__(self):
        self._hit_counter = Counter()
        self._attempt_counter = Counter()

    def hit(self, choice):
        self._hit_counter[choice.id] += 1

    def attempt(self, choice):
        self._attempt_counter[choice.id] += 1

    def data(self):
        return self._hit_counter, self._attempt_counter


class LoggerRegistry(object):
    def __init__(self):
        self._registry = {}

    def register(self, cls):
        if not issubclass(cls, Logger):
            raise LoggerError('You must registr a subclass of Logger')
        if not hasattr(cls, 'key'):
            raise LoggerError('Logger must contain a logging key')
        self._registry[cls.key] = cls()

    def hit(self, *args, **kwargs):
        format = kwargs.pop('format', None)
        return self._registry[format].hit(*args, **kwargs)

    def attempt(self, format, *args, **kwargs):
        format = kwargs.pop('format', None)
        return self._registry[format].attempt(*args, **kwargs)

    def data(self, format=None):
        return self._registry[format].data()

registry = LoggerRegistry()


def register(cls):
    registry.register(cls)
    return cls


register(Logger)


hit = partial(registry.hit)
attempt = partial(registry.attempt)
data = partial(registry.data)
