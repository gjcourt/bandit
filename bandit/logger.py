from collections import Counter
from functools import partial

from bandit.data import Data
from bandit.exceptions import LoggerError


class Logger(object):
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

    def register(self, test_name, cls):
        if not issubclass(cls, Logger):
            raise LoggerError('You must registr a subclass of Logger')
        self._registry[test_name] = cls()

    def hit(self, *args, **kwargs):
        test_name = kwargs.pop('test_name', None)
        return self._registry[test_name].hit(*args, **kwargs)

    def attempt(self, *args, **kwargs):
        test_name = kwargs.pop('test_name', None)
        return self._registry[test_name].attempt(*args, **kwargs)

    def data(self, *args, **kwargs):
        test_name = kwargs.pop('test_name', None)
        return self._registry[test_name].data()


class Register(object):
    def __init__(self, registry):
        self.registry = registry
        self.test_name = None

    def register_wrapper(self, cls):
        self.registry.register(self.test_name, cls)
        self.test_name = None
        return cls

    def __call__(self, test_name, *args):
        self.test_name = test_name
        nargs = len(args)
        if nargs == 0:
            return self.register_wrapper
        elif nargs == 1:
            cls = args[0]
            return self.register_wrapper(cls)
        else:
            raise Exception('Improper use of decorator')


registry = LoggerRegistry()
register = Register(registry)


hit = partial(registry.hit, test_name=None)
attempt = partial(registry.attempt, test_name=None)
data = partial(registry.data, test_name=None)

