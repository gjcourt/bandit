from bandit import logger
from bandit.backend import base


class TestMeta(type):
    def __new__(meta, name, bases, attrs):
        required_attrs = {
            'backend': base.BanditBackend,
            'logger': logger.Logger,
        }

        _meta = {'test_name': name}

        for attr, default in required_attrs.items():
            if attr in attrs:
                _attr = attrs[attr]
            else:
                _attr = type(
                    '%s%s' % (name, attr.capitalize()),
                    (default, ),
                    {'test_name': name}
                )

            _meta[attr] = _attr

        attrs['_meta'] = type('_meta', (object, ), _meta)()

        return super(TestMeta, meta).__new__(meta, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        return super(TestMeta, cls).__init__(name, bases, attrs)


class Test(object):
    """
    This is an abstract base class for a bandit multivariate optimization algorithm.
    To use, subclass Test and choice.  Instantiate your subclass
    with a set of choices.

    Call hit when a hit occurs.  attempt is called automatically.
    The default behavior uses the hit/attempt ratio to calculate probabilities
    of choosing each choice.

    Call select to retrieve a set of choices.
    """
    __metaclass__ = TestMeta

    def __init__(self, choices):
        self.choices = choices
        self.backend = self._meta.backend(self._meta.test_name, self.choices)
        self.logger = self._meta.logger()

    def __getattr__(self, attr):
        logger_attrs = set(['data'])
        if attr in logger_attrs:
            return getattr(self.logger, attr)
        else:
            return self.__getattribute__(attr)

    def select(self, limit=None, **kwargs):
        selections = self.backend.select(limit, **kwargs)
        for selection in selections:
            self.logger.hit(selection)
        return selections


class TTest(Test):
    pass

